import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# TiDB Cloud MySQL 연결 정보
TIDB_HOST = os.getenv("TIDB_HOST", "gateway01.ap-northeast-1.prod.aws.tidbcloud.com")
TIDB_PORT = os.getenv("TIDB_PORT", "4000")
TIDB_USER = os.getenv("TIDB_USER", "3bJdto8FKWk47Fu.root")
TIDB_PASSWORD = os.getenv("TIDB_PASSWORD", "NWOZOcYDO8W5nMk2")
TIDB_DATABASE = os.getenv("TIDB_DATABASE", "test")

# TiDB Cloud 사용자 이름 형식: {prefix}.{username}
# Serverless Tier는 접두사가 필요 없을 수 있음
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
