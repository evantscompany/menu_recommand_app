from fastapi import FastAPI
from .database import engine
import app.models as models
# 신규 라우터들 추가 (만들어야 할 것들)
from .api.endpoints import store, user, recommendation 

# DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="식당추천 서비스 메추리")

@app.get("/")
def home():
    return {"message": "서버가 정상적으로 실행되었습니다. 오늘 점심은 메추리가 책임집니다!"}

# 라우터 등록
app.include_router(store.router, prefix="/stores", tags=["Stores"])
app.include_router(user.router, prefix="/users", tags=["Users"]) # 가입 및 성향 저장용
app.include_router(recommendation.router, prefix="/recommend", tags=["Recommendation"]) # 핵심 로직용