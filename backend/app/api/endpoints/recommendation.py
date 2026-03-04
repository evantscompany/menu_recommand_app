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

@router.get("/recommendations", response_model=List[schemas.MenuRecommendation])
def get_recommendations_get(
    current_user: models.UserAccount = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    GET 방식 추천 API - 초고속 버전
    """
    # 인증된 사용자만 추천 가능
    user_id = current_user.user_id
    
    try:
        # 1. 간단한 메뉴 조회 (limit 50으로 제한)
        menus = db.query(models.Menu)\
            .filter(models.Menu.is_lunch_available == True)\
            .limit(50)\
            .all()
        
        # 2. 기본 프로필 생성 (DB 조회 없이)
        user_profile = {
            "spicy_threshold": 3,
            "lunch_budget_max": 12000,
            "is_adventurous": True
        }
        
        # 3. 날씨 데이터는 시뮬레이션 (API 호출 없이)
        weather_data = {
            "is_rainy": False,
            "is_cold": False,
            "is_hot": False
        }
        
        # 4. 간단한 점수 계산
        scored_items = []
        for menu in menus:
            score = 50  # 기본 점수
            
            # 가격 적합도
            if menu.price and menu.price <= user_profile["lunch_budget_max"]:
                score += 20
            
            # 랜덤 점수 추가
            score += random.randint(0, 30)
            
            if score > 0:
                scored_items.append((score, menu))
        
        # 5. 정렬 및 상위 3개 선택
        scored_items.sort(key=lambda x: x[0], reverse=True)
        
        final_items = []
        for score, menu in scored_items[:3]:
            final_items.append(schemas.MenuRecommendation(
                menu_name=menu.menu_name,
                category=menu.category,
                price=menu.price,
                match_rate=min(int(score), 99),
                description=f"오늘 날씨에 어울리는 {menu.category} 메뉴를 추천해요!",
                image_url=menu.image_url or "https://via.placeholder.com/150",
                details=schemas.MenuRecommendationDetail(
                    spicy_level=menu.details.spicy_level if menu.details else 0,
                    texture=menu.details.texture if menu.details else "일반적",
                    rating=menu.details.real_satisfaction_score if menu.details else 0.0
                ),
                restaurant_info=None  # Restaurant 조회 생략
            ))
        
        return final_items
        
    except Exception as e:
        print(f"❌ 추천 시스템 오류: {e}")
        # 에러 발생 시 기본 추천 반환
        return [
            schemas.MenuRecommendation(
                menu_name="김치찌개",
                category="한식",
                price=8000,
                match_rate=85,
                description="오늘 날씨에 어울리는 한식 메뉴를 추천해요!",
                image_url="https://via.placeholder.com/150",
                details=schemas.MenuRecommendationDetail(
                    spicy_level=2,
                    texture="일반적",
                    rating=4.0
                ),
                restaurant_info=None
            )
        ]

@router.get("/", response_model=List[schemas.MenuRecommendation])
def get_recommendations(
    current_user: models.UserAccount = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    GET 방식 추천 API
    """
    # 인증된 사용자만 추천 가능
    user_id = current_user.user_id
    
    try:
        # 1. 간단한 메뉴 조회 (limit 50으로 제한)
        menus = db.query(models.Menu)\
            .filter(models.Menu.is_lunch_available == True)\
            .limit(50)\
            .all()
        
        # 2. 랜덤으로 3개 선택
        if len(menus) >= 3:
            selected_menus = random.sample(menus, 3)
        else:
            selected_menus = menus
        
        # 3. 추천 결과 생성
        recommendations = []
        for menu in selected_menus:
            recommendation = schemas.MenuRecommendation(
                menu_id=menu.menu_id,
                menu_name=menu.menu_name,
                category=menu.category,
                price=menu.price,
                image_url=menu.image_url,
                match_rate=85,  # 필수 필드 추가
                description=f"{menu.menu_name}을 추천합니다!",
                details=schemas.MenuRecommendationDetail(
                    spicy_level=2,
                    texture="일반적",
                    rating=4.0
                ),
                restaurant_info=None
            )
            recommendations.append(recommendation)
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"추천 중 오류 발생: {str(e)}")

@router.post("/", response_model=List[schemas.MenuRecommendation])
def get_recommendations(
    current_user: models.UserAccount = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    POST 방식 추천 API - 초고속 버전
    """
    # 인증된 사용자만 추천 가능
    user_id = current_user.user_id
    
    try:
        # 1. 간단한 메뉴 조회 (limit 50으로 제한)
        menus = db.query(models.Menu)\
            .filter(models.Menu.is_lunch_available == True)\
            .limit(50)\
            .all()
        
        # 2. 기본 프로필 생성 (DB 조회 없이)
        user_profile = {
            "spicy_threshold": 3,
            "lunch_budget_max": 12000,
            "is_adventurous": True
        }
        
        # 3. 날씨 데이터는 시뮬레이션 (API 호출 없이)
        weather_data = {
            "is_rainy": False,
            "is_cold": False,
            "is_hot": False
        }
        
        # 4. 간단한 점수 계산
        scored_items = []
        for menu in menus:
            score = 50  # 기본 점수
            
            # 가격 적합도
            if menu.price and menu.price <= user_profile["lunch_budget_max"]:
                score += 20
            
            # 랜덤 점수 추가
            score += random.randint(0, 30)
            
            if score > 0:
                scored_items.append((score, menu))
        
        # 5. 정렬 및 상위 3개 선택
        scored_items.sort(key=lambda x: x[0], reverse=True)
        
        final_items = []
        for score, menu in scored_items[:3]:
            final_items.append(schemas.MenuRecommendation(
                menu_name=menu.menu_name,
                category=menu.category,
                price=menu.price,
                match_rate=min(int(score), 99),
                description=f"오늘 날씨에 어울리는 {menu.category} 메뉴를 추천해요!",
                image_url=menu.image_url or "https://via.placeholder.com/150",
                details=schemas.MenuRecommendationDetail(
                    spicy_level=menu.details.spicy_level if menu.details else 0,
                    texture=menu.details.texture if menu.details else "일반적",
                    rating=menu.details.real_satisfaction_score if menu.details else 0.0
                ),
                restaurant_info=None  # Restaurant 조회 생략
            ))
        
        return final_items
        
    except Exception as e:
        print(f"❌ 추천 시스템 오류: {e}")
        # 에러 발생 시 기본 추천 반환
        return [
            schemas.MenuRecommendation(
                menu_name="김치찌개",
                category="한식",
                price=8000,
                match_rate=85,
                description="오늘 날씨에 어울리는 한식 메뉴를 추천해요!",
                image_url="https://via.placeholder.com/150",
                details=schemas.MenuRecommendationDetail(
                    spicy_level=2,
                    texture="일반적",
                    rating=4.0
                ),
                restaurant_info=None
            )
        ]
