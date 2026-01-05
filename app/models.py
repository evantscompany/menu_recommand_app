from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Store(Base):
    __tablename__="stores"

    #고정정보
    store_id = Column(Integer,primary_key=True,index=True) #가게 고유 아이디 ,기준으로 씀
    store_name= Column(String,nullable=False) #가게 이름
    category=Column(String)         #카테고리 (일식,한식,중식 외)
    address=Column(String)          #매장 주소
    phone_number=Column(String)     #매장 전화번호
    image_url=Column(String)        #대표이미지
    price_level=Column(Integer)     #가격대
    
    #상황/환경 태그
    matching_weather = Column(String)   # 추천 날씨 
    matching_mood = Column(String)      # 추천 기분
    suitable_ground_size = Column(Integer)  #방문인원 적합도
    is_quick_meal = Column(Boolean)         #회전 여부(Yes or No)
    

    #관계 설정 (1:1 또는 1:N)
    #여기서 1:1 은 식당의 상세데이터는 식당 1개당 1개 뿐임 [단일 객체로 불러옴]
    #여기서 1:N 은 식당에 방문한 다양한 사람들의 히스토리가 들어가므로 여러가지를 불러올수 있다를 말함 [리스트 형식으로 여러 히스토리 불러옴]

    details = relationship("StoreDetail",back_populates="store",uselist=False)

    visits = relationship("UserHistory", back_populates="store")

    #relationship : Store테이블과 StoreDetail 테이블은 별도의 테이블로 완전 남남인데
    # relationship 설정 하면 웹사이트의 하이퍼 링크마냥 서로 인식하게 해줌.
    #back_populates -> 양방향 연결
    #->store 테이블에서 storedetail을 부르기도 하고 하는거
    #uselist=false -> 이 식당에 연결된 상세정보는 딱 하나 뿐이다! 리스트가 아닌 객체로 가져오라는것.

class StoreDetail(Base):
    __tablename__="store_details"

    detail_id = Column(Integer,primary_key=True, index=True)
    store_id= Column(Integer,ForeignKey("stores.store_id"))

    #수치기반데이터(알고리즘 핵심)
    spicy_level = Column(Integer)   #맵기정보
    saltiness_level= Column(Integer) #간의세기
    heaviness=Column(Float)         #음식의 무게감
    serving_temperature=Column(String) # 주관적이므로 문자열로 받기
    texture = Column(String)

    #신뢰도 및 경험
    revisit_rate = Column(Float) #재방문율
    avg_waiting_time = Column(Integer) #평균 대기 시간
    ad_suspicion_index = Column(Float) #광고 의심
    real_satisfaction_score = Column(Float) # 실제 만족도 점수

    store = relationship("Store",back_populates="details")


class UserHistory(Base): #사용자 히스토리 테이블
    __tablename__ = "user_histories"

    history_id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,index=True)
    store_id = Column(Integer, ForeignKey("stores.store_id"))

    #히스토리 데이터

    last_visit_date = Column(DateTime, default=datetime.utcnow)
    visit_count=Column(Integer,)
    last_eaten_category=Column(String)

    store=relationship("Store",back_populates="visits")