from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Store(Base):
    __tablename__ = "stores"

    # 고정 정보
    store_id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String, nullable=False)
    category = Column(String)             # 카테고리 (일식, 한식, 중식 등)
    address = Column(String)              # 매장 주소
    phone_number = Column(String)         # 매장 전화번호
    image_url = Column(String)            # 대표 이미지
    price_level = Column(Integer)         # 가격대 (1: 저렴 ~ 4: 비쌈)
    
    # 상황/환경 태그
    matching_weather = Column(String)     # 추천 날씨 (Rain, Clear 등)
    matching_mood = Column(String)        # 추천 기분
    suitable_ground_size = Column(Integer) # 방문 인원 적합도
    is_quick_meal = Column(Boolean)       # 회전율 빠름 여부
    is_lunch_available = Column(Boolean, default=True)

    # 관계 설정
    details = relationship("StoreDetail", back_populates="store", uselist=False)
    visits = relationship("UserHistory", back_populates="store")


class StoreDetail(Base):
    __tablename__ = "store_details"

    detail_id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.store_id"))

    # 수치 기반 데이터 (알고리즘 핵심)
    spicy_level = Column(Integer)        # 맵기 레벨 (1~5)
    saltiness_level = Column(Integer)    # 간의 세기 (1~5)
    heaviness = Column(Float)            # 음식의 무게감 (1.0~5.0)
    serving_temperature = Column(String) # 온도 (Cold, Hot, Warm)
    texture = Column(String)             # 식감 (Crispy, Chewy, Soft)

    # 신뢰도 및 통계 데이터
    revisit_rate = Column(Float)         # 재방문율
    avg_waiting_time = Column(Integer)   # 평균 대기 시간 (분)
    ad_suspicion_index = Column(Float)   # 광고 의심 지수 (0~1)
    real_satisfaction_score = Column(Float) # 실제 만족도 점수 (1~5)

    store = relationship("Store", back_populates="details")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)

    # 1. 신체적/철학적 제약 (하드 필터용)
    dietary_label = Column(String, default="none") # none, vegan, pesco 등
    allergies = Column(String, nullable=True)      # "nut,shrimp" 등 콤마 구분

    # 2. 미각적 기본 역치 (알고리즘 기준점)
    spicy_threshold = Column(Integer, default=3)   # 1~5 선호 맵기
    saltiness_preference = Column(Integer, default=3) # 1~5 선호 짠맛

    # 3. 라이프스타일 및 성향
    lunch_budget_max = Column(Integer, default=12000)
    is_adventurous = Column(Boolean, default=True) # 새로운 메뉴 도전 선호 여부
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계 설정
    histories = relationship("UserHistory", back_populates="user")


class UserHistory(Base):
    """
    사용자의 방문 기록 및 피드백 저장
    추천 결과에 대한 사후 피드백(평점, 재방문의사)이 여기에 저장됨
    """
    __tablename__ = "user_histories"

    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), index=True)
    store_id = Column(Integer, ForeignKey("stores.store_id"))

    # 방문 및 피드백 데이터
    last_visit_date = Column(DateTime, default=datetime.utcnow)
    visit_count = Column(Integer, default=1)
    last_eaten_category = Column(String)
    
    # [추가] 추천 후 피드백 반영용 필드
    user_rating = Column(Integer, nullable=True)     # 사용자가 남긴 평점 (1~5)
    is_revisit_intended = Column(Boolean, default=True) # 재방문 의사 여부
    feedback_comment = Column(String, nullable=True) # 간단한 피드백 (예: "오늘 기분에 딱이었음")

    # 관계 설정
    store = relationship("Store", back_populates="visits")
    user = relationship("User", back_populates="histories")