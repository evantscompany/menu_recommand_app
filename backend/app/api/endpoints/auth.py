from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # [추가]
from sqlalchemy.orm import Session
from datetime import timedelta

from ...database_mysql import get_db
from ... import crud, schemas, models
from ...core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..deps import get_current_user
from typing import Union, Optional

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
            detail="이미 사용 중인 이메일입니다."
        )
    
    # ← [추가] 닉네임 중복 체크
    db_nickname = db.query(models.UserAccount).filter(models.UserAccount.nickname == user.nickname).first()
    if db_nickname:
        raise HTTPException(
            status_code=400,
            detail="이미 사용 중인 닉네임입니다."
        )

    return crud.create_user(db=db, user=user)


# --- [2. 로그인 API] --- (OAuth2PasswordRequestForm 지원 - Swagger Authorize 버튼용)
@router.post("/login")
def login(
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
        "token": access_token,  # 프론트엔드에서 기대하는 필드명
        "access_token": access_token,  # 호환성 유지
        "token_type": "bearer",
        "username": user.username,
        "nickname": user.nickname
    }

# --- [2-1. 로그인 API] --- (JSON 요청 지원)
@router.post("/login-json")
def login_json(
    login_data: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    """
    아이디/비번 검증 후 Access Token(JWT) 발급
    JSON 형식 요청 지원
    """
    # 1. 유저 찾기
    user = crud.get_user_by_username(db, username=login_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 틀렸습니다.",
        )

    # 2. 비밀번호 검증
    if not verify_password(login_data.password, user.hashed_password):
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
        "token": access_token,  # 프론트엔드에서 기대하는 필드명
        "access_token": access_token,  # 호환성 유지
        "token_type": "bearer",
        "username": user.username,
        "nickname": user.nickname
    }

@router.get("/me", response_model=schemas.User)
def get_current_user_info(current_user: models.UserAccount = Depends(get_current_user)):
    """
    현재 인증된 사용자 정보 조회
    """
    return current_user