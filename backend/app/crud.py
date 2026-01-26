from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

# --- [1. 메뉴 관련 (Menu) ] ---

def create_menu(db: Session, menu: schemas.MenuCreate):
    """메뉴 기본 정보 및 상세 정보를 함께 저장 (Store -> Menu)"""
    db_menu = models.Menu(
        menu_name=menu.menu_name,
        category=menu.category,
        address=menu.address,
        phone_number=menu.phone_number,
        image_url=menu.image_url,
        price_level=menu.price_level,
        is_lunch_available=menu.is_lunch_available,
        matching_weather=menu.matching_weather,
        matching_mood=menu.matching_mood,
        suitable_ground_size=menu.suitable_ground_size,
        is_quick_meal=menu.is_quick_meal
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)

    # 상세 데이터(MenuDetail)가 있다면 추가 저장
    if menu.details:
        db_detail = models.MenuDetail(
            menu_id=db_menu.menu_id,
            **menu.details.dict()
        )
        db.add(db_detail)
        db.commit()
    
    return db_menu

def get_menus(db: Session, skip: int = 0, limit: int = 100):
    """모든 메뉴 조회"""
    return db.query(models.Menu).offset(skip).limit(limit).all()


# --- [2. 사용자 관련 (User) ] ---

def create_user(db: Session, user: schemas.UserCreate):
    """최초 가입 시 사용자의 성향 저장"""
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    """사용자 ID로 조회"""
    return db.query(models.User).filter(models.User.user_id == user_id).first()


# --- [3. 피드백 및 히스토리 관련 (History & Feedback) ] ---

def create_user_history(db: Session, user_id: int, menu_id: int, category: str):
    """추천된 메뉴를 사용자가 '선택'했을 때 방문 기록 생성"""
    # 기존 기록이 있는지 확인
    db_history = db.query(models.UserHistory).filter(
        models.UserHistory.user_id == user_id,
        models.UserHistory.menu_id == menu_id
    ).first()

    if db_history:
        db_history.visit_count += 1
        db_history.last_visit_date = datetime.utcnow()
    else:
        db_history = models.UserHistory(
            user_id=user_id,
            menu_id=menu_id,
            last_eaten_category=category
        )
        db.add(db_history)
    
    db.commit()
    db.refresh(db_history)
    return db_history

def update_user_feedback(db: Session, history_id: int, feedback: schemas.FeedbackUpdate):
    """식사 후 별점 및 재방문 의사 업데이트"""
    db_history = db.query(models.UserHistory).filter(models.UserHistory.history_id == history_id).first()
    if db_history:
        db_history.user_rating = feedback.user_rating
        db_history.is_revisit_intended = feedback.is_revisit_intended
        db_history.feedback_comment = feedback.feedback_comment
        db.commit()
        db.refresh(db_history)
    return db_history

def get_user_history_for_menu(db: Session, user_id: int, menu_id: int):
    """특정 사용자가 특정 메뉴에 대해 가졌던 과거 기록 조회 (알고리즘 주입용)"""
    return db.query(models.UserHistory).filter(
        models.UserHistory.user_id == user_id,
        models.UserHistory.menu_id == menu_id
    ).first()


# --- [4. 삭제 관련] ---

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def delete_menu(db: Session, menu_id: int):
    """식당(메뉴) 삭제"""
    db_menu = db.query(models.Menu).filter(models.Menu.menu_id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
    return db_menu