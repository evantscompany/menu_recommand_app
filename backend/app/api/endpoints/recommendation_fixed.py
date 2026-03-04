from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random
from datetime import datetime
import math

from ...database_mysql import get_db
from ... import models, schemas, crud
from ...core.algorithm import calculate_recommendation_score, generate_recommendation_reason
from ...core.weather_service import weather_service
from ..deps import get_current_user 

router = APIRouter()

def add_recommendation_randomness(scored_items):
    """
    추천 결과에 랜덤성 추가하여 동일 메뉴 추천 방지
    """
    random.seed(datetime.now().microsecond)  # 현재 시간의 마이크로초로 시드 설정
    
    randomized_items = []
    for item in scored_items:
        if len(item) == 3:  # (score, menu, reason) 형태
            score, menu, reason = item
        else:  # (score, menu) 형태
            score, menu = item
            reason = None
        
        # 점수의 15%만큼 랜덤 변동 추가 (다양성 강화)
        random_variation = score * 0.15 * (random.random() - 0.5) * 2
        new_score = max(0, min(100, score + random_variation))
        
        if reason:
            randomized_items.append((new_score, menu, reason))
        else:
            randomized_items.append((new_score, menu))
    
    # 다시 정렬
    randomized_items.sort(key=lambda x: x[0], reverse=True)
    return randomized_items

@router.get("/recommendations", response_model=List[schemas.MenuRecommendation])
def get_recommendations_get(
    current_user: models.UserAccount = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    GET 방식 추천 API - 프론트엔드 호환용
    """
    # 인증된 사용자만 추천 가능
    user_id = current_user.user_id
    user_profile = current_user.profile

    if not user_profile:
        raise HTTPException(status_code=404, detail="사용자 성향 프로필을 찾을 수 없습니다. 먼저 프로필을 설정해주세요.")

    try:
        # 메뉴 조회
        menus = db.query(models.Menu)\
            .filter(models.Menu.is_lunch_available == True)\
            .all()
        
        # 실시간 날씨 데이터
        weather_data = weather_service.get_current_weather("Seoul")
        
        # 추천 점수 계산
        scored_items = []
        for menu in menus:
            score = calculate_recommendation_score(
                menu=menu,
                user=user_profile,
                daily_inquiry=None,
                weather_data=weather_data,
                history=None,
                db=db
            )
            if score > 0:
                reason = generate_recommendation_reason(menu, weather_data, user_profile, db)
                scored_items.append((score, menu, reason))
        
        # 랜덤성 추가
        scored_items = add_recommendation_randomness(scored_items)
        
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
                match_rate=min(int(score * 100), 100),
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
    사용자 프로필 기반으로 최적의 메뉴 3곳을 추천합니다.
    """
    # 1. 유저 확인
    user_id = current_user.user_id
    user_profile = current_user.profile

    if not user_profile:
        raise HTTPException(status_code=404, detail="사용자 성향 프로필을 찾을 수 없습니다. 먼저 프로필을 설정해주세요.")

    try:
        # 2. 기초 데이터 준비 (메뉴만 조회)
        menus = db.query(models.Menu)\
            .filter(models.Menu.is_lunch_available == True)\
            .all()
        
        # 실시간 날씨 데이터 가져오기 (서울 기준)
        weather_data = weather_service.get_current_weather("Seoul")

        # 사용자의 최신 히스토리 가져오기
        latest_history = db.query(models.UserHistory)\
            .filter(models.UserHistory.user_id == user_id)\
            .order_by(models.UserHistory.last_visit_date.desc())\
            .first()
        
        scored_items = []
        for menu in menus:
            # DB 조회를 유효한 user_id로 수행
            history = crud.get_user_history_for_menu(db, user_id=user_id, menu_id=menu.menu_id)
            
            # recent_menus 정보는 최신 히스토리에서 가져오기
            if latest_history and (not history or not history.recent_menus):
                history = latest_history
            
            # 개선된 알고리즘 함수 호출
            score = calculate_recommendation_score(
                menu=menu,
                user=user_profile,
                daily_inquiry=None,
                weather_data=weather_data,
                history=history,
                db=db
            )
            
            if score >= 0:
                scored_items.append((score, menu))

        # 3. 점수 순 정렬 및 랜덤성 추가
        scored_items.sort(key=lambda x: x[0], reverse=True)
        scored_items = add_recommendation_randomness(scored_items)
        
        # 상위 3개 선택
        top_3 = scored_items[:3]

        if not top_3:
            raise HTTPException(status_code=404, detail="조건에 맞는 추천 결과가 없습니다.")

        # 4. 프론트엔드 규격 변환
        results = []
        for score, menu in top_3:
            # Restaurant 조회 예외 처리
            try:
                restaurant = db.query(models.Restaurant).filter(
                    models.Restaurant.category_1 == menu.category
                ).first()
            except Exception as e:
                print(f"⚠️ Restaurant 조회 오류: {e}")
                restaurant = None

            match_rate = min(99, int(score)) if score < 100 else 99
            spicy = menu.details.spicy_level if menu.details else 0
            texture = menu.details.texture if menu.details else "일반적"
            rating = menu.details.real_satisfaction_score if menu.details else 0.0

            results.append(
                schemas.MenuRecommendation(
                    menu_name=menu.menu_name,
                    category=menu.category,
                    image_url=menu.image_url or "https://via.placeholder.com/150",
                    price=menu.price,
                    match_rate=match_rate,
                    description=generate_recommendation_reason(menu, weather_data, user=current_user, db=db) or f"오늘 날씨에 어울리는 {menu.category} 메뉴를 추천해요!",
                    details=schemas.MenuRecommendationDetail(
                        spicy_level=spicy,
                        texture=texture,
                        rating=rating
                    ),
                    restaurant_info=restaurant
                )
            )
        return results
        
    except Exception as e:
        print(f"❌ 추천 시스템 오류: {e}")
        raise HTTPException(status_code=500, detail=f"추천 시스템 오류: {str(e)}")
