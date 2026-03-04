from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...database import get_db
from ... import crud, schemas
from ...core.security import get_current_user
from ...models import UserAccount

# 1. 여기서 router 객체를 반드시 생성해야 main.py가 인식합니다.
router = APIRouter()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """새로운 사용자 등록 및 취향 설정"""
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
    if user_update.email is not None:
        existing_email = db.query(UserAccount).filter(
            UserAccount.email == user_update.email,
            UserAccount.user_id != current_user.user_id
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")
    
    if user_update.nickname is not None:
        existing_nickname = db.query(UserAccount).filter(
            UserAccount.nickname == user_update.nickname,
            UserAccount.user_id != current_user.user_id
        ).first()
        if existing_nickname:
            raise HTTPException(status_code=400, detail="이미 사용 중인 닉네임입니다.")
    
    return db_user

@router.put("/me/password")
def update_current_user_password(
    password_update: schemas.PasswordUpdate,
    current_user: UserAccount = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """현재 로그인된 사용자의 비밀번호 수정"""
    db_user = crud.update_user_password(db, user_id=current_user.user_id, password_update=password_update)
    if db_user is None:
        raise HTTPException(
            status_code=400, 
            detail="현재 비밀번호가 올바르지 않습니다."
        )
    return {"message": "비밀번호가 성공적으로 변경되었습니다."}

@router.delete("/me")
def delete_current_user(
    current_user: UserAccount = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """현재 로그인된 사용자 계정 삭제 (회원탈퇴)"""
    success = crud.delete_user(db, user_id=current_user.user_id)
    if not success:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return {"message": "회원탈퇴가 완료되었습니다."}

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return {"message": f"User {user_id} 삭제 완료"}