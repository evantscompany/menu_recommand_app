from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database import SessionLocal
from ... import crud, schemas

router = APIRouter()

# DB 세션 의존성 주입 (매 요청마다 DB 연결을 관리)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Store)
def create_new_store(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    return crud.create_store(db=db, store=store)

@router.get("/", response_model=list[schemas.Store])
def read_stores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stores = crud.get_stores(db, skip=skip, limit=limit)
    return stores