from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON, Enum
from sqlalchemy.orm import relationship
from .database_railway import Base
from datetime import datetime
from enum import Enum as PyEnum

# --- [피드백 타입 Enum] ---
class FeedbackType(str, PyEnum):
    EXCELLENT = "excellent"
    GOOD = "good"
    NEUTRAL = "neutral"
    POOR = "poor"
    BAD = "bad"
    DISLIKE = "dislike"
    LOVE = "love"
    LIKE = "like"
    OKAY = "okay"
    
    @classmethod
    def get_positive_types(cls):
        return [cls.EXCELLENT, cls.GOOD, cls.LOVE, cls.LIKE]
    
    @classmethod
    def get_neutral_types(cls):
        return [cls.NEUTRAL, cls.OKAY]
    
    @classmethod
    def get_negative_types(cls):
        return [cls.POOR, cls.BAD, cls.DISLIKE]

# --- [2. 메뉴 정보 (정규화 후) ---
class Menu(Base):
    __tablename__ = "menus"

    menu_id = Column(Integer, primary_key=True, index=True)
    menu_name = Column(String(255), nullable=False)
    category = Column(String(100))
    image_url = Column(String(500))
    price = Column(Integer, default=8000)  # 가격 정보 직접 추가
    
    # 추천 알고리즘용 필드 (유지)
    matching_weather = Column(String(100))
    suitable_ground_size = Column(Integer)
    is_quick_meal = Column(Boolean)
    is_lunch_available = Column(Boolean, default=True)

    # 관계 설정
    details = relationship("MenuDetail", back_populates="menu", uselist=False)
    visits = relationship("UserHistory", back_populates="menu")

# --- [4. 메뉴 상세 수치] ---
class MenuDetail(Base):
    __tablename__ = "menu_details"

    detail_id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.menu_id"))

    spicy_level = Column(Integer)
    saltiness_level = Column(Integer)
    heaviness = Column(Float)
    serving_temperature = Column(String(50))
    texture = Column(String(50))

    revisit_rate = Column(Float)
    avg_waiting_time = Column(Integer)
    ad_suspicion_index = Column(Float)
    real_satisfaction_score = Column(Float)

    menu = relationship("Menu", back_populates="details")

# --- [3. UserAccount (계정/보안용)] ---
class UserAccount(Base):
    __tablename__ = "user_accounts"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nickname = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="account", uselist=False, lazy="joined")
    histories = relationship("UserHistory", back_populates="user", lazy="joined")
    feedbacks = relationship("RecommendationFeedback", back_populates="user", lazy="joined")

# --- [4. UserProfile (성향 데이터)] ---
class UserProfile(Base):
    __tablename__ = "user_profiles"
    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_accounts.user_id"), unique=True)
    
    dietary_label = Column(String(50), default="none")
    allergies = Column(String(255), nullable=True)
    spicy_threshold = Column(Integer, default=3)
    saltiness_preference = Column(Integer, default=3)
    lunch_budget_max = Column(Integer, default=12000)
    is_adventurous = Column(Boolean, default=True)

    account = relationship("UserAccount", back_populates="profile")

# --- [5. 방문 히스토리] ---
class UserHistory(Base):
    __tablename__ = "user_histories"

    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_accounts.user_id"), index=True)
    menu_id = Column(Integer, ForeignKey("menus.menu_id"))

    # 방문 및 피드백 데이터
    last_visit_date = Column(DateTime, default=datetime.utcnow)
    visit_count = Column(Integer, default=1)
    last_eaten_category = Column(String(100))
    last_eaten_menu = Column(String(255))  # 마지막으로 먹은 메뉴 이름
    recent_menus = Column(JSON)  # 최근 추천된 메뉴 목록 (JSON 배열)
    
    user_rating = Column(Integer, nullable=True)
    is_revisit_intended = Column(Boolean, default=True)
    feedback_comment = Column(String(500), nullable=True)

    # 관계 설정
    menu = relationship("Menu", back_populates="visits")
    user = relationship("UserAccount", back_populates="histories")

# --- [6. 추천 피드백] ---
class RecommendationFeedback(Base):
    __tablename__ = "recommendation_feedbacks"

    feedback_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_accounts.user_id"), index=True)
    menu_name = Column(String(255), nullable=False)
    feedback_type = Column(String(50))  # String으로 유지하여 기존 데이터 호환성 확보
    category = Column(String(100))
    score = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserAccount", back_populates="feedbacks")


# 2026-03-03 models.py추가
class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500))
    latitude = Column(Float)
    longitude = Column(Float)
    category_1 = Column(String(100))
    category_2 = Column(String(100))
    distance = Column(Integer)
    walking_time = Column(Integer)