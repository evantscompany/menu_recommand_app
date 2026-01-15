from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./restaurant_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- 이 부분이 빠져있어서 에러가 났습니다! ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()