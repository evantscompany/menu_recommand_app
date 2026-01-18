from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

# --- [1. 식당 상세 정보 스키마] ---
class StoreDetailBase(BaseModel):
    spicy_level: int
    saltiness_level: int
    heaviness: float
    serving_temperature: str
    texture: str
    revisit_rate: float
    avg_waiting_time: int
    ad_suspicion_index: float
    real_satisfaction_score: float

class StoreDetail(StoreDetailBase):
    class Config:
        from_attributes = True


# --- [2. 식당 메인 정보 스키마] ---
class StoreBase(BaseModel):
    store_name: str
    category: str
    address: Optional[str] = None
    phone_number: Optional[str] = None
    image_url: Optional[str] = None
    price_level: int
    is_lunch_available: bool = True
    
    # 상황 태그
    matching_weather: Optional[str] = None
    matching_mood: Optional[str] = None
    suitable_ground_size: int
    is_quick_meal: Optional[bool] = True

class StoreCreate(StoreBase):
    """식당 데이터를 처음 등록할 때 사용하는 규격"""
    details: Optional[StoreDetailBase] = None

class Store(StoreBase):
    """프론트엔드로 데이터를 보낼 때 규격 (ID 포함)"""
    store_id: int
    details: Optional[StoreDetail] = None

    class Config:
        from_attributes = True


# --- [3. 사용자 프로필 스키마] ---
class UserBase(BaseModel):
    username: str
    dietary_label: str = "none"         # 채식 여부 (none, vegan, pesco 등)
    allergies: Optional[str] = None     # 알레르기 (쉼표 구분)
    spicy_threshold: int = 3            # 선호 맵기 (1~5)
    saltiness_preference: int = 3       # 선호 간 (1~5)
    lunch_budget_max: int = 12000       # 최대 예산
    is_adventurous: bool = True         # 도전 선호 여부

class UserCreate(UserBase):
    """회원가입 시 사용하는 규격"""
    pass

class User(UserBase):
    """사용자 정보를 조회할 때 반환하는 규격"""
    user_id: int
    created_at: datetime  # models.py의 created_at과 매칭

    class Config:
        from_attributes = True


# --- [4. 데일리 질문 & 피드백 스키마] ---

class DailyInquiry(BaseModel):
    """매일 앱 접속 시 던지는 3초 질문 답변 규격"""
    # 프로토타입 추가 내용
    dietary_restriction : str #1.18 추가
    spicy_level : str #1.18 추가
    budget_range : str #1.18 추가
    salty_level : str #1.18 추가
    exploration_style : str #1.18 추가
    # condition: str      # normal(평온) or war(전쟁터)
    # social: str         # solo(혼밥) or team(팀원)
    # energy: str         # light(가볍게) or heavy(든든하게)
    city: str = "Seoul" # 실시간 날씨 조회를 위한 지역 정보

class FeedbackUpdate(BaseModel):
    """식사 후 사용자의 피드백을 받을 때 사용하는 규격"""
    user_rating: int             # 사용자가 준 별점 (1~5)
    is_revisit_intended: bool    # 재방문 의사 여부
    feedback_comment: Optional[str] = None # 한 줄 평