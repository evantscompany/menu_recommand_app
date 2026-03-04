from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random
from datetime import datetime

from ...database_railway import get_db
from ... import models, schemas
from ...core.weather_service import weather_service
from ...core.security import get_current_user

router = APIRouter()

def calculate_simple_score(menu, user_profile, weather_data):
    """간단한 추천 점수 계산"""
    score = 50  # 기본 점수
    
    # 맵기 선호도
    if menu.details and user_profile:
        if menu.details.spicy_level is not None and user_profile.spicy_threshold is not None:
            if abs(menu.details.spicy_level - user_profile.spicy_threshold) <= 1:
                score += 15
            elif abs(menu.details.spicy_level - user_profile.spicy_threshold) <= 2:
                score += 8
    
    # 가격 적합도
    if menu.price and user_profile and user_profile.lunch_budget_max is not None:
        if menu.price <= user_profile.lunch_budget_max * 0.8:
            score += 20
        elif menu.price <= user_profile.lunch_budget_max:
            score += 10
    
    # 날씨 적합도
    if weather_data:
        if weather_data.get('is_rainy') and menu.category in ["한식", "중식", "아시안"]:
            score += 15
        elif weather_data.get('is_cold') and menu.category in ["한식", "중식", "아시안"]:
            score += 10
        elif weather_data.get('is_hot') and menu.category in ["일식", "분식"]:
            score += 8
    
    return max(0, min(100, score))

def generate_simple_reason(menu, weather_data, user_profile):
    """간단한 추천 이유 생성"""
    reasons = []
    
    if weather_data:
        if weather_data.get('is_rainy') and menu.category in ["한식", "중식"]:
            reasons.append(f"비 오는 날에는 따뜻한 {menu.category} 메뉴를 추천해요!")
        elif weather_data.get('is_cold') and menu.category in ["한식", "중식"]:
            reasons.append(f"추운 날씨에는 따뜻한 {menu.category} 메뉴를 추천해요!")
        elif weather_data.get('is_hot') and menu.category in ["일식", "분식"]:
            reasons.append(f"더운 날씨에는 시원한 {menu.category} 메뉴가 좋겠어요!")
    
    if user_profile:
        if menu.price and user_profile.lunch_budget_max is not None:
            if menu.price <= user_profile.lunch_budget_max * 0.7:
                reasons.append(f"예산에 맞는 저렴한 메뉴예요!")
    
    if reasons:
        return " ".join(reasons[:2])
    else:
        return f"오늘 날씨에 어울리는 {menu.category} 메뉴를 추천해요!"

@router.get("/recommendations", response_model=List[schemas.MenuRecommendation])
def get_recommendations_get(
    current_user: models.UserAccount = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    GET 방식 추천 API - 최종 수정 버전
    """
    # 인증된 사용자만 추천 가능
    user_id = current_user.user_id
    
    # 직접 profile 조회 (관계 로드 문제 해결)
    try:
        user_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
        if not user_profile:
            # 기본 프로필 생성
            user_profile = models.UserProfile(
                user_id=user_id,
                dietary_label="none",
                allergies="",
                spicy_threshold=3,
                saltiness_preference=3,
                lunch_budget_max=12000,
                is_adventurous=True
            )
    except Exception as e:
        print(f"⚠️ Profile 조회 오류: {e}")
        user_profile = models.UserProfile(
            user_id=user_id,
            dietary_label="none",
            allergies="",
            spicy_threshold=3,
            saltiness_preference=3,
            lunch_budget_max=12000,
            is_adventurous=True
        )
    
    try:
        # 메뉴 조회
        menus = db.query(models.Menu)\
            .filter(models.Menu.is_lunch_available == True)\
            .all()
        
        # 날씨 데이터 가져오기 (오류 처리 강화)
        try:
            weather_data = weather_service.get_current_weather("Seoul")
        except Exception as e:
            print(f"⚠️ 날씨 데이터 오류: {e}")
            weather_data = None
        
        # 점수 계산
        scored_items = []
        for menu in menus:
            score = calculate_simple_score(menu, user_profile, weather_data)
            if score > 0:
                reason = generate_simple_reason(menu, weather_data, user_profile)
                scored_items.append((score, menu, reason))
        
        # 정렬
        scored_items.sort(key=lambda x: x[0], reverse=True)
        
        # 상위 3개 선택
        final_items = []
        for score, menu, reason in scored_items[:3]:
            # Restaurant 조회 예외 처리
            try:
                restaurant = db.query(models.Restaurant).filter(
                    models.Restaurant.category_1 == menu.category
                ).first()
            except Exception as e:
                print(f"⚠️ Restaurant 조회 오류: {e}")
                restaurant = None

            description = reason or f"오늘 날씨에 어울리는 {menu.category} 메뉴를 추천해요!"
            
            final_items.append(schemas.MenuRecommendation(
                menu_name=menu.menu_name,
                category=menu.category,
                price=menu.price,
                match_rate=min(int(score), 99),
                description=description,
                image_url=menu.image_url,
                details=schemas.MenuRecommendationDetail(
                    spicy_level=menu.details.spicy_level if menu.details else 0,
                    texture=menu.details.texture if menu.details else "일반적",
                    rating=menu.details.real_satisfaction_score if menu.details else 0.0
                ),
                restaurant_info=restaurant
            ))
        
        return final_items
        
    except Exception as e:
        print(f"❌ 추천 시스템 오류: {e}")
        raise HTTPException(status_code=500, detail=f"추천 시스템 오류: {str(e)}")

@router.post("/", response_model=List[schemas.MenuRecommendation])
def get_recommendations(
    current_user: models.UserAccount = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    POST 방식 추천 API - 최종 수정 버전
    """
    # 인증된 사용자만 추천 가능
    user_id = current_user.user_id
    
    # 직접 profile 조회 (관계 로드 문제 해결)
    try:
        user_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
        if not user_profile:
            # 기본 프로필 생성
            user_profile = models.UserProfile(
                user_id=user_id,
                dietary_label="none",
                allergies="",
                spicy_threshold=3,
                saltiness_preference=3,
                lunch_budget_max=12000,
                is_adventurous=True
            )
    except Exception as e:
        print(f"⚠️ Profile 조회 오류: {e}")
        user_profile = models.UserProfile(
            user_id=user_id,
            dietary_label="none",
            allergies="",
            spicy_threshold=3,
            saltiness_preference=3,
            lunch_budget_max=12000,
            is_adventurous=True
        )
    
    try:
        # 메뉴 조회
        menus = db.query(models.Menu)\
            .filter(models.Menu.is_lunch_available == True)\
            .all()
        
        # 날씨 데이터 가져오기 (오류 처리 강화)
        try:
            weather_data = weather_service.get_current_weather("Seoul")
        except Exception as e:
            print(f"⚠️ 날씨 데이터 오류: {e}")
            weather_data = None
        
        # 점수 계산
        scored_items = []
        for menu in menus:
            score = calculate_simple_score(menu, user_profile, weather_data)
            if score > 0:
                reason = generate_simple_reason(menu, weather_data, user_profile)
                scored_items.append((score, menu, reason))
        
        # 정렬
        scored_items.sort(key=lambda x: x[0], reverse=True)
        
        # 상위 3개 선택
        final_items = []
        for score, menu, reason in scored_items[:3]:
            # Restaurant 조회 예외 처리
            try:
                restaurant = db.query(models.Restaurant).filter(
                    models.Restaurant.category_1 == menu.category
                ).first()
            except Exception as e:
                print(f"⚠️ Restaurant 조회 오류: {e}")
                restaurant = None

            description = reason or f"오늘 날씨에 어울리는 {menu.category} 메뉴를 추천해요!"
            
            final_items.append(schemas.MenuRecommendation(
                menu_name=menu.menu_name,
                category=menu.category,
                image_url=menu.image_url or "https://via.placeholder.com/150",
                price=menu.price,
                match_rate=min(int(score), 99),
                description=description,
                details=schemas.MenuRecommendationDetail(
                    spicy_level=menu.details.spicy_level if menu.details else 0,
                    texture=menu.details.texture if menu.details else "일반적",
                    rating=menu.details.real_satisfaction_score if menu.details else 0.0
                ),
                restaurant_info=restaurant
            ))
        
        return final_items
        
    except Exception as e:
        print(f"❌ 추천 시스템 오류: {e}")
        raise HTTPException(status_code=500, detail=f"추천 시스템 오류: {str(e)}")
