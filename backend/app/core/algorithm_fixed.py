import re
import math
import random
from datetime import datetime, timedelta
from app.database_mysql import SessionLocal
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
            .filter(models.UserHistory.user_id == user.user_id)\
            .filter(models.Menu.category == menu.category)\
            .filter(models.UserHistory.last_visit_date >= datetime.now() - timedelta(days=30))\
            .all()
        
        if len(same_hour_history) >= 3:
            hour_preferences = defaultdict(list)
            for history in same_hour_history:
                hour = history.last_visit_date.hour
                # None 체크 추가
                rating = history.user_rating if history.user_rating is not None else 3
                hour_preferences[hour].append(rating)
            
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
        
        # 같은 요일의 과거 선택 분석
        same_weekday_history = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .filter(models.Menu.category == menu.category)\
            .filter(models.UserHistory.last_visit_date >= datetime.now() - timedelta(days=30))\
            .all()
        
        if len(same_weekday_history) >= 3:
            weekday_preferences = defaultdict(list)
            for history in same_weekday_history:
                weekday = history.last_visit_date.weekday()
                # None 체크 추가
                rating = history.user_rating if history.user_rating is not None else 3
                weekday_preferences[weekday].append(rating)
            
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
        # 사용자의 최근 선택 패턴 분석
        all_history = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .filter(models.UserHistory.last_visit_date >= datetime.now() - timedelta(days=30))\
            .order_by(models.UserHistory.last_visit_date.desc())\
            .limit(20)\
            .all()
        
        if len(all_history) >= 5:
            recent_ratings = []
            previous_ratings = []
            
            for h in all_history:
                # None 체크 추가
                rating = h.user_rating if h.user_rating is not None else 3
                if len(recent_ratings) < 5:
                    recent_ratings.append(rating)
                elif len(previous_ratings) < 5:
                    previous_ratings.append(rating)
            
            recent_avg = sum(recent_ratings) / len(recent_ratings)
            previous_avg = sum(previous_ratings) / len(previous_ratings)
            
            # 성장 추세 보너스
            if recent_avg > previous_avg:
                return 5
        
        return 0

class CollaborativeFilteringStrategy:
    """협업 필터링 전략 - 유사 사용자 기반 추천"""
    
    @staticmethod
    def calculate_bonus(user, menu, db):
        """유사 사용자 기반 보너스 계산"""
        bonus = 0
        
        # 🔄 주기성 패턴 분석
        cyclical_bonus = CollaborativeFilteringStrategy._analyze_cyclical_pattern(user, menu, db)
        bonus += cyclical_bonus
        
        # 📊 예측 가능성 분석
        prediction_bonus = CollaborativeFilteringStrategy._analyze_prediction_potential(user, menu, db)
        bonus += prediction_bonus
        
        # 👥 유사 사용자 선호 분석
        similar_user_bonus = CollaborativeFilteringStrategy._analyze_similar_user_preference(user, menu, db)
        bonus += similar_user_bonus
        
        return bonus
    
    @staticmethod
    def _analyze_cyclical_pattern(user, menu, db):
        """주기성 패턴 분석"""
        current_weekday = datetime.now().weekday()
        
        # 사용자의 요일별 선호 패턴 분석
        user_histories = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .filter(models.UserHistory.last_visit_date >= datetime.now() - timedelta(days=30))\
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
    def _analyze_prediction_potential(user, menu, db):
        """예측 가능성 분석"""
        # 메뉴의 평균 평점과 사용자의 최신 평점 비교
        menu_histories = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(models.Menu.menu_id == menu.menu_id)\
            .filter(models.UserHistory.user_rating.isnot(None))\
            .all()
        
        if len(menu_histories) >= 3:
            ratings = []
            for h in menu_histories:
                # None 체크 추가
                rating = h.user_rating if h.user_rating is not None else 3
                ratings.append(rating)
            
            avg_rating = sum(ratings) / len(ratings)
            
            # 사용자의 최신 히스토리
            latest_history = db.query(models.UserHistory)\
                .filter(models.UserHistory.user_id == user.user_id)\
                .filter(models.UserHistory.user_rating.isnot(None))\
                .all()
            
            if len(latest_history) >= 3:
                user_ratings = []
                for h in latest_history:
                    # None 체크 추가
                    rating = h.user_rating if h.user_rating is not None else 3
                    user_ratings.append(rating)
                
                user_avg_rating = sum(user_ratings) / len(user_ratings)
                
                if menu_detail and menu_detail.real_satisfaction_score >= avg_rating:
                    return 8  # 예측 가능성 보너스
        
        return 0
    
    @staticmethod
    def _analyze_similar_user_preference(user, menu, db):
        """유사 사용자 선호 분석"""
        # 비슷한 성향의 사용자 찾기
        similar_users = db.query(models.UserAccount)\
            .join(models.UserProfile)\
            .filter(models.UserProfile.spicy_threshold.between(
                user.profile.spicy_threshold - 1, 
                user.profile.spicy_threshold + 1
            ))\
            .filter(models.UserProfile.lunch_budget_max.between(
                user.profile.lunch_budget_max - 2000, 
                user.profile.lunch_budget_max + 2000
            ))\
            .filter(models.UserAccount.user_id != user.user_id)\
            .limit(10)\
            .all()
        
        if similar_users:
            similar_user_ids = [u.user_id for u in similar_users]
            similar_user_histories = db.query(models.UserHistory)\
                .filter(models.UserHistory.user_id.in_(similar_user_ids))\
                .all()
            
            if similar_user_histories:
                avg_rating = sum(h.user_rating or 3 for h in similar_user_histories) / len(similar_user_histories)
                if avg_rating >= 4.0:
                    return 7  # 유사 사용자 선호 보너스
        
        return 0

class ContentBasedStrategy:
    """콘텐츠 기반 전략 - 메뉴 속성 기반 추천"""
    
    @staticmethod
    def calculate_bonus(user, menu, db):
        """콘텐츠 기반 보너스 계산"""
        bonus = 0
        
        # 🕐 시간대별 선호도
        time_bonus = ContentBasedStrategy._analyze_time_preference(user, menu, db)
        bonus += time_bonus
        
        # 🔄 주기성 선호도
        weekday_bonus = ContentBasedStrategy._analyze_weekday_preference(user, menu, db)
        bonus += weekday_bonus
        
        # 📈 성장 패턴
        growth_bonus = ContentBasedStrategy._analyze_growth_pattern(user, menu, db)
        bonus += growth_bonus
        
        return bonus
    
    @staticmethod
    def _analyze_time_preference(user, menu, db):
        """시간대별 선호도 분석"""
        current_hour = datetime.now().hour
        
        # 사용자의 시간대별 선호 패턴
        user_histories = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .filter(models.UserHistory.last_visit_date >= datetime.now() - timedelta(days=30))\
            .all()
        
        if len(user_histories) >= 4:
            weekday_patterns = defaultdict(list)
            for history in user_histories:
                weekday = history.last_visit_date.weekday()
                # None 체크 추가
                rating = history.user_rating if history.user_rating is not None else 3
                weekday_patterns[weekday].append(rating)
            
            current_weekday = datetime.now().weekday()
            current_pattern = weekday_patterns.get(current_weekday, [])
            
            if len(current_pattern) >= 2:
                most_common_category = Counter(current_pattern).most_common(1)[0][0]
                if menu.category == most_common_category:
                    return 8  # 주기성 패턴 보너스
        
        return 0
    
    @staticmethod
    def _analyze_weekday_preference(user, menu, db):
        """요일별 선호도 분석"""
        current_month = datetime.now().month
        
        # 사용자의 계절별 선호 패턴
        seasonal_histories = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .filter(models.UserHistory.last_visit_date >= datetime.now() - timedelta(days=90))\
            .all()
        
        if len(seasonal_histories) >= 3:
            seasonal_preferences = defaultdict(list)
            for history in seasonal_histories:
                month = history.last_visit_date.month
                # None 체크 추가
                rating = history.user_rating if history.user_rating is not None else 3
                seasonal_preferences[month].append(rating)
            
            current_month_ratings = seasonal_preferences.get(current_month, [3])
            avg_rating = sum(current_month_ratings) / len(current_month_ratings)
            
            if avg_rating >= 4.0:
                return 6  # 계절성 선호 보너스
        
        return 0
    
    @staticmethod
    def _analyze_growth_pattern(user, menu, db):
        """성장 패턴 분석"""
        # 최근 7일간의 인기도 트렌드 분석
        recent_histories = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(
                models.UserHistory.last_visit_date >= datetime.now() - timedelta(days=7),
                models.Menu.menu_id == menu.menu_id
            )\
            .all()
        
        if recent_histories:
            recent_popularity = len(recent_histories)
            
            # 전체 기간 동안의 인기도
            total_histories = db.query(models.UserHistory)\
                .join(models.Menu)\
                .filter(models.Menu.menu_id == menu.menu_id)\
                .all()
            
            if total_histories > 0:
                popularity_ratio = recent_popularity / len(total_histories)
                if popularity_ratio >= 0.3:
                    return 5  # 인기도 트렌드 보너스
        
        return 0

class TrendAnalysisStrategy:
    """트렌드 분석 전략 - 시간에 따른 선호도 변화 분석"""
    
    @staticmethod
    def calculate_bonus(user, menu, db):
        """트렌드 기반 보너스 계산"""
        bonus = 0
        
        # 🌟 전문가 추천 보너스
        expert_bonus = TrendAnalysisStrategy._analyze_expert_recommendation(user, menu, db)
        bonus += expert_bonus
        
        # 🎯 숨겨진 보석 보너스
        hidden_gem_bonus = TrendAnalysisStrategy._analyze_hidden_gem(user, menu, db)
        bonus += hidden_gem_bonus
        
        # ⏰ 시간 기반 선호도
        time_preference_bonus = TrendAnalysisStrategy._analyze_time_based_preference(user, menu, db)
        bonus += time_preference_bonus
        
        return bonus
    
    @staticmethod
    def _analyze_expert_recommendation(user, menu, db):
        """전문가 추천 보너스"""
        # 메뉴의 평균 평점이 높은 메뉴 우선
        menu_detail = db.query(models.MenuDetail)\
            .filter(models.MenuDetail.menu_id == menu.menu_id)\
            .first()
        
        if menu_detail and menu_detail.real_satisfaction_score >= 4.5:
            return 6  # 전문가 추천 보너스
        
        return 0
    
    @staticmethod
    def _analyze_hidden_gem(user, menu, db):
        """숨겨진 보석 보너스"""
        # 사용자가 자주 먹지 않지만 평점이 높은 메뉴
        user_histories = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .all()
        
        if len(user_histories) >= 3:
            liked_categories = []
            all_categories = set()
            
            for h in user_histories:
                # None 체크 추가
                rating = h.user_rating if h.user_rating is not None else 3
                if rating >= 4:
                    liked_categories.append(h.menu.category)
                all_categories.add(h.menu.category)
            
            rarely_eaten = set(["양식", "아시안", "샐러드", "디저트"]) - all_categories
            
            if menu.category in rarely_eaten:
                menu_detail = db.query(models.MenuDetail)\
                    .filter(models.MenuDetail.menu_id == menu.menu_id)\
                    .first()
                
                if menu_detail and menu_detail.real_satisfaction_score >= 4.5:
                    return 15  # 숨겨진 보석 보너스
        
        return 0
    
    @staticmethod
    def _analyze_time_based_preference(user, menu, db):
        """시간 기반 선호도 분석"""
        # 마지막 식사 시간 기반 선호도
        user_histories = db.query(models.UserHistory)\
            .join(models.Menu)\
            .filter(models.UserHistory.user_id == user.user_id)\
            .order_by(models.UserHistory.last_visit_date.desc())\
            .limit(5)\
            .all()
        
        if len(user_histories) >= 2:
            last_meal_time = user_histories[0].last_visit_date
            time_since_last_meal = (datetime.now() - last_meal_time).total_seconds() / 3600
            
            # 너무 자주 먹은 메뉴는 페널티
            if time_since_last_meal < 4:
                return -3
        
        return 0

def calculate_recommendation_score(menu, user, daily_inquiry, weather_data, history, db):
    """
    고도화된 추천 점수 계산 알고리즘
    """
    score = 50  # 기본 점수
    
    # 1. 기본 사용자 선호도 점수
    score += calculate_user_preference_score(menu, user)
    
    # 2. 날씨 적합도 점수
    score += calculate_weather_score(menu, weather_data)
    
    # 3. 가격 적합도 점수
    score += calculate_price_score(menu, user)
    
    # 4. 식사 기록 기반 점수
    if history:
        score += calculate_history_score(menu, history)
    
    # 5. 🧠 고도화된 전략 점수
    pattern_bonus = PatternMiningStrategy.calculate_bonus(user, menu, db)
    collaborative_bonus = CollaborativeFilteringStrategy.calculate_bonus(user, menu, db)
    content_bonus = ContentBasedStrategy.calculate_bonus(user, menu, db)
    trend_bonus = TrendAnalysisStrategy.calculate_bonus(user, menu, db)
    
    score += pattern_bonus + collaborative_bonus + content_bonus + trend_bonus
    
    return max(0, min(100, score))

def calculate_user_preference_score(menu, user):
    """사용자 선호도 점수 계산"""
    score = 0
    
    # 맵기 선호도
    if menu.details:
        if menu.details.spicy_level is not None and user.profile.spicy_threshold is not None:
            if abs(menu.details.spicy_level - user.profile.spicy_threshold) <= 1:
                score += 15
            elif abs(menu.details.spicy_level - user.profile.spicy_threshold) <= 2:
                score += 8
            elif abs(menu.details.spicy_level - user.profile.spicy_threshold) > 3:
                score -= 10
    
    # 짠맛 선호도
    if menu.details and menu.details.saltiness_level is not None and user.profile.saltiness_preference is not None:
        if abs(menu.details.saltiness_level - user.profile.saltiness_preference) <= 1:
            score += 10
        elif abs(menu.details.saltiness_level - user.profile.saltiness_preference) <= 2:
            score += 5
    
    # 예산 적합도
    if menu.price is not None and user.profile.lunch_budget_max is not None:
        if menu.price <= user.profile.lunch_budget_max * 0.8:
            score += 20
        elif menu.price <= user.profile.lunch_budget_max:
            score += 10
        else:
            score -= 15
    
    # 모험적 성향
    if user.profile.is_adventurous and menu.category in ["양식", "아시안", "샐러드", "디저트"]:
        score += 12
    
    return score

def calculate_weather_score(menu, weather_data):
    """날씨 적합도 점수 계산"""
    if not weather_data:
        return 0
    
    score = 0
    
    # 날씨 조건에 따른 점수
    if weather_data.get('is_rainy') and menu.category in ["한식", "중식", "아시안"]:
        score += 15  # 비 오는 날 따뜻한 요리 보너스
    
    if weather_data.get('is_cold') and menu.category in ["한식", "중식", "아시안"]:
        score += 10  # 추운 날 따뜻한 요리 보너스
    
    if weather_data.get('is_hot') and menu.category in ["일식", "분식"]:
        score += 8  # 더운 날 시원한 요리 보너스
    
    if weather_data.get('is_clear') and menu.category in ["양식", "샐러드"]:
        score += 5  # 맑은 날 경식 메뉴 보너스
    
    return score

def calculate_price_score(menu, user):
    """가격 적합도 점수 계산"""
    if not menu.price or not user.profile.lunch_budget_max:
        return 0
    
    score = 0
    
    # 예산 대비 가격 비율
    price_ratio = menu.price / user.profile.lunch_budget_max
    
    if price_ratio <= 0.6:
        score += 15  # 매우 저렴
    elif price_ratio <= 0.8:
        score += 10  # 저렴
    elif price_ratio <= 1.0:
        score += 5  # 적정
    else:
        score -= 10  # 비쌈
    
    return score

def calculate_history_score(menu, history):
    """식사 기록 기반 점수 계산"""
    if not history:
        return 0
    
    score = 0
    
    # 방문 횟수 보너스
    if history.visit_count and history.visit_count > 1:
        score += min(history.visit_count * 2, 15)
    
    # 재방문 의향 보너스
    if history.is_revisit_intended:
        score += 10
    
    # 사용자 평점 보너스
    if history.user_rating is not None:
        if history.user_rating >= 4:
            score += 15
        elif history.user_rating >= 3:
            score += 8
    
    return score

def generate_recommendation_reason(menu, weather_data, user, db):
    """
    개인화된 추천 이유 생성
    """
    reasons = []
    
    # 날씨 기반 추천 이유
    if weather_data:
        if weather_data.get('is_rainy') and menu.category in ["한식", "중식"]:
            reasons.append(f"비/눈 오는 날({weather_data.get('description', '비 오는 날')})엔 따끈하고 든든한 {menu.category} 요리 어떠세요?")
        elif weather_data.get('is_cold') and menu.category in ["한식", "중식"]:
            reasons.append(f"추운 날씨에는 따뜻한 {menu.category} 메뉴를 추천해요!")
        elif weather_data.get('is_hot') and menu.category in ["일식", "분식"]:
            reasons.append(f"더운 날씨에는 시원한 {menu.category} 메뉴가 좋겠어요!")
    
    # 사용자 선호도 기반 추천 이유
    if user.profile:
        if menu.price and user.profile.lunch_budget_max:
            if menu.price <= user.profile.lunch_budget_max * 0.7:
                reasons.append(f"예산에 맞는 저렴한 {menu.category} 메뉴예요!")
        
        if menu.details and menu.details.spicy_level is not None and user.profile.spicy_threshold is not None:
            if abs(menu.details.spicy_level - user.profile.spicy_threshold) <= 1:
                reasons.append(f"맵기 선호도에 맞는 {menu.category} 메뉴를 추천해요!")
    
    # 개인화된 추천 이우
    if reasons:
        return " ".join(reasons[:2])  # 최대 2개까지만 조합
    else:
        return f"오늘 날씨에 어울리는 {menu.category} 메뉴를 추천해요!"
