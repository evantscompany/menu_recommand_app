import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-lunch-recommendation-app")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"mysql+pymysql://{os.getenv('TIDB_USER', '4R3uzcejsPmMq28.root')}:{os.getenv('TIDB_PASSWORD', 'MYtryu4hzULop2t1')}@{os.getenv('TIDB_HOST', 'gateway01.ap-northeast-1.prod.aws.tidbcloud.com')}:{os.getenv('TIDB_PORT', '4000')}/{os.getenv('TIDB_DATABASE', 'test')}?charset=utf8mb4&ssl=true")

settings = Settings()
