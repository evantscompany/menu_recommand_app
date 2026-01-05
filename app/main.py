from fastapi import FastAPI
from .database import engine, Base
import app.models as models
from .api.endpoints import store

#서버가 시작될 때, models.py 에 정의된 테이블들을 실제 DB에 만듬
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title = "식당추천 서비스 메추리")

@app.get("/")
def home():
    return{"message": "서버가 정상적으로 실행되었습니다."}

app.include_router(store.router, prefix="/stores", tags=["Stores"])