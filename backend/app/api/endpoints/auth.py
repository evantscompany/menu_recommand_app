"""
로그인 API 수정 - JSON 요청 지원
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel

from ...database_railway import get_db
from ... import crud, schemas, models
from ...core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..deps import get_current_user
from typing import Union, Optional

# JSON 로그인 요청 모델
class LoginRequest(BaseModel):
    username: str
    password: str

router = APIRouter()

# --- [1. 회원가입 API] --- (기존 유지)
@router.post("/signup", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    아이디/이메일/닉네임 중복 체크 후 계정 및 취향 프로필 생성
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="이미 존재하는 아이디입니다."
        )
    
    db_email = db.query(models.UserAccount).filter(models.UserAccount.email == user.email).first()
    if db_email:
        raise HTTPException(
            status_code=400,
            detail="이미 존재하는 이메일입니다."
        )
    
    # 닉네임 중복 체크 및 자동 생성
    original_nickname = user.nickname
    counter = 1
    while True:
        db_nickname = db.query(models.UserAccount).filter(models.UserAccount.nickname == user.nickname).first()
        if not db_nickname:
            break
        user.nickname = f"{original_nickname}{counter}"
        counter += 1
        if counter > 100:
            raise HTTPException(status_code=400, detail="닉네임 생성에 실패했습니다.")
    
    # 사용자 생성
    try:
        db_user = crud.create_user(db, user)
        db.refresh(db_user)
        
        return db_user
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"회원가입 중 오류 발생: {str(e)}")

# --- [2. 로그인 API] --- (JSON 지원 추가)
@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    login_data: LoginRequest,  # JSON 요청 지원
    db: Session = Depends(get_db)
):
    """
    아이디/비번 검증 후 Access Token(JWT) 발급
    JSON 요청과 Form 요청 모두 지원
    """
    username = login_data.username
    password = login_data.password

    # 1. 유저 찾기
    user = crud.get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 틀렸습니다.",
        )

    # 2. 비밀번호 검증
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 틀렸습니다.",
        )

    # 3. 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )

    # 응답 규격 (프론트엔드와 맞춤)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "nickname": user.nickname
    }

# --- [3. 기존 Form 로그인 API] --- (Swagger 호환성 유지)
@router.post("/token", response_model=schemas.Token)
def login_for_access_token_form(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    아이디/비번 검증 후 Access Token(JWT) 발급
    OAuth2PasswordRequestForm 지원 (Swagger Authorize 버튼용)
    """
    username = form_data.username
    password = form_data.password

    # 1. 유저 찾기
    user = crud.get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 틀렸습니다.",
        )

    # 2. 비밀번호 검증
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 틀렸습니다.",
        )

    # 3. 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )

    # 응답 규격 (프론트엔드와 맞춤)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "nickname": user.nickname
    }

# --- [4. 현재 사용자 정보 API] ---
@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.UserAccount = Depends(get_current_user)):
    """
    현재 로그인된 사용자 정보 반환
    """
    return current_user
