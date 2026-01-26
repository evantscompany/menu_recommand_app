from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

# --- [1. 메뉴 상세 정보 스키마] ---
class MenuDetailBase(BaseModel):
    spicy_level: int
    saltiness_level: int
    heaviness: float
    serving_temperature: str
    texture: str
    revisit_rate: float
    avg_waiting_time: int
    ad_suspicion_index: float
    real_satisfaction_score: float

class MenuDetail(MenuDetailBase):
    class Config:
        from_attributes = True


# --- [2. 메뉴 메인 정보 스키마] ---
class MenuBase(BaseModel):
    menu_name: str
    category: str
    address: Optional[str] = None
    phone_number: Optional[str] = None
    image_url: Optional[str] = None
    price_level: int
    is_lunch_available: bool = True
    
    # [수정] 아래 필드들을 Optional로 변경하여 에러 방지
    matching_weather: Optional[str] = None
    matching_mood: Optional[str] = None
    suitable_ground_size: Optional[int] = None # int -> Optional[int]
    is_quick_meal: Optional[bool] = True

class MenuCreate(MenuBase):
    """메뉴 데이터를 처음 등록할 때 사용하는 규격"""
    details: Optional[MenuDetailBase] = None

class Menu(MenuBase):
    """프론트엔드로 기본 데이터를 보낼 때 규격 (ID 포함)"""
    menu_id: int
    details: Optional[MenuDetail] = None

    class Config:
        from_attributes = True


# --- [3. 사용자 프로필 스키마] ---
class UserBase(BaseModel):
    username: str
    dietary_label: str = "none"         
    allergies: Optional[str] = None     
    spicy_threshold: int = 3            
    saltiness_preference: int = 3       
    lunch_budget_max: int = 12000       
    is_adventurous: bool = True         

class UserCreate(UserBase):
    """회원가입 시 사용하는 규격"""
    pass

class User(UserBase):
    """사용자 정보를 조회할 때 반환하는 규격"""
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- [4. 질문 및 피드백 스키마] ---

class DailyInquiry(BaseModel):
    """매일 앱 접속 시 던지는 질문 답변 규격"""
    dietary_restriction : str
    spicy_level : str
    budget_range : str
    salty_level : str
    exploration_style : str
    city: str = "Seoul"

class FeedbackCreate(BaseModel):
    """추천 메뉴 카드에 대해 즉시 남기는 피드백"""
    user_id: int
    menu_name: str
    feedback_type: str       
    category: str
    score: float             

class FeedbackResponse(FeedbackCreate):
    feedback_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FeedbackUpdate(BaseModel):
    """식사 후 방문 기록(History) 업데이트용"""
    user_rating: int 
    is_revisit_intended: bool
    feedback_comment: Optional[str] = None


# --- [5. 최종 추천 결과 전용 스키마] ---

class MenuRecommendationDetail(BaseModel):
    """프론트엔드 이미지 카드 하단 상세 데이터"""
    spicy_level: int
    texture: str
    rating: float

class MenuRecommendation(BaseModel):
    """프론트엔드 이미지 요구사항을 반영한 최종 응답 규격"""
    menu_id: int
    menu_name: str
    category: str
    image_url: Optional[str] = None
    match_rate: int
    description: str
    details: MenuRecommendationDetail

    class Config:
        from_attributes = True