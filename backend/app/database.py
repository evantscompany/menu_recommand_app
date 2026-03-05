import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# TiDB Cloud MySQL 연결 정보
TIDB_HOST = os.getenv("TIDB_HOST", "gateway01.ap-northeast-1.prod.aws.tidbcloud.com")
TIDB_PORT = os.getenv("TIDB_PORT", "4000")
TIDB_USER = os.getenv("TIDB_USER", "4R3uzcejsPmMq28.root")
TIDB_PASSWORD = os.getenv("TIDB_PASSWORD", "MYtryu4hzULop2t1")
TIDB_DATABASE = os.getenv("TIDB_DATABASE", "test")

# TiDB Cloud 사용자 이름 형식: {prefix}.{username}
MYSQL_USER = TIDB_USER

# MySQL 연결 URL 생성 (TiDB Cloud Serverless용)
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{TIDB_PASSWORD}@{TIDB_HOST}:{TIDB_PORT}/{TIDB_DATABASE}?charset=utf8mb4&ssl=true"

# Engine 생성 (TiDB Cloud Serverless용 설정)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 연결 상태 확인
    pool_recycle=3600,  # 1시간마다 연결 재생성
    connect_args={
        "ssl": {
            "ssl": True
        }
    },
    echo=False  # SQL 로그 출력 (개발 시 True로 설정)
)

# 세션 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 생성을 위한 Base 클래스
Base = declarative_base()

# Dependency Injection용 get_db 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()