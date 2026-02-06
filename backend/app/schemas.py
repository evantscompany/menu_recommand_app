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


# --- [2. 식당 정보 스키마] ---
class RestaurantBase(BaseModel):
    restaurant_name: str
    address: str
    phone_number: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    opening_hours: Optional[str] = None
    rating: float = 0.0
    image_url: Optional[str] = None

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    restaurant_id: int
    
    class Config:
        from_attributes = True

# --- [3. 식당-메뉴 연결 스키마 ---
class RestaurantMenuBase(BaseModel):
    restaurant_id: int
    menu_id: int
    price: int
    is_available: bool = True
    special_note: Optional[str] = None

class RestaurantMenuCreate(RestaurantMenuBase):
    pass

class RestaurantMenu(RestaurantMenuBase):
    restaurant_menu_id: int
    restaurant: Restaurant
    menu: 'Menu'
    
    class Config:
        from_attributes = True

# --- [4. 메뉴 메인 정보 스키마] --- (정규화 후)
class MenuBase(BaseModel):
    menu_name: str
    category: str
    image_url: Optional[str] = None
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
    restaurant_menus: Optional[List[RestaurantMenu]] = None

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

    class Config:
        from_attributes = True

class Token(BaseModel):
    """로그인 결과 발급할 토큰 규격 (추가)"""
    access_token: str
    token_type: str
    username: str
    nickname: str  # ← [추가] 닉네임 필드


# --- [4. 질문 및 피드백 스키마] --- (기존 유지)

class DailyInquiry(BaseModel):
    dietary_restriction : str
    spicy_level : str
    budget_range : str
    salty_level : str
    exploration_style : str
    city: str = "Seoul"

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
    menu_id: int
    menu_name: str
    category: str
    image_url: Optional[str] = None
    match_rate: int
    description: str
    details: MenuRecommendationDetail
    restaurant_info: Optional[dict] = None  # 식당 정보 필드 추가

    class Config:
        from_attributes = True