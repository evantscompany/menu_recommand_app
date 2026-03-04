from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.database_railway import engine
import app.models as models
# [수정] auth 라우터를 추가로 불러옵니다.
from app.api.endpoints import user, recommendation, menu, auth

# DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="식당추천 서비스 메추리")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# UTF-8 인코딩 미들웨어 추가
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000
)

@app.get("/")
def home():
    return {"message": "서버가 정상적으로 실행되었습니다. 오늘 점심은 메추리가 책임집니다!"}

# --- [라우터 등록] ---

# 1. 인증 및 계정 관련 (로그인, 회원가입 등)
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# 2. 메뉴 관련 (메뉴 등록, 조회 등)
app.include_router(menu.router, prefix="/api/menus", tags=["Menus"])

# 3. 사용자 정보 관련 (기존 user 라우터)
app.include_router(user.router, prefix="/api/users", tags=["Users"])

# 4. 추천 시스템 관련
app.include_router(recommendation.router, prefix="/api/recommend", tags=["Recommendation"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.0.22", port=8000)