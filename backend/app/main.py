from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# 상대 경로(.) 대신 절대 경로 형식으로 수정하여 인식률을 높입니다.
from app.database import engine
import app.models as models
from app.api.endpoints import store, user, recommendation 

# DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="식당추천 서비스 메추리")

# [중요] 프론트엔드 통신을 위한 CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (테스트용)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS 등 모두 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.get("/")
def home():
    return {"message": "서버가 정상적으로 실행되었습니다. 오늘 점심은 메추리가 책임집니다!"}

# 라우터 등록
app.include_router(store.router, prefix="/stores", tags=["Stores"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(recommendation.router, prefix="/recommend", tags=["Recommendation"])