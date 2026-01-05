#main.py가 DB에 저장되는 데이터의 생김새라면, schemas.py 는 사용자(프론트 앤드)와 주고 받는 데이터 규격

from pydantic import BaseModel,HttpUrl
from typing import List, Optional
from datetime import datetime

#상세 데이터 스키마
class StoreDetailBase(BaseModel):
    spicy_level:int
    saltiness_level : int
    heaviness : float
    serving_temperature : str
    texture : str
    revisit_rate: float
    avg_waiting_time : int
    ad_suspicion_index : float
    real_satisfaction_score : float

class StoreDetail(StoreDetailBase):
    class Config:
        from_attributes = True # DB모델 객체를 자동으로 변환해주는 설정


# --- [식당 정보 스키마] ---
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
    is_quick_meal: bool

class StoreCreate(StoreBase):
    """식당 데이터를 처음 등록할 때 사용하는 규격"""
    pass

class Store(StoreBase):
    """프론트엔드로 데이터를 보낼 때 사용하는 규격 (ID와 상세정보 포함)"""
    store_id: int
    details: Optional[StoreDetail] = None

    class Config:
        from_attributes = True