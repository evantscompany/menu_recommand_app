from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from .core.security import get_password_hash

# --- [1. 메뉴 관련 (Menu) ] --- (로직 동일)
def create_menu(db: Session, menu: schemas.MenuCreate):
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

    if menu.details:
        db_detail = models.MenuDetail(
            menu_id=db_menu.menu_id,
            **menu.details.dict()
        )
        db.add(db_detail)
        db.commit()
    
    return db_menu

def get_menus(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Menu).offset(skip).limit(limit).all()


# --- [2. 사용자 관련 (UserAccount & Profile) ] ---

def get_user_by_username(db: Session, username: str):
    """로그인 시 아이디로 유저를 찾기 위한 함수 (추가)"""
    return db.query(models.UserAccount).filter(models.UserAccount.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    # 1. 계정 정보 생성 시 비밀번호를 암호화해서 저장!
    db_account = models.UserAccount(
        username=user.username,
        email=user.email,
        nickname=user.nickname,  # ← [추가] 닉네임 필드
        hashed_password=get_password_hash(user.password) # <--- 평문 대신 해시값 저장
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    # 2. 성향 정보 생성 (user_profiles 테이블)
    db_profile = models.UserProfile(
        user_id=db_account.user_id,
        dietary_label=user.dietary_label,
        allergies=user.allergies,
        spicy_threshold=user.spicy_threshold,
        saltiness_preference=user.saltiness_preference,
        lunch_budget_max=user.lunch_budget_max,
        is_adventurous=user.is_adventurous
    )
    db.add(db_profile)
    db.commit()
    
    return db_account

def get_user(db: Session, user_id: int):
    """사용자 ID로 계정과 프로필을 함께 조회"""
    return db.query(models.UserAccount).filter(models.UserAccount.user_id == user_id).first()


# --- [3. 피드백 및 히스토리 관련 (History & Feedback) ] --- (연결 테이블명 수정)

def create_user_history(db: Session, user_id: int, menu_id: int, category: str):
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

# update_user_feedback 로직 동일
def update_user_feedback(db: Session, history_id: int, feedback: schemas.FeedbackUpdate):
    db_history = db.query(models.UserHistory).filter(models.UserHistory.history_id == history_id).first()
    if db_history:
        db_history.user_rating = feedback.user_rating
        db_history.is_revisit_intended = feedback.is_revisit_intended
        db_history.feedback_comment = feedback.feedback_comment
        db.commit()
        db.refresh(db_history)
    return db_history

def get_user_history_for_menu(db: Session, user_id: int, menu_id: int):
    return db.query(models.UserHistory).filter(
        models.UserHistory.user_id == user_id,
        models.UserHistory.menu_id == menu_id
    ).first()


# --- [4. 삭제 관련] ---

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.UserAccount).filter(models.UserAccount.user_id == user_id).first()
    if db_user:
        # UserAccount를 삭제하면 Cascade 설정에 따라 Profile도 같이 삭제되도록 구성 가능
        db.delete(db_user)
        db.commit()
    return db_user

def delete_menu(db: Session, menu_id: int):
    db_menu = db.query(models.Menu).filter(models.Menu.menu_id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
    return db_menu