from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

# 프로젝트 구조에 맞게 수정된 import (상대 경로 혹은 절대 경로)
from ..database_railway import get_db
from .. import models, crud
# 여기서 방금 보여주신 보안 파일의 변수와 함수를 가져옵니다
from ..core.security import SECRET_KEY, ALGORITHM 
from ..core.config import settings

# 프론트엔드가 토큰을 실어 보낼 경로 정의
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> models.UserAccount:
    """
    보여주신 security.py의 토큰 해독 로직을 사용하여 
    현재 접속한 유저 객체를 반환하는 공통 함수입니다.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보가 유효하지 않거나 만료되었습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. security.py에서 정의한 SECRET_KEY와 ALGORITHM으로 토큰 해독
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # subject(유저 식별자) 추출
        
        if username is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # 2. 해독된 username으로 DB에서 실제 유저(Account) 정보를 가져옴
    user = crud.get_user_by_username(db, username=username)
    
    if user is None:
        raise credentials_exception
        
    # 3. profile 관계를 명시적으로 로드하여 None 방지
    if hasattr(user, 'profile') and user.profile is None:
        # profile이 없으면 빈 UserProfile 객체 생성
        from .. import models
        user.profile = models.UserProfile(
            user_id=user.user_id,
            dietary_label="none",
            allergies="",
            spicy_threshold=3,
            saltiness_preference=3,
            lunch_budget_max=12000,
            is_adventurous=True
        )
        
    return user
