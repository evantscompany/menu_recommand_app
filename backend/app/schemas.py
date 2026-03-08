from pydantic import BaseModel, HttpUrl, EmailStr
from typing import List, Optional
from datetime import datetime

# --- [1. 메뉴 상세 정보 스키마] --- (기존 유지)
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


# --- [4. 메뉴 메인 정보 스키마] --- (정규화 후)
class MenuBase(BaseModel):
    menu_name: str
    category: str
    image_url: Optional[str] = None
    price: int = 8000
    is_lunch_available: bool = True
    matching_weather: Optional[str] = None
    matching_mood: Optional[str] = None
    suitable_ground_size: Optional[int] = None 
    is_quick_meal: Optional[bool] = True

class MenuCreate(MenuBase):
    details: Optional[MenuDetailBase] = None

class Menu(MenuBase):
    menu_id: int
    details: Optional[MenuDetail] = None

    class Config:
        from_attributes = True


# --- [5. 사용자 관련 스키마] --- (필드 추가 및 분리)

class UserBase(BaseModel):
    username: str
    email: EmailStr  # [추가] 이메일 필드
    nickname: str    # [추가] 닉네임 필드

class UserProfileBase(BaseModel):
    """유저 성향 데이터 (기존 UserBase 로직 유지)"""
    dietary_label: str = "none"         
    allergies: Optional[str] = None     
    spicy_threshold: int = 3            
    saltiness_preference: int = 3       
    lunch_budget_max: int = 12000       
    is_adventurous: bool = True         

class UserCreate(UserBase, UserProfileBase):
    """회원가입 시 사용하는 규격 (비밀번호 추가)"""
    password: str

class UserLogin(BaseModel):
    """로그인 전용 스키마 (추가)"""
    username: str
    password: str

class User(UserBase):
    """사용자 조회용 규격"""
    user_id: int
    created_at: datetime
    profile: Optional[UserProfileBase] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """사용자 프로필 수정용 규격"""
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    dietary_label: Optional[str] = None
    allergies: Optional[str] = None
    spicy_threshold: Optional[int] = None
    saltiness_preference: Optional[int] = None
    lunch_budget_max: Optional[int] = None
    is_adventurous: Optional[bool] = None

class PasswordUpdate(BaseModel):
    """비밀번호 수정용 규격"""
    current_password: str
    new_password: str

class Token(BaseModel):
    """로그인 결과 발급할 토큰 규격 (추가)"""
    access_token: str
    token_type: str
    username: str
    nickname: str  # ← [추가] 닉네임 필드


# --- [4. 피드백 스키마] --- (DailyInquiry 제거)

class FeedbackCreate(BaseModel):
    # 인증된 유저의 토큰에서 ID를 가져오므로 user_id 필드 제외 가능 (프론트 전달용)
    menu_name: str
    feedback_type: str       
    category: str
    score: float             

class FeedbackResponse(FeedbackCreate):
    feedback_id: int
    user_id: int  # 응답에는 포함
    created_at: datetime

    class Config:
        from_attributes = True

class FeedbackUpdate(BaseModel):
    user_rating: int 
    is_revisit_intended: bool
    feedback_comment: Optional[str] = None


# --- [5. 최종 추천 결과 전용 스키마] --- (기존 유지)

class MenuRecommendationDetail(BaseModel):
    spicy_level: int
    texture: str
    rating: float

class MenuRecommendation(BaseModel):
    menu_name: str
    category: str
    image_url: Optional[str] = None
    price: int  # 가격 필드 추가
    match_rate: int
    description: str
    details: MenuRecommendationDetail
    restaurant_info: Optional[dict] = None  # 식당 정보 필드 추가

    class Config:
        from_attributes = True

# 2026-03-03 추가

class RestaurantBase(BaseModel):
    name: str
    address: Optional[str] = None
    latitude: float
    longitude: float
    category_1: Optional[str] = None
    category_2: Optional[str] = None
    distance: Optional[int] = None
    walking_time: Optional[int] = None

class RestaurantCreate(RestaurantBase):
    """식당 데이터 생성 시 사용 (필요 시)"""
    pass

class RestaurantResponse(RestaurantBase):
    """식당 정보 조회 응답용"""
    id: int

    class Config:
        from_attributes = True