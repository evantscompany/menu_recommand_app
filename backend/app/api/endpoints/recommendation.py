from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random

from ...database import get_db
from ... import models, schemas, crud
from ...core.algorithm import calculate_recommendation_score, generate_recommendation_reason

router = APIRouter()

# 임시 날씨 가져오기 함수 (기존 유지)
def get_current_weather(city: str):
    return {"weather": "Clear", "temp": 25}

@router.post("/", response_model=List[schemas.MenuRecommendation])
def get_recommendations(
    inquiry: schemas.DailyInquiry,
    user_id: int, 
    db: Session = Depends(get_db)
):
    """
    사용자의 상태와 성향을 분석하여 최적의 메뉴 3곳을 추천합니다.
    """
    # 1. 유저 확인
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 2. 기초 데이터 준비
    menus = db.query(models.Menu).all()
    weather_data = get_current_weather(inquiry.city)

    scored_items = []
    for menu in menus:
        history = crud.get_user_history_for_menu(db, user_id=user_id, menu_id=menu.menu_id)
        
        score = calculate_recommendation_score(
            menu=menu,
            user=user,
            daily_inquiry=inquiry,
            weather_data=weather_data,
            history=history
        )
        
        # 필터링 대상(-1) 제외
        if score >= 0:
            scored_items.append((score, menu))

    # 3. 점수 순 정렬 및 상위 10개 (로그 및 결과용)
    scored_items.sort(key=lambda x: x[0], reverse=True)
    top_3 = scored_items[:3]
    top_10_for_log = scored_items[:10]

    # --- [VS Code 콘솔 출력 로그 시작] ---
    print("\n" + "📊 " + "="*65)
    print(f"🔍 [알고리즘 분석 리포트] 유저 ID: {user_id}")
    print(f"💬 조건: 예산({inquiry.budget_range}), 맵기({inquiry.spicy_level})")
    print("-" * 67)
    
    if not scored_items:
        print("⚠️ 추천 가능한 메뉴가 없습니다.")
    else:
        for i, (score, menu) in enumerate(top_10_for_log, 1):
            # 알고리즘이 100점 만점 기반이므로 score를 그대로 정수화하여 사용
            display_match = min(99, int(score)) if score < 100 else 99
            
            rank_label = f"⭐ {i}위" if i <= 3 else f"   {i}위"
            print(f"{rank_label} | {display_match}% | {score:6.2f}점 | [{menu.category}] {menu.menu_name[:12]:<12}")
            
    print("="*67 + "\n")
    # --- [VS Code 콘솔 출력 로그 끝] ---

    if not top_3:
        raise HTTPException(status_code=404, detail="조건에 맞는 추천 결과가 없습니다.")

    # 4. 프론트엔드 규격(MenuRecommendation)에 맞게 변환
    results = []
    for score, menu in top_3:
        # 매칭율 계산: 알고리즘의 100점 만점 점수를 그대로 반영
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
                )
            )
        )

    return results

@router.post("/select/{menu_id}")
def select_menu(user_id: int, menu_id: int, db: Session = Depends(get_db)):
    """메뉴 최종 선택 시 히스토리 생성"""
    menu = db.query(models.Menu).filter(models.Menu.menu_id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="메뉴 정보를 찾을 수 없습니다.")
    
    history = crud.create_user_history(db, user_id=user_id, menu_id=menu_id, category=menu.category)
    return {"message": f"{menu.menu_name} 선택 완료", "history_id": history.history_id}

@router.post("/feedback/instant", response_model=schemas.FeedbackResponse)
def submit_instant_feedback(
    feedback: schemas.FeedbackCreate, 
    db: Session = Depends(get_db)
):
    """추천 리스트에서 메뉴별 즉각 피드백 저장"""
    db_feedback = models.RecommendationFeedback(
        user_id=feedback.user_id,
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
def submit_feedback(history_id: int, feedback: schemas.FeedbackUpdate, db: Session = Depends(get_db)):
    """식사 후 방문 기록에 대한 상세 피드백 업데이트"""
    updated_history = crud.update_user_feedback(db, history_id=history_id, feedback=feedback)
    if not updated_history:
         raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다.")
    return {"message": "피드백이 반영되었습니다."}