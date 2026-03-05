from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from .core.security import get_password_hash

# --- [1. 메뉴 관??(Menu) ] ---
# 메뉴???�해�??�이??기반?��?�?조회 기능�??��?
def get_menus(db: Session, skip: int = 0, limit: int = 100):
    """
    ?�록??메뉴 리스?��? 가?�옵?�다.
    메뉴 ?�이?�는 ?�해�??�이�??�이?��? 기반?�로 ?�니??
    """
    return db.query(models.Menu).offset(skip).limit(limit).all()


# --- [2. ?�용??관??(UserAccount & Profile) ] ---

def get_user_by_username(db: Session, username: str):
    """로그?????�이?�로 ?��?�?찾기 ?�한 ?�수 (추�?)"""
    return db.query(models.UserAccount).filter(models.UserAccount.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    # 1. 계정 ?�보 ?�성 ??비�?번호�??�호?�해???�??
    db_account = models.UserAccount(
        username=user.username,
        email=user.email,
        nickname=user.nickname,  # ??[추�?] ?�네???�드
        hashed_password=get_password_hash(user.password) # <--- ?�문 ?�???�시�??�??
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    # 2. ?�향 ?�보 ?�성 (user_profiles ?�이�?
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
    """?�용??ID�?계정�??�로?�을 ?�께 조회"""
    return db.query(models.UserAccount).filter(models.UserAccount.user_id == user_id).first()

def update_user_profile(db: Session, user_id: int, user_update: schemas.UserUpdate):
    """?�용???�로???�데?�트"""
    db_user = db.query(models.UserAccount).filter(models.UserAccount.user_id == user_id).first()
    if not db_user:
        return None
    
    # 계정 ?�보 ?�데?�트
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.nickname is not None:
        db_user.nickname = user_update.nickname
    
    # ?�로???�보 ?�데?�트
    db_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    if db_profile:
        if user_update.dietary_label is not None:
            db_profile.dietary_label = user_update.dietary_label
        if user_update.allergies is not None:
            db_profile.allergies = user_update.allergies
        if user_update.spicy_threshold is not None:
            db_profile.spicy_threshold = user_update.spicy_threshold
        if user_update.saltiness_preference is not None:
            db_profile.saltiness_preference = user_update.saltiness_preference
        if user_update.lunch_budget_max is not None:
            db_profile.lunch_budget_max = user_update.lunch_budget_max
        if user_update.is_adventurous is not None:
            db_profile.is_adventurous = user_update.is_adventurous
    
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db: Session, user_id: int, password_update: schemas.PasswordUpdate):
    """?�용??비�?번호 ?�데?�트"""
    db_user = db.query(models.UserAccount).filter(models.UserAccount.user_id == user_id).first()
    if not db_user:
        return None
    
    # ?�재 비�?번호 ?�인
    from .core.security import verify_password
    if not verify_password(password_update.current_password, db_user.hashed_password):
        return None
    
    # ??비�?번호�??�데?�트
    from .core.security import get_password_hash
    db_user.hashed_password = get_password_hash(password_update.new_password)
    
    db.commit()
    db.refresh(db_user)
    return db_user


# --- [3. ?�드�?�??�스?�리 관??(History & Feedback) ] --- (?�결 ?�이블명 ?�정)

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

# update_user_feedback 로직 ?�일
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


# --- [4. ??�� 관?? ---
# ?�용??계정 ??��

def delete_user(db: Session, user_id: int):
    """?�용??계정 ??��"""
    db_user = db.query(models.UserAccount).filter(models.UserAccount.user_id == user_id).first()
    if db_user:
        # UserAccount�???��?�면 Cascade ?�정???�라 Profile??같이 ??��?�도�?구성 가??
        db.delete(db_user)
        db.commit()
        return True
    return False

def delete_menu(db: Session, menu_id: int):
    db_menu = db.query(models.Menu).filter(models.Menu.menu_id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
    
