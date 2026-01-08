def calculate_recommendation_score(store, user, daily_inquiry, weather_data, history=None):
    """
    [통합 추천 알고리즘]
    1. store: 식당 및 상세 정보 (Store, StoreDetail)
    2. user: 사용자 기본 성향 및 제약 사항 (User)
    3. daily_inquiry: 오늘의 컨디션/인원/에너지 (DailyInquiry)
    4. weather_data: 실시간 날씨/온도 (dict)
    5. history: 해당 식당에 대한 사용자의 과거 방문/피드백 기록 (UserHistory, Optional)
    """
    score = 0
    details = store.details
    
    # 기초 필터: 정보가 없거나 점심 영업을 안 하면 제외
    if not details or not store.is_lunch_available:
        return -1

    # --- [Step 1] 하드 필터링 (Hard Constraints) ---
    # 예산 필터: 사용자의 점심 상한선보다 비싸면 제외
    if store.price_level > user.lunch_budget_max:
        return 0
    
    # 식단 제약: 알레르기나 채식 성향이 카테고리와 충돌할 경우 (예시 로직)
    if user.dietary_label != "none" and user.dietary_label not in store.category:
        return 0

    # --- [Step 2] 미각 성향 매칭 (Taste Alignment) ---
    # 사용자의 평소 취향(Threshold)과 식당 수치의 차이 계산 (적을수록 고득점)
    spicy_diff = abs(user.spicy_threshold - details.spicy_level)
    score += (5 - spicy_diff) * 5  # 최대 25점

    salt_diff = abs(user.saltiness_preference - details.saltiness_level)
    score += (5 - salt_diff) * 3   # 최대 15점

    # --- [Step 3] 오늘의 컨디션 반영 (Daily Context) ---
    # 오전 업무 상태 (전쟁터라면 자극적인 맛 가중치)
    if daily_inquiry.condition == "war":
        if details.spicy_level >= user.spicy_threshold:
            score += 15
    
    # 인원 구성 (팀 단위라면 규모와 속도 중점)
    if daily_inquiry.social == "team":
        if store.suitable_ground_size >= 4: score += 10
        if store.is_quick_meal: score += 10
    
    # 에너지 상태 (든든함 vs 가벼움)
    if daily_inquiry.energy == "heavy":
        score += (details.heaviness * 4)  # 최대 20점
    else:
        score += (5 - details.heaviness) * 4 # 가벼울수록 가점

    # --- [Step 4] 실시간 외부 환경 (Environment) ---
    current_weather = weather_data.get("weather")
    # 비/눈 올 때의 특수 선호도 (식감 및 무게감)
    if current_weather in ["Rain", "Snow", "Drizzle"]:
        if details.texture == "crispy": score += 10  # 바삭함(튀김/전 등)
        if details.heaviness >= 4.0: score += 10    # 묵직한 국물
    # 온도에 따른 보정
    if weather_data.get("temp", 20) > 28 and details.serving_temperature == "Cold":
        score += 15

    # --- [Step 5] 과거 피드백 반영 (Feedback Learning) ---
    if history:
        # 평점이 높았던 곳은 강력 추천
        if history.user_rating and history.user_rating >= 4:
            score += 25 
        # 재방문 의사가 없다고 한 곳은 강력 제외
        if history.is_revisit_intended is False:
            score -= 100
        # 평점이 낮았던 곳 감점
        if history.user_rating and history.user_rating <= 2:
            score -= 40
        # 다양성 유지: 어제 먹은 카테고리는 오늘 피함
        if history.last_eaten_category == store.category:
            score -= 30

    # --- [Step 6] 신뢰도 및 성향 보정 ---
    # 광고 의심 지수 패널티 및 실제 만족도 가점
    trust_score = (details.real_satisfaction_score * 2) - (details.ad_suspicion_index * 15)
    score += trust_score

    # 새로운 도전형 사용자에게는 가보지 않은 곳 가산점
    if user.is_adventurous and (not history or history.visit_count == 0):
        score += 20

    return max(0, score)