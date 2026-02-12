from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ...database import get_db
from ... import models, schemas
from ..deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Restaurant])
def get_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    식당 목록 조회 (페이지네이션 지원)
    """
    restaurants = db.query(models.Restaurant)\
                 .offset(skip)\
                 .limit(limit)\
                 .all()
    return restaurants

@router.get("/{restaurant_id}", response_model=schemas.Restaurant)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    """
    특정 식당 정보 조회
    """
    restaurant = db.query(models.Restaurant)\
                 .filter(models.Restaurant.restaurant_id == restaurant_id)\
                 .first()
    
    if not restaurant:
        raise HTTPException(status_code=404, detail="식당을 찾을 수 없습니다.")
    
    return restaurant

@router.get("/{restaurant_id}/menus", response_model=List[schemas.RestaurantMenu])
def get_restaurant_menus(
    restaurant_id: int,
    available_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """
    특정 식당의 메뉴 목록 조회
    """
    query = db.query(models.RestaurantMenu)\
            .filter(models.RestaurantMenu.restaurant_id == restaurant_id)
    
    if available_only:
        query = query.filter(models.RestaurantMenu.is_available == True)
    
    menus = query.all()
    return menus

@router.post("/", response_model=schemas.Restaurant)
def create_restaurant(
    restaurant: schemas.RestaurantCreate,
    current_user: models.UserAccount = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    식당 정보 생성 (관리자 기능)
    """
    # TODO: 관리자 권한 체크 로직 추가
    db_restaurant = models.Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant
