from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random

from ...database import get_db
from ... import models, schemas, crud
from ...core.algorithm import calculate_recommendation_score, generate_recommendation_reason
# 인증 Dependency 가져오기
from ..deps import get_current_user 

router = APIRouter()

# 임시 날씨 가져오기 함수 (기존 유지)
def get_current_weather(city: str):
    return {"weather": "Clear", "temp": 25}

@router.post("/", response_model=List[schemas.MenuRecommendation])
def get_recommendations(
    inquiry: schemas.DailyInquiry,
    # [변경] user_id: int 대신 토큰을 통해 현재 유저 객체를 직접 주입받음
    current_user: models.UserAccount = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    사용자의 상태와 성향을 분석하여 최적의 메뉴 3곳을 추천합니다.
    """
    # 1. 유저 확인 (current_user에 이미 유저 성향 profile이 포함되어 있음)
    user_id = current_user.user_id
    user_profile = current_user.profile # 알고리즘에 전달할 유저 성향 데이터

    if not user_profile:
        raise HTTPException(status_code=404, detail="사용자 성향 프로필을 찾을 수 없습니다.")

    # 2. 기초 데이터 준비 (정규화된 데이터 조회)
    restaurant_menus = db.query(models.RestaurantMenu, models.Menu, models.Restaurant)\
        .join(models.Menu, models.RestaurantMenu.menu_id == models.Menu.menu_id)\
        .join(models.Restaurant, models.RestaurantMenu.restaurant_id == models.Restaurant.restaurant_id)\
        .filter(models.RestaurantMenu.is_available == True)\
        .all()
    
    weather_data = get_current_weather(inquiry.city)

    scored_items = []
    for restaurant_menu, menu, restaurant in restaurant_menus:
        # DB 조회를 유효한 user_id로 수행
        history = crud.get_user_history_for_menu(db, user_id=user_id, menu_id=menu.menu_id)
        
        # 알고리즘 함수 호출 (정규화된 데이터 전달)
        score = calculate_recommendation_score(
            menu=menu,
            restaurant_menu=restaurant_menu,  # 추가: 가격 정보 포함
            user=user_profile,
            daily_inquiry=inquiry,
            weather_data=weather_data,
            history=history
        )
        
        if score >= 0:
            scored_items.append((score, menu, restaurant_menu, restaurant))

    # 3. 점수 순 정렬 및 상위 10개 (로그 및 결과용)
    scored_items.sort(key=lambda x: x[0], reverse=True)
    top_3 = scored_items[:3]
    top_10_for_log = scored_items[:10]

    # --- [VS Code 콘솔 출력 로그 시작] (로직 유지) ---
    print("\n" + "📊 " + "="*65)
    print(f"🔍 [알고리즘 분석 리포트] 유저 ID: {user_id} ({current_user.username})")
    print(f"💬 조건: 예산({inquiry.budget_range}), 맵기({inquiry.spicy_level})")
    print("-" * 67)
    
    if not scored_items:
        print("⚠️ 추천 가능한 메뉴가 없습니다.")
    else:
        for i, (score, menu, restaurant_menu, restaurant) in enumerate(top_10_for_log, 1):
            display_match = min(99, int(score)) if score < 100 else 99
            rank_label = f"⭐ {i}위" if i <= 3 else f"   {i}위"
            print(f"{rank_label} | {display_match}% | {score:6.2f}점 | [{menu.category}] {menu.menu_name[:12]:<12}")
            
    print("="*67 + "\n")
    # --- [VS Code 콘솔 출력 로그 끝] ---

    if not top_3:
        raise HTTPException(status_code=404, detail="조건에 맞는 추천 결과가 없습니다.")

    # 4. 프론트엔드 규격 변환 (식당 정보 포함)
    results = []
    for score, menu, restaurant_menu, restaurant in top_3:
        match_rate = min(99, int(score)) if score < 100 else 99
        spicy = menu.details.spicy_level if menu.details else 0
        texture = menu.details.texture if menu.details else "일반적"
        rating = menu.details.real_satisfaction_score if menu.details else 0.0

        results.append(
            schemas.MenuRecommendation(
                menu_id=menu.menu_id,
                menu_name=menu.menu_name,
                category=menu.category,
                image_url=menu.image_url or "https://via.placeholder.com/150",
                match_rate=match_rate,
                description=generate_recommendation_reason(menu, weather_data),
                details=schemas.MenuRecommendationDetail(
                    spicy_level=spicy,
                    texture=texture,
                    rating=rating
                ),
                # 식당 정보 추가
                restaurant_info={
                    "restaurant_id": restaurant.restaurant_id,
                    "restaurant_name": restaurant.restaurant_name,
                    "address": restaurant.address,
                    "phone_number": restaurant.phone_number,
                    "price": restaurant_menu.price
                }
            )
        )
    return results

@router.post("/select/{menu_id}")
def select_menu(
    menu_id: int, 
    current_user: models.UserAccount = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """메뉴 최종 선택 시 히스토리 생성 (인증 적용)"""
    menu = db.query(models.Menu).filter(models.Menu.menu_id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="메뉴 정보를 찾을 수 없습니다.")
    
    # current_user.user_id 사용
    history = crud.create_user_history(db, user_id=current_user.user_id, menu_id=menu_id, category=menu.category)
    return {"message": f"{menu.menu_name} 선택 완료", "history_id": history.history_id}

@router.post("/feedback/instant", response_model=schemas.FeedbackResponse)
def submit_instant_feedback(
    feedback: schemas.FeedbackCreate, 
    current_user: models.UserAccount = Depends(get_current_user), # 추가 보안용
    db: Session = Depends(get_db)
):
    """추천 리스트에서 메뉴별 즉각 피드백 저장"""
    # 요청 바디의 user_id보다 인증된 유저의 id를 우선시하여 보안 강화
    db_feedback = models.RecommendationFeedback(
        user_id=current_user.user_id,
        menu_name=feedback.menu_name,
        feedback_type=feedback.feedback_type,
        category=feedback.category,
        score=feedback.score
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.patch("/feedback/{history_id}")
def submit_feedback(
    history_id: int, 
    feedback: schemas.FeedbackUpdate, 
    current_user: models.UserAccount = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """식사 후 방문 기록에 대한 상세 피드백 업데이트"""
    # 내 기록인지 확인하는 로직을 추가하면 더 안전합니다.
    updated_history = crud.update_user_feedback(db, history_id=history_id, feedback=feedback)
    if not updated_history:
         raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다.")
    return {"message": "피드백이 반영되었습니다."}