from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...database_railway import get_db
from ... import crud, schemas
from ...core.security import get_current_user
from ...models import UserAccount

# 1. 여기서 router 객체를 반드시 생성해야 main.py가 인식합니다.
router = APIRouter()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """새로운 사용자 등록 및 성향 설정"""
    return crud.create_user(db=db, user=user)

@router.get("/me", response_model=schemas.User)
def get_current_user_profile(current_user: UserAccount = Depends(get_current_user)):
    """현재 로그인된 사용자의 프로필 정보 조회"""
    # 직접 current_user 객체 사용 (DB 재조회 불필요)
    if current_user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    # User 스키마에 맞게 반환 (profile은 None으로 설정)
    user_data = {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "nickname": current_user.nickname,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "profile": None  # 스키마 기본값 사용
    }
    
    return schemas.User(**user_data)

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """사용자 프로필 및 성향 조회"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return db_user

@router.put("/me", response_model=schemas.User)
def update_current_user_profile(
    user_update: schemas.UserUpdate,
    current_user: UserAccount = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """현재 로그인된 사용자의 프로필 정보 수정"""
    db_user = crud.update_user_profile(db, user_id=current_user.user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    # 이메일/닉네임 중복 체크
