from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ... import models, schemas, crud
from ...core.algorithm import calculate_recommendation_score

router = APIRouter()

# 임시 날씨 가져오기 함수 (실제로는 OpenWeatherMap 등의 API 연동)
def get_current_weather(city: str):
    # 실제 API 호출 로직이 들어갈 자리
    return {"weather": "Clear", "temp": 25}

@router.post("/", response_model=List[schemas.Store])
def get_recommendations(
    user_id: int, 
    inquiry: schemas.DailyInquiry, 
    db: Session = Depends(get_db)
):
    """
    사용자의 상태와 성향을 분석하여 최적의 식당 3곳을 추천합니다.
    """
    # 1. 사용자 정보 가져오기
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 2. 모든 식당(및 상세정보) 가져오기 
    # (실제 서비스에서는 위치 기반으로 1차 필터링을 수행함)
    stores = db.query(models.Store).all()
    
    # 3. 실시간 날씨 정보 획득
    weather_data = get_current_weather(inquiry.city)

    # 4. 각 식당별 추천 점수 계산
    scored_stores = []
    for store in stores:
        # 해당 사용자가 이 식당에 방문한 적이 있는지 히스토리 조회
        history = crud.get_user_history_for_store(db, user_id=user_id, store_id=store.store_id)
        
        # 알고리즘 가동
        score = calculate_recommendation_score(
            store=store,
            user=user,
            daily_inquiry=inquiry,
            weather_data=weather_data,
            history=history
        )
        
        if score > 0:
            scored_stores.append((score, store))

    # 5. 점수 높은 순으로 정렬 후 상위 3개 추출
    scored_stores.sort(key=lambda x: x[0], reverse=True)
    top_3_stores = [item[1] for item in scored_stores[:3]]

    if not top_3_stores:
        raise HTTPException(status_code=404, detail="조건에 맞는 식당이 없습니다.")

    return top_3_stores

@router.post("/select/{store_id}")
def select_store(user_id: int, store_id: int, db: Session = Depends(get_db)):
    """
    추천된 리스트 중 사용자가 식당을 최종 선택했을 때 호출 (히스토리 생성)
    """
    store = db.query(models.Store).filter(models.Store.store_id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="식당 정보를 찾을 수 없습니다.")
    
    history = crud.create_user_history(db, user_id=user_id, store_id=store_id, category=store.category)
    return {"message": f"{store.store_name} 방문 기록이 생성되었습니다.", "history_id": history.history_id}

@router.patch("/feedback/{history_id}")
def submit_feedback(history_id: int, feedback: schemas.FeedbackUpdate, db: Session = Depends(get_db)):
    """
    식사 후 평점 및 피드백을 남길 때 호출 (알고리즘 학습 데이터 업데이트)
    """
    updated_history = crud.update_user_feedback(db, history_id=history_id, feedback=feedback)
    return {"message": "피드백이 반영되었습니다. 내일은 더 정확한 추천을 해드릴게요!"}