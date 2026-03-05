from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from .core.security import get_password_hash

# --- [1. ë©”ë‰´ ê´€??(Menu) ] ---
# ë©”ë‰´???•í•´ì§??°ì´??ê¸°ë°˜?´ë?ë¡?ì¡°íšŒ ê¸°ëŠ¥ë§?? ì?
def get_menus(db: Session, skip: int = 0, limit: int = 100):
    """
    ?±ë¡??ë©”ë‰´ ë¦¬ìŠ¤?¸ë? ê°€?¸ì˜µ?ˆë‹¤.
    ë©”ë‰´ ?°ì´?°ëŠ” ?•í•´ì§??Œì´ë¸??°ì´?°ë? ê¸°ë°˜?¼ë¡œ ?©ë‹ˆ??
    """
    return db.query(models.Menu).offset(skip).limit(limit).all()


# --- [2. ?¬ìš©??ê´€??(UserAccount & Profile) ] ---

def get_user_by_username(db: Session, username: str):
    """ë¡œê·¸?????„ì´?”ë¡œ ? ì?ë¥?ì°¾ê¸° ?„í•œ ?¨ìˆ˜ (ì¶”ê?)"""
    return db.query(models.UserAccount).filter(models.UserAccount.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    # 1. ê³„ì • ?•ë³´ ?ì„± ??ë¹„ë?ë²ˆí˜¸ë¥??”í˜¸?”í•´???€??
    db_account = models.UserAccount(
        username=user.username,
        email=user.email,
        nickname=user.nickname,  # ??[ì¶”ê?] ?‰ë„¤???„ë“œ
        hashed_password=get_password_hash(user.password) # <--- ?‰ë¬¸ ?€???´ì‹œê°??€??
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    # 2. ?±í–¥ ?•ë³´ ?ì„± (user_profiles ?Œì´ë¸?
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
    """?¬ìš©??IDë¡?ê³„ì •ê³??„ë¡œ?„ì„ ?¨ê»˜ ì¡°íšŒ"""
    return db.query(models.UserAccount).filter(models.UserAccount.user_id == user_id).first()

def update_user_profile(db: Session, user_id: int, user_update: schemas.UserUpdate):
    """?¬ìš©???„ë¡œ???…ë°?´íŠ¸"""
    db_user = db.query(models.UserAccount).filter(models.UserAccount.user_id == user_id).first()
    if not db_user:
        return None
    
    # ê³„ì • ?•ë³´ ?…ë°?´íŠ¸
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.nickname is not None:
        db_user.nickname = user_update.nickname
    
    # ?„ë¡œ???•ë³´ ?…ë°?´íŠ¸
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
    """?¬ìš©??ë¹„ë?ë²ˆí˜¸ ?…ë°?´íŠ¸"""
    db_user = db.query(models.UserAccount).filter(models.UserAccount.user_id == user_id).first()
    if not db_user:
        return None
    
    # ?„ì¬ ë¹„ë?ë²ˆí˜¸ ?•ì¸
    from .core.security import verify_password
    if not verify_password(password_update.current_password, db_user.hashed_password):
        return None
    
    # ??ë¹„ë?ë²ˆí˜¸ë¡??…ë°?´íŠ¸
    from .core.security import get_password_hash
    db_user.hashed_password = get_password_hash(password_update.new_password)
    
    db.commit()
    db.refresh(db_user)
    return db_user


# --- [3. ?¼ë“œë°?ë°??ˆìŠ¤? ë¦¬ ê´€??(History & Feedback) ] --- (?°ê²° ?Œì´ë¸”ëª… ?˜ì •)

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

# update_user_feedback ë¡œì§ ?™ì¼
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


# --- [4. ?? œ ê´€?? ---
# ?¬ìš©??ê³„ì • ?? œ

def delete_user(db: Session, user_id: int):
    """?¬ìš©??ê³„ì • ?? œ"""
    db_user = db.query(models.UserAccount).filter(models.UserAccount.user_id == user_id).first()
    if db_user:
        # UserAccountë¥??? œ?˜ë©´ Cascade ?¤ì •???°ë¼ Profile??ê°™ì´ ?? œ?˜ë„ë¡?êµ¬ì„± ê°€??
        db.delete(db_user)
        db.commit()
        return True
    return False

def delete_menu(db: Session, menu_id: int):
    db_menu = db.query(models.Menu).filter(models.Menu.menu_id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
    
