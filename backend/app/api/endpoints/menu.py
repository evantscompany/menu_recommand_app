from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_db
from ... import crud, schemas

router = APIRouter()

# 메뉴 조회 기능만 유지 (메뉴는 정해진 데이터 기반)
@router.get("/", response_model=list[schemas.Menu])
def read_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    등록된 메뉴 리스트를 가져옵니다.
    메뉴 데이터는 정해진 테이블 데이터를 기반으로 합니다.
    """
    menus = crud.get_menus(db, skip=skip, limit=limit)
    return menus