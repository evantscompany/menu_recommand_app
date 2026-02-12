from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # [추가]
from sqlalchemy.orm import Session
from datetime import timedelta

from ...database import get_db
from ... import crud, schemas, models
from ...core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

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


# --- [2. 로그인 API] --- (Swagger Authorize 호환 수정)
@router.post("/login")
def login(
    db: Session = Depends(get_db),
    # [수정] schemas.UserLogin 대신 OAuth2PasswordRequestForm 사용
    # 이를 통해 Swagger UI의 Authorize 창(Form Data 방식)과 호환됩니다.
    login_data: OAuth2PasswordRequestForm = Depends() 
):
    """
    아이디/비번 검증 후 Access Token(JWT) 발급
    """
    # 1. 유저 찾기 (login_data.username으로 접근)
    user = crud.get_user_by_username(db, username=login_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 틀렸습니다.",
        )

    # 2. 비밀번호 검증 (login_data.password로 접근)
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

    # 응답 규격은 schemas.Token 형식을 따름
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "username": user.username,
        "nickname": user.nickname  # ← [추가] 닉네임 필드
    }