import re
import math
import random
from datetime import datetime, timedelta
from app.database import SessionLocal
from app import models
from app.models import FeedbackType
from collections import defaultdict, Counter

def get_latest_feedback(db: Session, user_id: int, menu_name: str):
    """
    특정 사용자의 특정 메뉴에 대한 최신 피드백 조회
    """
    return db.query(models.RecommendationFeedback)\
        .filter(models.RecommendationFeedback.user_id == user_id)\
        .filter(models.RecommendationFeedback.menu_name == menu_name)\
        .order_by(models.RecommendationFeedback.created_at.desc())\
        .first()

# 🧠 고도화된 알고리즘 전략들
class PatternMiningStrategy:
    """패턴 마이닝 전략 - 현재 데이터에서 숨겨진 패턴 발견"""
    
    @staticmethod
    def calculate_bonus(user, menu, db):
        """패턴 기반 보너스 계산"""
        bonus = 0
        
        # 🕐 시간 패턴 분석
        time_pattern_bonus = PatternMiningStrategy._analyze_time_pattern(user, menu, db)
        bonus += time_pattern_bonus
        
        # 🔄 주기성 패턴 분석
        cyclical_pattern_bonus = PatternMiningStrategy._analyze_cyclical_pattern(user, menu, db)
        bonus += cyclical_pattern_bonus
        
        # 📈 성장 패턴 분석
        growth_pattern_bonus = PatternMiningStrategy._analyze_growth_pattern(user, menu, db)
        bonus += growth_pattern_bonus
        
        return bonus
    
    @staticmethod
    def _analyze_time_pattern(user, menu, db):
        """시간 패턴 분석"""
        current_hour = datetime.now().hour
        
        # 같은 시간대의 과거 선택 분석
        same_hour_history = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(
                models.UserHistory.user_id == user.user_id,
                models.Menu.category == menu.category
            ).all()
        
        if same_hour_history:
            hour_preferences = defaultdict(list)
            for history in same_hour_history:
                hour = history.last_visit_date.hour
                hour_preferences[hour].append(history.user_rating or 3)
            
            current_hour_ratings = hour_preferences.get(current_hour, [3])
            avg_rating = sum(current_hour_ratings) / len(current_hour_ratings)
            
            if avg_rating >= 4.0:
                return 8  # 시간대별 선호도 보너스
            elif avg_rating >= 3.5:
                return 4
        
        return 0
    
    @staticmethod
    def _analyze_cyclical_pattern(user, menu, db):
        """주기성 패턴 분석"""
        current_weekday = datetime.now().weekday()
        
        same_weekday_history = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(
                models.UserHistory.user_id == user.user_id,
                models.Menu.category == menu.category
            ).all()
        
        if same_weekday_history:
            weekday_preferences = defaultdict(list)
            for history in same_weekday_history:
                weekday = history.last_visit_date.weekday()
                weekday_preferences[weekday].append(history.user_rating or 3)
            
            current_weekday_ratings = weekday_preferences.get(current_weekday, [3])
            avg_rating = sum(current_weekday_ratings) / len(current_weekday_ratings)
            
            if avg_rating >= 4.0:
                return 6  # 요일별 선호도 보너스
            elif avg_rating >= 3.5:
                return 3
        
        return 0
    
    @staticmethod
    def _analyze_growth_pattern(user, menu, db):
        """성장 패턴 분석"""
        all_history = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .order_by(models.UserHistory.last_visit_date.desc())\
            .limit(20)\
            .all()
        
        if len(all_history) >= 5:
            recent_ratings = [h.user_rating or 3 for h in all_history[:5]]
            previous_ratings = [h.user_rating or 3 for h in all_history[5:10]]
            
            recent_avg = sum(recent_ratings) / len(recent_ratings)
            previous_avg = sum(previous_ratings) / len(previous_ratings)
            
            if recent_avg > previous_avg + 0.5:
                # 성장 중 - 새로운 메뉴에 더 개방적
                if len([h for h in all_history if h.menu.category == menu.category]) == 0:
                    return 10  # 새로운 카테고리 탐험 보너스
            elif recent_avg < previous_avg - 0.5:
                # 보수적 - 익숙한 메뉴 선호
                if len([h for h in all_history if h.menu.category == menu.category]) > 0:
                    return 8  # 익숙한 카테고리 보너스
        
        return 0

class BehavioralInsightsStrategy:
    """행동 통찰 전략 - 사용자 행동에서 의미 발견"""
    
    @staticmethod
    def calculate_bonus(user, menu, db):
        """행동 통찰 기반 보너스 계산"""
        bonus = 0
        
        # 🎯 선택 일관성 분석
        consistency_bonus = BehavioralInsightsStrategy._analyze_selection_consistency(user, menu, db)
        bonus += consistency_bonus
        
        # 📊 평점 편차 분석
        rating_variance_bonus = BehavioralInsightsStrategy._analyze_rating_variance(user, menu, db)
        bonus += rating_variance_bonus
        
        # 🔄 재방문 패턴 분석
        revisit_pattern_bonus = BehavioralInsightsStrategy._analyze_revisit_pattern(user, menu, db)
        bonus += revisit_pattern_bonus
        
        return bonus
    
    @staticmethod
    def _analyze_selection_consistency(user, menu, db):
        """선택 일관성 분석"""
        user_histories = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .all()
        
        if len(user_histories) >= 3:
            category_counts = Counter([h.menu.category for h in user_histories])
            most_common_category = category_counts.most_common(1)[0][0]
            
            if menu.category == most_common_category:
                consistency_score = category_counts[most_common_category] / len(user_histories)
                if consistency_score >= 0.6:
                    return 7  # 일관성 보너스
        
        return 0
    
    @staticmethod
    def _analyze_rating_variance(user, menu, db):
        """평점 편차 분석"""
        user_histories = db.query(models.UserHistory)\
            .filter(models.UserHistory.user_id == user.user_id,
                   models.UserHistory.user_rating.isnot(None))\
            .all()
        
        if len(user_histories) >= 5:
            ratings = [h.user_rating for h in user_histories]
            avg_rating = sum(ratings) / len(ratings)
            
            variance = sum((r - avg_rating) ** 2 for r in ratings) / len(ratings)
            std_dev = math.sqrt(variance)
            
            if std_dev < 1.0:
                menu_detail = db.query(models.MenuDetail)\
                    .join(models.Menu)\
                    .filter(models.Menu.menu_id == menu.menu_id)\
                    .first()
                
                if menu_detail and menu_detail.real_satisfaction_score >= avg_rating:
                    return 8  # 예측 가능성 보너스
        
        return 0
    
    @staticmethod
    def _analyze_revisit_pattern(user, menu, db):
        """재방문 패턴 분석"""
        user_histories = db.query(models.UserHistory)\
            .filter(models.UserHistory.user_id == user.user_id,
                   models.UserHistory.is_revisit_intended.isnot(None))\
            .all()
        
        if len(user_histories) >= 3:
            revisit_intentions = [h.is_revisit_intended for h in user_histories]
            revisit_rate = sum(revisit_intentions) / len(revisit_intentions)
            
            if revisit_rate >= 0.7:
                history = db.query(models.UserHistory)\
                    .filter(models.UserHistory.user_id == user.user_id,
                           models.UserHistory.menu_id == menu.menu_id)\
                    .first()
                
                if history and history.visit_count > 0:
                    return 6  # 재방문 선호 보너스
        
        return 0

class TemporalDynamicsStrategy:
    """시간 동학 전략 - 시간의 흐름을 고려한 추천"""
    
    @staticmethod
    def calculate_bonus(user, menu, db):
        """시간 동학 기반 보너스 계산"""
        bonus = 0
        
        # ⏰ 최근성 효과
        recency_bonus = TemporalDynamicsStrategy._calculate_recency_effect(user, menu, db)
        bonus += recency_bonus
        
        # 📅 계절성 효과
        seasonality_bonus = TemporalDynamicsStrategy._calculate_seasonality_effect(user, menu, db)
        bonus += seasonality_bonus
        
        # 🔄 주기성 효과
        periodicity_bonus = TemporalDynamicsStrategy._calculate_periodicity_effect(user, menu, db)
        bonus += periodicity_bonus
        
        return bonus
    
    @staticmethod
    def _calculate_recency_effect(user, menu, db):
        """최근성 효과 계산"""
        recent_histories = db.query(models.UserHistory)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .order_by(models.UserHistory.last_visit_date.desc())\
            .limit(5)\
            .all()
        
        if recent_histories:
            recent_categories = [h.menu.category for h in recent_histories]
            category_ratio = recent_categories.count(menu.category) / len(recent_categories)
            
            if category_ratio >= 0.4:
                return 5  # 최근 선호 보너스
        
        return 0
    
    @staticmethod
    def _calculate_seasonality_effect(user, menu, db):
        """계절성 효과 계산"""
        current_month = datetime.now().month
        
        seasonal_histories = db.query(models.UserHistory)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .all()
        
        if seasonal_histories:
            seasonal_preferences = defaultdict(list)
            for history in seasonal_histories:
                month = history.last_visit_date.month
                seasonal_preferences[month].append(history.user_rating or 3)
            
            current_month_ratings = seasonal_preferences.get(current_month, [3])
            avg_rating = sum(current_month_ratings) / len(current_month_ratings)
            
            if avg_rating >= 4.0:
                return 6  # 계절성 선호 보너스
        
        return 0
    
    @staticmethod
    def _calculate_periodicity_effect(user, menu, db):
        """주기성 효과 계산"""
        user_histories = db.query(models.UserHistory)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .all()
        
        if len(user_histories) >= 4:
            weekday_patterns = defaultdict(list)
            for history in user_histories:
                weekday = history.last_visit_date.weekday()
                weekday_patterns[weekday].append(history.menu.category)
            
            current_weekday = datetime.now().weekday()
            current_pattern = weekday_patterns.get(current_weekday, [])
            
            if len(current_pattern) >= 2:
                most_common_category = Counter(current_pattern).most_common(1)[0][0]
                if menu.category == most_common_category:
                    return 8  # 주기성 패턴 보너스
        
        return 0

class SocialLearningStrategy:
    """사회적 학습 전략 - 다른 사용자 데이터로 학습"""
    
    @staticmethod
    def calculate_bonus(user, menu, db):
        """사회적 학습 기반 보너스 계산"""
        bonus = 0
        
        # 👥 유사 사용자 패턴
        similar_user_bonus = SocialLearningStrategy._calculate_similar_user_bonus(user, menu, db)
        bonus += similar_user_bonus
        
        # 📈 인기도 트렌드
        popularity_bonus = SocialLearningStrategy._calculate_popularity_trend(menu, db)
        bonus += popularity_bonus
        
        # 🌟 전문가 추천
        expert_bonus = SocialLearningStrategy._calculate_expert_recommendation(menu, db)
        bonus += expert_bonus
        
        return bonus
    
    @staticmethod
    def _calculate_similar_user_bonus(user, menu, db):
        """유사 사용자 패턴 보너스"""
        similar_users = db.query(models.UserProfile)\
            .filter(
                models.UserProfile.spicy_threshold.between(
                    user.spicy_threshold - 1, user.spicy_threshold + 1
                ),
                models.UserProfile.lunch_budget_max.between(
                    user.lunch_budget_max - 3000, user.lunch_budget_max + 3000
                ),
                models.UserProfile.is_adventurous == user.is_adventurous
            )\
            .limit(10)\
            .all()
        
        if similar_users:
            similar_user_histories = db.query(models.UserHistory)\
                .join(models.Menu)\
                .filter(
                    models.UserHistory.user_id.in_([u.user_id for u in similar_users]),
                    models.Menu.menu_id == menu.menu_id
                )\
                .all()
            
            if similar_user_histories:
                avg_rating = sum(h.user_rating or 3 for h in similar_user_histories) / len(similar_user_histories)
                if avg_rating >= 4.0:
                    return 7  # 유사 사용자 선호 보너스
        
        return 0
    
    @staticmethod
    def _calculate_popularity_trend(menu, db):
        """인기도 트렌드 보너스"""
        recent_histories = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(
                models.UserHistory.last_visit_date >= datetime.now() - timedelta(days=7),
                models.Menu.menu_id == menu.menu_id
            )\
            .all()
        
        if recent_histories:
            recent_popularity = len(recent_histories)
            total_histories = db.query(models.UserHistory)\
                .filter(models.Menu.menu_id == menu.menu_id)\
                .count()
            
            if total_histories > 0:
                popularity_ratio = recent_popularity / total_histories
                if popularity_ratio >= 0.3:
                    return 5  # 인기도 트렌드 보너스
        
        return 0
    
    @staticmethod
    def _calculate_expert_recommendation(menu, db):
        """전문가 추천 보너스"""
        menu_detail = db.query(models.MenuDetail)\
            .join(models.Menu)\
            .filter(models.Menu.menu_id == menu.menu_id)\
            .first()
        
        if menu_detail and menu_detail.real_satisfaction_score >= 4.5:
            return 6  # 전문가 추천 보너스
        
        return 0

class SurpriseGenerationStrategy:
    """놀라움 생성 전략 - 예상치 못은 추천"""
    
    @staticmethod
    def calculate_bonus(user, menu, db):
        """놀라움 생성 기반 보너스 계산"""
        bonus = 0
        
        # 🎲 예상치 못은 조합
        unexpected_bonus = SurpriseGenerationStrategy._calculate_unexpected_combination(user, menu, db)
        bonus += unexpected_bonus
        
        # 🌈 숨겨진 보석
        hidden_gem_bonus = SurpriseGenerationStrategy._calculate_hidden_gem(user, menu, db)
        bonus += hidden_gem_bonus
        
        # 🎯 완벽한 타이밍
        timing_bonus = SurpriseGenerationStrategy._calculate_perfect_timing(user, menu, db)
        bonus += timing_bonus
        
        return bonus
    
    @staticmethod
    def _calculate_unexpected_combination(user, menu, db):
        """예상치 못은 조합 보너스"""
        user_histories = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .all()
        
        if len(user_histories) >= 3:
            liked_categories = [h.menu.category for h in user_histories if (h.user_rating or 3) >= 4]
            all_categories = set([h.menu.category for h in user_histories])
            rarely_eaten = set(["양식", "아시안", "샐러드", "디저트"]) - all_categories
            
            if menu.category in rarely_eaten and len(liked_categories) > 0:
                return 12  # 예상치 못은 조합 보너스
        
        return 0
    
    @staticmethod
    def _calculate_hidden_gem(user, menu, db):
        """숨겨진 보석 보너스"""
        user_menu_ids = [h.menu_id for h in db.query(models.UserHistory)\
            .filter(models.UserHistory.user_id == user.user_id).all()]
        
        if menu.menu_id not in user_menu_ids:
            menu_detail = db.query(models.MenuDetail)\
                .filter(models.MenuDetail.menu_id == menu.menu_id)\
                .first()
            
            if menu_detail and menu_detail.real_satisfaction_score >= 4.5:
                return 15  # 숨겨진 보석 보너스
        
        return 0
    
    @staticmethod
    def _calculate_perfect_timing(user, menu, db):
        """완벽한 타이밍 보너스"""
        user_histories = db.query(models.UserHistory)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .order_by(models.UserHistory.last_visit_date.desc())\
            .limit(5)\
            .all()
        
        if len(user_histories) >= 2:
            last_meal_time = user_histories[0].last_visit_date
            time_since_last_meal = (datetime.now() - last_meal_time).total_seconds() / 3600
            
            if 4 <= time_since_last_meal <= 8:
                return 8  # 완벽한 타이밍 보너스
        
        return 0

def calculate_recommendation_score(menu, user, daily_inquiry, weather_data, history=None, db=None):
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
    numeric_budget = user.lunch_budget_max  # 기본값은 사용자 프로필
    if daily_inquiry and daily_inquiry.budget_range:
        try:
            raw_budget = daily_inquiry.budget_range
            numeric_budget = int(re.sub(r'[^0-9]', '', str(raw_budget)))
        except (ValueError, TypeError, AttributeError):
            pass  # 기본값 유지

    # 예산 초과 시 즉시 제외 (정규화된 가격 정보 사용)
    if menu.price > numeric_budget:
        return 0 
    
    # 예산 안쪽이면 보너스 (가성비 가점)
    if menu.price <= numeric_budget * 0.8:
        score += 10

    # 2. 식단 제약 필터링 (감점 폭 완화)
    dietary_restriction = None
    if daily_inquiry and daily_inquiry.dietary_restriction:
        dietary_restriction = daily_inquiry.dietary_restriction
    else:
        dietary_restriction = user.dietary_label
        
    if dietary_restriction and dietary_restriction != "뭐든 잘 먹음":
        if dietary_restriction not in (menu.category or "") and \
           dietary_restriction not in (menu.menu_name or ""):
            score -= 20  # -50점에서 -20점으로 완화 (완전 제외보다는 순위 하락 유도)

    # --- [Step 2] 미각 성향 매칭 (Taste Alignment) ---
    
    # 맵기 선호도 (가중치 조정 - 균형화)
    daily_spicy = user.spicy_threshold
    if daily_inquiry and daily_inquiry.spicy_level:
        try:
            daily_spicy = int(re.search(r'\d', daily_inquiry.spicy_level).group())
        except (AttributeError, ValueError, TypeError):
            pass  # 기본값 유지

    spicy_diff = abs(daily_spicy - (details.spicy_level or 3))
    # 완벽 일치 시 +15점, 차이날수록 큰 감점 (20점에서 15점으로 감소)
    spicy_score = (15 - (spicy_diff * 6))
    score += spicy_score
    
    # 카테고리별 추가 가중치 (맵기 1단계 메뉴들 간 차이 만들기)
    category_bonus = 0
    if daily_spicy <= 2:  # 맵기 싫어하는 유저
        if menu.category in ["일식", "분식", "샐러드", "디저트"]:
            category_bonus += 8  # 담백한 카테고리 가점
        elif menu.category in ["한식", "중식", "아시안"]:
            category_bonus -= 5  # 매울 수 있는 카테고리 감점
    elif daily_spicy >= 4:  # 맵기 좋아하는 유저
        if menu.category in ["중식", "아시안", "기타"]:
            category_bonus += 10  # 매운 카테고리 가점
        elif menu.category in ["일식", "분식"]:
            category_bonus -= 3  # 담백한 카테고리 감점
    
    score += category_bonus

    # 간 조절 (가중치 조정)
    salt_map = {"많이 싱겁게": 1, "싱겁게": 2, "보통": 3, "조금 짜게": 4, "많이 짜게": 5}
    user_salt_pref = user.saltiness_preference
    if daily_inquiry and daily_inquiry.salty_level:
        user_salt_pref = salt_map.get(daily_inquiry.salty_level, user.saltiness_preference)
    salt_diff = abs(user_salt_pref - (details.saltiness_level or 3))
    score += (10 - (salt_diff * 3))

    # --- [Step 3] 탐험 성향 반영 ---
    exploration_style = "모험형(새로운 도전)" if user.is_adventurous else "안정형(익숙한 맛)"
    if daily_inquiry and daily_inquiry.exploration_style:
        exploration_style = daily_inquiry.exploration_style
    
    if exploration_style == "모험형(새로운 도전)":
        # 모험형 사용자 신규성 가중치 강화
        if not history or (history.visit_count or 0) == 0:
            score += 12  # 기존 첫 방문 보너스
        
        # 모험형 전용 신규성 보너스
        if history and history.recent_menus:
            # 최근 추천된 메뉴가 아닌 경우 추가 보너스
            if menu.menu_name not in history.recent_menus[:5]:  # 최근 5개 제외
                score += 15  # 새로운 메뉴 발견 보너스
                print(f" {menu.menu_name}: 모험형 신규 메뉴 발견 보너스 (+15)")
            
            # 새로운 카테고리 탐험 보너스
            recent_categories = set()
            for recent_menu in history.recent_menus[:10]:
                # 최근 메뉴의 카테고리 확인 (DB 조회 필요)
                recent_menu_obj = db.query(models.Menu).filter(models.Menu.menu_name == recent_menu).first()
                if recent_menu_obj:
                    recent_categories.add(recent_menu_obj.category)
            
            if menu.category not in recent_categories:
                score += 25  # 새로운 카테고리 탐험 보너스
                print(f" {menu.menu_name}: 모험형 신규 카테고리 탐험 보너스 (+25) - {menu.category}")
        
        # 모험형 사용자 반복 방지 강화
        if history and history.recent_menus:
            # 최근 추천된 메뉴에 대한 강력 페널티
            if menu.menu_name in history.recent_menus[:3]:  # 최근 3개
                score -= 50  # 모험형에게 더 강력한 페널티
                print(f" {menu.menu_name}: 모험형 반복 추천 강력 페널티 (-50)")
            elif menu.menu_name in history.recent_menus[:5]:  # 최근 5개
                score -= 25  # 중간 페널티
                print(f" {menu.menu_name}: 모험형 반복 추천 페널티 (-25)")
                
    elif exploration_style == "안정형(익숙한 맛)":
        if history and (history.visit_count or 0) > 0:
            score += 10

    # --- [Step 4] 실시간 외부 환경 (가점 위주) ---
    current_weather = weather_data.get("weather", "Clear")
    current_temp = weather_data.get("temp", 20)
    is_rainy = weather_data.get("is_rainy", False)
    is_snowy = weather_data.get("is_snowy", False)
    is_hot = weather_data.get("is_hot", False)
    is_cold = weather_data.get("is_cold", False)
    is_clear = weather_data.get("is_clear", False)
    
    # 비/눈 오는 날씨 보너스
    if is_rainy or is_snowy:
        if details.texture == "Crispy": 
            score += 8  
            print(f" {menu.menu_name}: 비/눈 날씨 바삭한 식감 보너스 (+8)")
        if (details.heaviness or 0) >= 4.0: 
            score += 7
            print(f" {menu.menu_name}: 비/눈 날씨 든든한 요리 보너스 (+7)")
        if menu.category in ["한식", "중식"]: 
            score += 5
            print(f" {menu.menu_name}: 비/눈 날씨 따뜻한 요리 보너스 (+5)")
    
    # 더운 날씨 보너스
    if is_hot:
        if details.serving_temperature == "Cold": 
            score += 10
            print(f" {menu.menu_name}: 더운 날씨 시원한 요리 보너스 (+10)")
        if menu.category in ["샐러드", "디저트", "카페"]: 
            score += 8
            print(f" {menu.menu_name}: 더운 날씨 가벼운 요리 보너스 (+8)")
        if (details.spicy_level or 0) <= 2: 
            score += 5
            print(f" {menu.menu_name}: 더운 날씨 맵지 않은 요리 보너스 (+5)")
    
    # 추운 날씨 보너스
    if is_cold:
        if details.serving_temperature == "Hot": 
            score += 10
            print(f" {menu.menu_name}: 추운 날씨 따뜻한 요리 보너스 (+10)")
        if (details.spicy_level or 0) >= 4: 
            score += 8
            print(f" {menu.menu_name}: 추운 날씨 매운 요리 보너스 (+8)")
        if (details.heaviness or 0) >= 4.0: 
            score += 6
            print(f" {menu.menu_name}: 추운 날씨 든든한 요리 보너스 (+6)")
    
    # 맑은 날씨 보너스
    if is_clear:
        if menu.category in ["샐러드", "디저트", "카페"]: 
            score += 5
            print(f" {menu.menu_name}: 맑은 날씨 상쾌한 요리 보너스 (+5)")
        if details.texture == "Fresh": 
            score += 3
            print(f" {menu.menu_name}: 맑은 날씨 신선한 요리 보너스 (+3)")
    
    # 습도 반영
    humidity = weather_data.get("humidity", 50)
    if humidity > 70:
        # 습한 날씨: 가벼운 요리 선호
        if (details.heaviness or 0) <= 3.0: 
            score += 4
            print(f" {menu.menu_name}: 습한 날씨 가벼운 요리 보너스 (+4)")
    elif humidity < 30:
        # 건조한 날씨: 국물 요리 선호
        if menu.category in ["한식", "중식"] and (details.heaviness or 0) >= 3.0: 
            score += 4
            print(f" {menu.menu_name}: 건조한 날씨 국물 요리 보너스 (+4)")
    
    # --- [Step 5] 개선된 과거 피드백 반영 ---
    
    # 기존 히스토리 기반 피드백
    if history:
        if (history.user_rating or 0) >= 4:
            score += 15
        if history.is_revisit_intended is False:
            score -= 30 # 아예 안 먹겠다는 메뉴는 하단으로
        if (history.user_rating or 0) <= 2:
            score -= 25
        if history.last_eaten_category == menu.category:
            score -= 10 # 연속 같은 카테고리 방지
        
        # 연속 같은 메뉴 추천 방지 (완전 제외 + 초강력 페널티)
        if history.recent_menus and menu.menu_name in history.recent_menus:
            # 최근 추천된 메뉴는 완전 제외
            if menu.menu_name == history.recent_menus[0]:  # 직전 추천
                return -1  # 완전 제외
            elif menu.menu_name in history.recent_menus[:3]:  # 최근 3회 이내
                return -1  # 완전 제외
            elif menu.menu_name in history.recent_menus[:5]:  # 최근 5회 이내
                score -= 500  # 초강력 페널티
                print(f" 🚫 {menu.menu_name}: 최근 5회 이내 추천 제외 (-500)")
        
        # 유사 메뉴 식별 및 페널티 (세분화 강화)
        if history.recent_menus:
            similar_menus = _find_similar_menus(menu, history.recent_menus[:3])
            if similar_menus:
                score -= 400  # 유사 메뉴 강력 페널티
                print(f" 🚫 {menu.menu_name}: 유사 메뉴 그룹 제외 (-400) - {', '.join(similar_menus)}")
        
        # 추가 보호: last_eaten_menu 확인
        if history.last_eaten_menu == menu.menu_name:
            score -= 300  # 직전 식사 메뉴 강력 제외
            print(f" 🚫 {menu.menu_name}: 직전 식사 메뉴 강력 제외 (-300)")
    
    # 실시간 피드백 반영 (개선된 부분)
    if db and user:
        # user가 UserProfile 객체인 경우와 UserAccount 객체인 경우 모두 처리
        user_id = getattr(user, 'user_id', None)
        if not user_id and hasattr(user, 'id'):
            user_id = user.id
        
        if user_id:
            latest_feedback = get_latest_feedback(db, user_id, menu.menu_name)
        
        if latest_feedback:
            # 피드백 점수 기반 동적 조정
            feedback_score = latest_feedback.score or 3.0
            
            if feedback_score >= 4.5:          # 매우 만족
                score += 20
                print(f" {menu.menu_name}: 최신 피드백 매우 만족 (+20)")
            elif feedback_score >= 4.0:        # 만족
                score += 12
                print(f" {menu.menu_name}: 최신 피드백 만족 (+12)")
            elif feedback_score >= 3.0:        # 보통
                score += 5
                print(f" {menu.menu_name}: 최신 피드백 보통 (+5)")
            elif feedback_score <= 2.0:        # 불만족
                score -= 15
                print(f" {menu.menu_name}: 최신 피드백 불만족 (-15)")
            elif feedback_score <= 1.0:        # 매우 불만족
                score -= 30
                print(f" {menu.menu_name}: 최신 피드백 매우 불만족 (-30)")
            
            # 피드백 타입별 추가 조정 (개선된 로직)
            feedback_type = latest_feedback.feedback_type.lower()
            
            # 긍정적 피드백
            if feedback_type in FeedbackType.get_positive_types():
                score += 8   # 긍정적 피드백 추가 보너스
            # 부정적 피드백
            elif feedback_type in FeedbackType.get_negative_types():
                score -= 12  # 부정적 피드백 추가 페널티
            # 중립적 피드백
            elif feedback_type in FeedbackType.get_neutral_types():
                score += 2   # 중립적 피드백 미세 조정

    # --- [Step 6] 고도화된 알고리즘 보너스 ---
    
    # 패턴 마이닝 전략
    pattern_bonus = PatternMiningStrategy.calculate_bonus(user, menu, db)
    score += pattern_bonus
    if pattern_bonus > 0:
        print(f" {menu.menu_name}: 패턴 마이닝 보너스 (+{pattern_bonus})")
    
    # 행동 통찰 전략
    behavioral_bonus = BehavioralInsightsStrategy.calculate_bonus(user, menu, db)
    score += behavioral_bonus
    if behavioral_bonus > 0:
        print(f" {menu.menu_name}: 행동 통찰 보너스 (+{behavioral_bonus})")
    
    # 시간 동학 전략
    temporal_bonus = TemporalDynamicsStrategy.calculate_bonus(user, menu, db)
    score += temporal_bonus
    if temporal_bonus > 0:
        print(f" {menu.menu_name}: 시간 동학 보너스 (+{temporal_bonus})")
    
    # 사회적 학습 전략
    social_bonus = SocialLearningStrategy.calculate_bonus(user, menu, db)
    score += social_bonus
    if social_bonus > 0:
        print(f" {menu.menu_name}: 사회적 학습 보너스 (+{social_bonus})")
    
    # 놀라움 생성 전략
    surprise_bonus = SurpriseGenerationStrategy.calculate_bonus(user, menu, db)
    score += surprise_bonus
    if surprise_bonus > 0:
        print(f" {menu.menu_name}: 놀라움 생성 보너스 (+{surprise_bonus})")

    # --- [Step 7] 신뢰도 및 통계 보정 ---
    # 평점 5점 만점 기준 보너스
    rating_bonus = (details.real_satisfaction_score or 3.0) * 2  # 최대 10점
    # 광고 의심도 감점 (영향력 축소)
    ad_penalty = (details.ad_suspicion_index or 0) * 5 # 최대 5점 감점
    score += (rating_bonus - ad_penalty)
    
    # 최종 점수가 너무 튀지 않게 0~100 사이로 보정
    return max(0, min(100, score))

def _find_similar_menus(menu, recent_menus):
    """유사 메뉴 식별 (세분화 강화)"""
    if not recent_menus:
        return []
    
    similar_menus = []
    menu_name = menu.menu_name.lower()
    menu_category = menu.category
    
    # 한식 메뉴 그룹화
    korean_food_groups = {
        '김치류': ['김치찌개', '김치조림', '김치라면', '김치볶음밥'],
        '국밥류': ['돼지국밥', '소머리국밥', '굴국밥', '따로국밥', '콩나물국밥'],
        '볶음밥류': ['게살볶음밥', '제육볶음밥', '낙지볶음밥', '김치볶음밥'],
        '탕류': ['곰탕', '설렁탕', '추어탕', '매운탕', '닭곰탕', '알탕', '해물탕'],
        '면류': ['라면', '짜장라면', '볶음라면', '칼국수', '우동면'],
        '찌개류': ['꽁치조림', '부대찌개', '막찌개', '순대찌개'],
        '기타한식': ['떡볶이', '불고기', '불고기버거', '비빔땡', '잡채']
    }
    
    # 메뉴 그룹 찾기
    menu_group = None
    for group_name, menus in korean_food_groups.items():
        if menu_name in menus:
            menu_group = group_name
            break
    
    if not menu_group:
        return similar_menus
    
    # 같은 그룹의 다른 메뉴 찾기
    for recent_menu in recent_menus:
        recent_menu_lower = recent_menu.lower()
        if recent_menu_lower in korean_food_groups.get(menu_group, []):
            similar_menus.append(recent_menu)

    return similar_menus

def generate_recommendation_reason(menu, weather_data, user, db):
    """메뉴 추천 이유 생성"""
    # 최신 피드백 기반 이유 추가
    latest_feedback = None
    if db and user:
        # user가 UserProfile 객체인 경우와 UserAccount 객체인 경우 모두 처리
        user_id = getattr(user, 'user_id', None)
        if not user_id and hasattr(user, 'id'):
            user_id = user.id

        if user_id:
            latest_feedback = get_latest_feedback(db, user_id, menu.menu_name)

        if latest_feedback:
            feedback_score = latest_feedback.score or 3.0
            
            if feedback_score >= 4.5:
                return f"최근 사용자들이 '{menu.menu_name}'에 매우 만족했습니다! ({feedback_score}점)"
            elif feedback_score >= 4.0:
                return f"'{menu.menu_name}'는 최근 높은 평점을 받았습니다 ({feedback_score}점)"
            elif feedback_score <= 2.0:
                return f"'{menu.menu_name}'는 최근 피드백이 다소 아쉽습니다. 다시 도전해보세요!"
    
    # 개선된 날씨 기반 이유
    weather_desc = weather_data.get("description", "") if weather_data else ""
    is_rainy = weather_data.get("is_rainy", False) if weather_data else False
    is_snowy = weather_data.get("is_snowy", False) if weather_data else False
    is_hot = weather_data.get("is_hot", False) if weather_data else False
    is_cold = weather_data.get("is_cold", False) if weather_data else False
    is_clear = weather_data.get("is_clear", False) if weather_data else False
    
    # 날씨별 추천 이유
    if is_rainy or is_snowy:
        return f"비/눈 오는 날({weather_desc})엔 따끈하고 든든한 {menu.menu_name} 어떠세요?"
    elif is_hot:
        return f"더운 날({weather_desc})엔 시원하고 상쾌한 {menu.menu_name}을 추천해요!"
    elif is_cold:
        return f"추운 날({weather_desc})엔 따뜻한 {menu.menu_name}으로 몸을 녹여보세요!"
    elif is_clear:
        return f"맑은 날({weather_desc})엔 상쾌한 {menu.menu_name}이 딱이에요!"
    
    # 습도 기반 이유
    humidity = weather_data.get("humidity", 50) if weather_data else 50
    if humidity > 70:
        return f"습한 날({humidity}%)엔 가벼운 {menu.menu_name}이 좋겠어요!"
    elif humidity < 30:
        return f"건조한 날({humidity}%)엔 국물 있는 {menu.menu_name}으로 수분 보충!"
    
    # 기본 이유
    if menu.details and menu.details.real_satisfaction_score >= 4.5:
        return f"실제 이용자 평점이 {menu.details.real_satisfaction_score}점으로 매우 검증된 메뉴입니다!"
    
    return f"오늘 날씨({weather_desc})에 어울리는 {menu.category} 메뉴를 추천해요!" if weather_desc else f"{menu.category} 메뉴를 추천해요!"