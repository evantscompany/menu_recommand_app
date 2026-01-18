import re

def calculate_recommendation_score(store, user, daily_inquiry, weather_data, history=None):
    """
    [통합 추천 알고리즘 - 데이터 매칭 최적화 버전]
    1. store: 식당 기본 정보 (models.Store)
    2. user: 사용자 기본 성향 (models.User)
    3. daily_inquiry: 프론트엔드 설문 응답 (schemas.DailyInquiry)
    4. weather_data: 실시간 날씨/온도 (dict)
    5. history: 과거 기록 (models.UserHistory, Optional)
    """
    score = 0
    details = store.details # StoreDetail 관계
    
    # 기초 필터: 상세 정보가 없거나 점심 영업을 안 하면 제외
    if not details or not store.is_lunch_available:
        return -1

    # --- [Step 1] 하드 필터링 (Hard Constraints) ---
    
    # 1. 예산 필터링 (AttributeError 해결 및 파싱 강화)
    try:
        raw_budget = daily_inquiry.budget_range
        # "15000원 이하" -> 15000 추출
        numeric_budget = int(re.sub(r'[^0-9]', '', raw_budget))
    except (ValueError, TypeError):
        numeric_budget = user.lunch_budget_max # 실패 시 유저 기본값

    # [수정 완료] 모델의 필드명인 price_level을 사용합니다.
    if store.price_level > numeric_budget:
        return 0 
    
    # 2. 식단 제약 필터링
    if daily_inquiry.dietary_restriction != "뭐든 잘 먹음":
        # 식당 카테고리나 이름에 제약 키워드(예: 비건)가 포함되어 있는지 확인
        if daily_inquiry.dietary_restriction not in store.category and \
           daily_inquiry.dietary_restriction not in store.store_name:
            # 엄격한 필터를 원하시면 여기서 return 0를 사용하세요. 
            # 지금은 점수 감점 방식으로 처리합니다.
            score -= 50

    # --- [Step 2] 미각 성향 매칭 (Taste Alignment) ---
    
    # 맵기 선호도 추출: "3(불닭볶음면)" -> 3
    try:
        daily_spicy = int(re.sub(r'[^0-9]', '', daily_inquiry.spicy_level)[0])
    except (IndexError, ValueError, TypeError):
        daily_spicy = user.spicy_threshold

    # 오늘의 선호도와 식당 실제 맵기(StoreDetail.spicy_level) 차이 계산
    spicy_diff = abs(daily_spicy - details.spicy_level)
    score += (5 - spicy_diff) * 7  # 차이가 작을수록 고득점 (최대 35점)

    # 간 조절 매핑
    salt_map = {"많이 싱겁게": 1, "싱겁게": 2, "보통": 3, "조금 짜게": 4, "많이 짜게": 5}
    user_salt_pref = salt_map.get(daily_inquiry.salty_level, 3)
    salt_diff = abs(user_salt_pref - details.saltiness_level)
    score += (5 - salt_diff) * 3   # 최대 15점

    # --- [Step 3] 탐험 성향 반영 ---
    
    if daily_inquiry.exploration_style == "모험형(새로운 도전)":
        if not history or history.visit_count == 0:
            score += 20  # 방문한 적 없는 식당 가산점
    elif daily_inquiry.exploration_style == "안정형(익숙한 맛)":
        if history and history.visit_count > 0:
            score += 15  # 가본 적 있는 식당 가산점

    # --- [Step 4] 실시간 외부 환경 (Environment) ---
    current_weather = weather_data.get("weather", "Clear")
    
    # 비/눈 올 때 무거운 음식 혹은 바삭한 음식 선호도
    if current_weather in ["Rain", "Snow", "Drizzle"]:
        if details.texture == "Crispy": score += 10  
        if details.heaviness >= 4.0: score += 10    
    
    # 더울 때 차가운 음식 가산점
    if weather_data.get("temp", 20) > 28 and details.serving_temperature == "Cold":
        score += 15

    # --- [Step 5] 과거 피드백 반영 (Feedback Learning) ---
    if history:
        if history.user_rating and history.user_rating >= 4:
            score += 25 # 만족했던 곳은 가점
        if history.is_revisit_intended is False:
            return 0    # 재방문 의사 없는 곳은 제외
        if history.user_rating and history.user_rating <= 2:
            score -= 40 # 불만족했던 곳 감점
        if history.last_eaten_category == store.category:
            score -= 20 # 방금 먹은 메뉴 카테고리는 가급적 피함

    # --- [Step 6] 신뢰도 및 통계 보정 ---
    # 실제 만족도(1~5) 가점 및 광고 의심 지수 감점
    trust_score = (details.real_satisfaction_score * 2) - (details.ad_suspicion_index * 15)
    score += trust_score
    
    return max(0, score)