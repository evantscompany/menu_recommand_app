"""
Railway 환경용 TiDB Cloud 연결 설정
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# TiDB Cloud 연결 정보 (Railway 환경용)
TIDB_HOST = os.getenv("TIDB_HOST", "gateway01.ap-northeast-1.prod.aws.tidbcloud.com")
TIDB_PORT = os.getenv("TIDB_PORT", "4000")
TIDB_USER = os.getenv("TIDB_USER", "3bJdto8FKWk47Fu.root")
TIDB_PASSWORD = os.getenv("TIDB_PASSWORD", "NWOZOcYDO8W5nMk2")
TIDB_DATABASE = os.getenv("TIDB_DATABASE", "test")

# MySQL 연결 URL 생성 (Railway용)
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{TIDB_USER}:{TIDB_PASSWORD}@{TIDB_HOST}:{TIDB_PORT}/{TIDB_DATABASE}?charset=utf8mb4"

# Engine 생성 (Railway 환경용)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # 핵심: SSL 설정을 딕셔너리로 명시
    connect_args={
        "ssl": {
            "fake_config": True,  # 일부 환경에서 SSL 활성화를 위해 필요
            "check_hostname": False,  # 호스트명 확인 생략
        }
    },
    # 연결 유지 설정 (TiDB/Railway 타임아웃 방지)
    pool_recycle=300,  # 5분마다 연결 재생성
    pool_pre_ping=True,  # 연결 상태 확인
    echo=False  # SQL 로그 출력 (배포 시 False)
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

# 데이터베이스 연결 테스트 함수
def test_connection():
    """TiDB Cloud 연결 테스트"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            print(f"✅ TiDB Cloud 연결 성공!")
            print(f"📊 MySQL 버전: {version}")
            return True
    except Exception as e:
        print(f"❌ TiDB Cloud 연결 실패: {e}")
        return False

# 테이블 생성 함수
def create_tables():
    """모든 테이블 생성"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ 데이터베이스 테이블 생성 완료")
    except Exception as e:
        print(f"❌ 테이블 생성 실패: {e}")

if __name__ == "__main__":
    # 연결 테스트
    if test_connection():
        # 테이블 생성
        create_tables()
