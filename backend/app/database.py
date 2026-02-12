from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. SQLite 데이터베이스 경로 설정
# 현재 프로젝트 루트에 restaurant_app.db 파일이 생성돼.
SQLALCHEMY_DATABASE_URL = "sqlite:///./restaurant_app.db"

# 2. Engine 생성
# check_same_thread: False는 SQLite에서 FastAPI처럼 멀티 스레드를 쓸 때 필수 설정이야.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 세션 설정
# 실제 DB 작업(Commit, Flush 등)을 관리하는 도구야.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 모델 생성을 위한 Base 클래스
Base = declarative_base()

# 5. Dependency Injection용 get_db 함수 (중요!)
# API 엔드포인트에서 Depends(get_db)로 호출해서 사용해.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # 요청이 끝나면 에러 유무와 상관없이 반드시 연결을 닫아줘서 메모리 누수를 막아.
        db.close()