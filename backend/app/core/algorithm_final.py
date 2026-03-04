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
    
    return max(0, min(100, score))

def calculate_user_preference_score(menu, user):
    """사용자 선호도 점수 계산"""
    score = 0
    
    # 맵기 선호도
    if menu.details and user.profile:
        if menu.details.spicy_level is not None and user.profile.spicy_threshold is not None:
            if abs(menu.details.spicy_level - user.profile.spicy_threshold) <= 1:
                score += 15
            elif abs(menu.details.spicy_level - user.profile.spicy_threshold) <= 2:
                score += 8
            elif abs(menu.details.spicy_level - user.profile.spicy_threshold) > 3:
                score -= 10
    
    # 짠맛 선호도
    if menu.details and user.profile:
        if menu.details.saltiness_level is not None and user.profile.saltiness_preference is not None:
            if abs(menu.details.saltiness_level - user.profile.saltiness_preference) <= 1:
                score += 10
            elif abs(menu.details.saltiness_level - user.profile.saltiness_preference) <= 2:
                score += 5
    
    # 예산 적합도
    if menu.price and user.profile and user.profile.lunch_budget_max is not None:
        if menu.price <= user.profile.lunch_budget_max * 0.8:
            score += 20
        elif menu.price <= user.profile.lunch_budget_max:
            score += 10
        else:
            score -= 15
    
    # 모험적 성향
    if user.profile and user.profile.is_adventurous and menu.category in ["양식", "아시안", "샐러드", "디저트"]:
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
    if not menu.price or not user.profile or user.profile.lunch_budget_max is None:
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
    if user and user.profile:
        if menu.price and user.profile.lunch_budget_max is not None:
            if menu.price <= user.profile.lunch_budget_max * 0.7:
                reasons.append(f"예산에 맞는 저렴한 {menu.category} 메뉴예요!")
        
        if menu.details and menu.details.spicy_level is not None and user.profile.spicy_threshold is not None:
            if abs(menu.details.spicy_level - user.profile.spicy_threshold) <= 1:
                reasons.append(f"맵기 선호도에 맞는 {menu.category} 메뉴를 추천해요!")
    
    # 개인화된 추천 이유
    if reasons:
        return " ".join(reasons[:2])  # 최대 2개까지만 조합
    else:
        return f"오늘 날씨에 어울리는 {menu.category} 메뉴를 추천해요!"
