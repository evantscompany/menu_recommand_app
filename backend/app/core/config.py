import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-lunch-recommendation-app")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///restaurant_app.db")

settings = Settings()
