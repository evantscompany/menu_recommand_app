from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
import app.models as models
# [수정] 모든 엔드포인트를 app.api.endpoints에서 일관되게 가져옵니다.
from app.api.endpoints import user, recommendation, menu 

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

@app.get("/")
def home():
    return {"message": "서버가 정상적으로 실행되었습니다. 오늘 점심은 메추리가 책임집니다!"}

# [수정] 라우터 등록: prefix를 /menus로 변경하여 일관성을 맞춥니다.
app.include_router(menu.router, prefix="/menus", tags=["Menus"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(recommendation.router, prefix="/recommend", tags=["Recommendation"])