from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ...database import get_db
from ... import models, schemas
from ..deps import get_current_user

router = APIRouter()

# [수정] response_model을 사장님이 새로 만든 schemas.RestaurantResponse로 변경 (거리, 도보시간 포함 위함)
@router.get("/", response_model=List[schemas.RestaurantResponse])
def get_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    식당 목록 조회 (사장님이 추가한 엑셀 데이터 포함)
    """
    restaurants = db.query(models.Restaurant)\
                 .offset(skip)\
                 .limit(limit)\
                 .all()
    return restaurants

# [수정] response_model 변경 및 ID 필터링 조건 수정
@router.get("/{restaurant_id}", response_model=schemas.RestaurantResponse)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    """
    특정 식당 정보 조회
    """
    # [수정] 사장님 모델의 실제 컬럼명인 .id로 매칭 (기존 restaurant_id에서 변경)
    restaurant = db.query(models.Restaurant)\
                 .filter(models.Restaurant.id == restaurant_id)\
                 .first()
    
    if not restaurant:
        raise HTTPException(status_code=404, detail="식당을 찾을 수 없습니다.")
    
    return restaurant

# [수정] 기존 Menu 모델과 연동되도록 로직 보완
@router.get("/{restaurant_id}/menus", response_model=List[schemas.Menu])
def get_restaurant_menus(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    """
    식당의 카테고리를 기반으로 추천 가능한 메뉴 목록을 가져옵니다.
    """
    # 1. 먼저 해당 식당의 정보를 가져옵니다.
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="식당을 찾을 수 없습니다.")
    
    # 2. 식당의 category_1과 일치하는 메뉴들을 menus 테이블에서 검색합니다.
    menus = db.query(models.Menu).filter(models.Menu.category == restaurant.category_1).all()
    return menus

# [수정] response_model을 RestaurantResponse로 변경
@router.post("/", response_model=schemas.RestaurantResponse)
def create_restaurant(
    restaurant: schemas.RestaurantCreate,
    current_user: models.UserAccount = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    식당 정보 생성 (관리자 기능)
    """
    # 사장님 모델 구조에 맞게 데이터 생성
    db_restaurant = models.Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant