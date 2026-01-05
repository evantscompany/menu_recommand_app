from sqlalchemy.orm import Session
from . import models, schemas

# 1. 식당 정보 저장 (Create)
def create_store(db: Session, store: schemas.StoreCreate):
    # 식당 기본 정보 생성
    db_store = models.Store(
        store_name=store.store_name,
        category=store.category,
        address=store.address,
        phone_number=store.phone_number,
        image_url=store.image_url,
        price_level=store.price_level,
        is_lunch_available=store.is_lunch_available,
        matching_weather=store.matching_weather,
        matching_mood=store.matching_mood,
        suitable_ground_size=store.suitable_ground_size,
        is_quick_meal=store.is_quick_meal
    )
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

# 2. 모든 식당 목록 가져오기 (Read - List)
def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Store).offset(skip).limit(limit).all()

# 3. 특정 조건(날씨/기분)으로 식당 추천 받기 (Read - Filter)
# (나중에 core/algorithm.py로 발전시키기 전 기초 단계입니다)
def get_stores_by_condition(db: Session, weather: str = None, mood: str = None):
    query = db.query(models.Store)
    if weather:
        query = query.filter(models.Store.matching_weather == weather)
    if mood:
        query = query.filter(models.Store.matching_mood == mood)
    return query.all()