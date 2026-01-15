from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

# --- [1. 식당 관련 (Store) ] ---

def create_store(db: Session, store: schemas.StoreCreate):
    """식당 기본 정보 및 상세 정보를 함께 저장"""
    db_store = models.Store(
        store_name=store.store_name,
        category=store.category,
        address=store.address,
        phone_number=store.phone_number,
        image_url=store.image_url,
        price_level=store.price_level,
        is_lunch_available=store.is_lunch_available,
        matching_weather=store.matching_weather,
        matching_mood=store.matching_mood,
        suitable_ground_size=store.suitable_ground_size,
        is_quick_meal=store.is_quick_meal
    )
    db.add(db_store)
    db.commit()
    db.refresh(db_store)

    # 상세 데이터(StoreDetail)가 있다면 추가 저장
    if store.details:
        db_detail = models.StoreDetail(
            store_id=db_store.store_id,
            **store.details.dict()
        )
        db.add(db_detail)
        db.commit()
    
    return db_store

def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Store).offset(skip).limit(limit).all()


# --- [2. 사용자 관련 (User) ] ---

def create_user(db: Session, user: schemas.UserCreate):
    """최초 가입 시 사용자의 성향(맵부심, 예산 등) 저장"""
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


# --- [3. 피드백 및 히스토리 관련 (History & Feedback) ] ---

def create_user_history(db: Session, user_id: int, store_id: int, category: str):
    """추천된 식당을 사용자가 '선택'했을 때 방문 기록 생성"""
    # 기존 기록이 있는지 확인
    db_history = db.query(models.UserHistory).filter(
        models.UserHistory.user_id == user_id,
        models.UserHistory.store_id == store_id
    ).first()

    if db_history:
        db_history.visit_count += 1
        db_history.last_visit_date = datetime.utcnow()
    else:
        db_history = models.UserHistory(
            user_id=user_id,
            store_id=store_id,
            last_eaten_category=category
        )
        db.add(db_history)
    
    db.commit()
    db.refresh(db_history)
    return db_history

def update_user_feedback(db: Session, history_id: int, feedback: schemas.FeedbackUpdate):
    """식사 후 별점 및 재방문 의사 업데이트 (알고리즘 학습의 핵심)"""
    db_history = db.query(models.UserHistory).filter(models.UserHistory.history_id == history_id).first()
    if db_history:
        db_history.user_rating = feedback.user_rating
        db_history.is_revisit_intended = feedback.is_revisit_intended
        db_history.feedback_comment = feedback.feedback_comment
        db.commit()
        db.refresh(db_history)
    return db_history

def get_user_history_for_store(db: Session, user_id: int, store_id: int):
    """특정 사용자가 특정 식당에 대해 가졌던 과거 기록 조회 (알고리즘 주입용)"""
    return db.query(models.UserHistory).filter(
        models.UserHistory.user_id == user_id,
        models.UserHistory.store_id == store_id
    ).first()


# --유저랑 상점 삭제 코드 ---

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def delete_store(db: Session, store_id: int):
    db_store = db.query(models.Store).filter(models.Store.store_id == store_id).first()
    if db_store:
        db.delete(db_store)
        db.commit()
    return db_store