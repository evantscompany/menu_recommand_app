import re

def calculate_recommendation_score(menu, user, daily_inquiry, weather_data, history=None):
    """
    [정밀 튜닝된 추천 알고리즘]
    1. 기본 점수 부여 (0점이 아닌 40점에서 시작)
    2. 가중치 밸런싱 (매칭률이 70~90%대에 형성되도록 조정)
    3. 필터링 로직 유연화
    """
    # 0. 기초 필터 (기존 유지)
    details = menu.details
    if not details or not menu.is_lunch_available:
        return -1

    # --- [Step 1] 하드 필터링 및 기본 점수 설정 ---
    score = 40.0  # 기본 점수를 부여하여 '추천 가능성'을 깔고 시작함
    
    # 1. 예산 필터링 (숫자만 추출)
    try:
        raw_budget = daily_inquiry.budget_range
        numeric_budget = int(re.sub(r'[^0-9]', '', str(raw_budget)))
    except (ValueError, TypeError, AttributeError):
        numeric_budget = user.lunch_budget_max

    # 예산 초과 시 즉시 제외 (기존 유지)
    if menu.price_level > numeric_budget:
        return 0 
    
    # 예산 안쪽이면 보너스 (가성비 가점)
    if menu.price_level <= numeric_budget * 0.8:
        score += 10

    # 2. 식단 제약 필터링 (감점 폭 완화)
    if daily_inquiry.dietary_restriction and daily_inquiry.dietary_restriction != "뭐든 잘 먹음":
        if daily_inquiry.dietary_restriction not in (menu.category or "") and \
           daily_inquiry.dietary_restriction not in (menu.menu_name or ""):
            score -= 20  # -50점에서 -20점으로 완화 (완전 제외보다는 순위 하락 유도)

    # --- [Step 2] 미각 성향 매칭 (Taste Alignment) ---
    
    # 맵기 선호도 (가중치 상향)
    try:
        daily_spicy = int(re.search(r'\d', daily_inquiry.spicy_level).group())
    except (AttributeError, ValueError, TypeError):
        daily_spicy = user.spicy_threshold

    spicy_diff = abs(daily_spicy - (details.spicy_level or 3))
    # 완벽 일치 시 +15점, 차이날수록 감점
    score += (15 - (spicy_diff * 5))

    # 간 조절 (가중치 조정)
    salt_map = {"많이 싱겁게": 1, "싱겁게": 2, "보통": 3, "조금 짜게": 4, "많이 짜게": 5}
    user_salt_pref = salt_map.get(daily_inquiry.salty_level, 3)
    salt_diff = abs(user_salt_pref - (details.saltiness_level or 3))
    score += (10 - (salt_diff * 3))

    # --- [Step 3] 탐험 성향 반영 ---
    if daily_inquiry.exploration_style == "모험형(새로운 도전)":
        if not history or (history.visit_count or 0) == 0:
            score += 12
    elif daily_inquiry.exploration_style == "안정형(익숙한 맛)":
        if history and (history.visit_count or 0) > 0:
            score += 10

    # --- [Step 4] 실시간 외부 환경 (가점 위주) ---
    current_weather = weather_data.get("weather", "Clear")
    current_temp = weather_data.get("temp", 20)
    
    if current_weather in ["Rain", "Snow", "Drizzle"]:
        if details.texture == "Crispy": score += 8  
        if (details.heaviness or 0) >= 4.0: score += 7    
    
    if current_temp > 28 and details.serving_temperature == "Cold":
        score += 10

    # --- [Step 5] 과거 피드백 반영 ---
    if history:
        if (history.user_rating or 0) >= 4:
            score += 15
        if history.is_revisit_intended is False:
            score -= 30 # 아예 안 먹겠다는 메뉴는 하단으로
        if (history.user_rating or 0) <= 2:
            score -= 25
        if history.last_eaten_category == menu.category:
            score -= 10 # 연속 같은 카테고리 방지

    # --- [Step 6] 신뢰도 및 통계 보정 ---
    # 평점 5점 만점 기준 보너스
    rating_bonus = (details.real_satisfaction_score or 3.0) * 2  # 최대 10점
    # 광고 의심도 감점 (영향력 축소)
    ad_penalty = (details.ad_suspicion_index or 0) * 5 # 최대 5점 감점
    score += (rating_bonus - ad_penalty)
    
    # 최종 점수가 너무 튀지 않게 0~100 사이로 보정
    return max(0, min(100, score))

def generate_recommendation_reason(menu, weather_data):
    """
    추천 이유 생성 (기존 로직 유지하되 평점 강조 추가)
    """
    weather = weather_data.get("weather", "Clear")
    temp = weather_data.get("temp", 20)

    if weather in ["Rain", "Snow"]:
        return f"비 오는 날엔 바삭하고 든든한 {menu.menu_name} 어떠세요?"
    if temp > 28:
        return f"무더위를 날려줄 시원한 {menu.category} 메뉴를 추천해요!"
    if menu.details and menu.details.real_satisfaction_score >= 4.5:
        return f"실제 이용자 평점이 {menu.details.real_satisfaction_score}점으로 매우 검증된 메뉴예요!"
    
    return f"오늘 유저님의 취향과 {menu.category} 카테고리가 잘 어울려요."