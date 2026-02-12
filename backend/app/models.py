from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

# --- [1. 식당 정보] ---
class Restaurant(Base):
    __tablename__ = "restaurants"

    restaurant_id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone_number = Column(String)
    latitude = Column(Float)  # GPS 좌표
    longitude = Column(Float)
    opening_hours = Column(String)  # "09:00-22:00"
    rating = Column(Float, default=0.0)  # 식당 평점
    image_url = Column(String)
    
    # 관계 설정
    menus = relationship("RestaurantMenu", back_populates="restaurant")

# --- [2. 메뉴 정보 (정규화 후) ---
class Menu(Base):
    __tablename__ = "menus"

    menu_id = Column(Integer, primary_key=True, index=True)
    menu_name = Column(String, nullable=False)
    category = Column(String)
    image_url = Column(String)
    
    # 추천 알고리즘용 필드 (유지)
    matching_weather = Column(String)
    matching_mood = Column(String)
    suitable_ground_size = Column(Integer)
    is_quick_meal = Column(Boolean)
    is_lunch_available = Column(Boolean, default=True)

    # 관계 설정
    details = relationship("MenuDetail", back_populates="menu", uselist=False)
    restaurant_menus = relationship("RestaurantMenu", back_populates="menu")
    visits = relationship("UserHistory", back_populates="menu")

# --- [3. 식당-메뉴 연결 테이블] ---
class RestaurantMenu(Base):
    __tablename__ = "restaurant_menus"

    restaurant_menu_id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.menu_id"), nullable=False)
    
    # 해당 식당에서의 메뉴별 정보
    price = Column(Integer, nullable=False)  # 가격
    is_available = Column(Boolean, default=True)  # 판매 여부
    special_note = Column(String)  # "특선 메뉴", "시즌 한정" 등
    
    # 관계 설정
    restaurant = relationship("Restaurant", back_populates="menus")
    menu = relationship("Menu", back_populates="restaurant_menus")

# --- [4. 메뉴 상세 수치] ---
class MenuDetail(Base):
    __tablename__ = "menu_details"

    detail_id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.menu_id"))

    spicy_level = Column(Integer)
    saltiness_level = Column(Integer)
    heaviness = Column(Float)
    serving_temperature = Column(String)
    texture = Column(String)

    revisit_rate = Column(Float)
    avg_waiting_time = Column(Integer)
    ad_suspicion_index = Column(Float)
    real_satisfaction_score = Column(Float)

    menu = relationship("Menu", back_populates="details")

# --- [3. UserAccount (계정/보안용)] ---
class UserAccount(Base):
    __tablename__ = "user_accounts"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    nickname = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="account", uselist=False)
    histories = relationship("UserHistory", back_populates="user")
    feedbacks = relationship("RecommendationFeedback", back_populates="user")

# --- [4. UserProfile (성향 데이터)] ---
class UserProfile(Base):
    __tablename__ = "user_profiles"
    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_accounts.user_id"), unique=True)
    
    dietary_label = Column(String, default="none")
    allergies = Column(String, nullable=True)
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
    last_eaten_category = Column(String)
    
    user_rating = Column(Integer, nullable=True)
    is_revisit_intended = Column(Boolean, default=True)
    feedback_comment = Column(String, nullable=True)

    # 관계 설정
    menu = relationship("Menu", back_populates="visits")
    # [수정] 중복 정의 제거 및 "UserAccount"로 명칭 통일
    user = relationship("UserAccount", back_populates="histories")

# --- [6. 추천 피드백] ---
class RecommendationFeedback(Base):
    __tablename__ = "recommendation_feedbacks"

    feedback_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_accounts.user_id"), index=True)
    menu_name = Column(String, nullable=False)
    feedback_type = Column(String)
    category = Column(String)
    score = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserAccount", back_populates="feedbacks")