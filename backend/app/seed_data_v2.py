import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
import random



def seed_db():
    db = SessionLocal()
    # 1. 초기화: 기존 테이블 삭제 후 재생성
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    # 기본 메뉴 소스 (이 리스트를 기반으로 100개를 변형 생성)
    base_menus = [
        ("김치찌개", "한식"), ("된장찌개", "한식"), ("제육볶음", "한식"), ("비빔밥", "한식"),
        ("순두부찌개", "한식"), ("불고기정식", "한식"), ("육개장", "한식"), ("냉면", "한식"),
        ("등심돈카츠", "일식"), ("안심돈카츠", "일식"), ("소유라멘", "일식"), ("미소라멘", "일식"),
        ("사케동", "일식"), ("규동", "일식"), ("모듬초밥", "일식"), ("가츠동", "일식"),
        ("짜장면", "중식"), ("해물짬뽕", "중식"), ("마라탕", "중식"), ("꿔바로우", "중식"),
        ("볶음밥", "중식"), ("마파두부", "중식"), ("양장피", "중식"), ("토마토계란볶음", "중식"),
        ("치즈버거", "양식"), ("까르보나라", "양식"), ("알리오올리오", "양식"), ("스테이크", "양식"),
        ("페퍼로니피자", "양식"), ("시저샐러드", "샐러드"), ("연어포케", "샐러드"), ("샌드위치", "분식"),
        ("떡볶이", "분식"), ("김밥", "분식"), ("쌀국수", "아시안"), ("팟타이", "아시안"),
        ("나시고랭", "아시안"), ("분짜", "아시안"), ("타코", "기타"), ("케밥", "기타")
    ]

    print("🚀 100개의 메뉴 데이터 생성을 시작합니다...")

    for i in range(100):
        # 기본 메뉴 리스트에서 하나를 선택하고 변형을 줍니다.
        base_name, category = random.choice(base_menus)
        menu_name = f"{base_name}_{i+1}" # 중복 방지를 위해 인덱스 추가
        
        # 2. 메뉴 기본 정보 설정
        menu = models.Menu(
            menu_name=menu_name,
            category=category,
            price_level=random.randrange(7000, 25000, 500), # 7000원~25000원 사이
            image_url=f"https://picsum.photos/seed/{menu_name}/400/300",
            is_lunch_available=True,
            matching_weather=random.choice(["Clear", "Rain", "Cloudy", "Snow"]),
            matching_mood=random.choice(["스트레스", "가벼움", "든든함", "피곤함"])
        )

        # 3. 메뉴 상세 정보 (알고리즘 핵심 데이터) 랜덤 설정
        menu.details = models.MenuDetail(
            spicy_level=random.randint(1, 5),
            saltiness_level=random.randint(1, 5),
            heaviness=round(random.uniform(1.0, 5.0), 1),
            serving_temperature=random.choice(["Hot", "Cold", "Warm"]),
            texture=random.choice(["Crispy", "Soft", "Chewy"]),
            real_satisfaction_score=round(random.uniform(3.0, 5.0), 1),
            ad_suspicion_index=round(random.uniform(0.0, 0.3), 2),
            revisit_rate=round(random.uniform(0.5, 0.98), 2),
            avg_waiting_time=random.randint(0, 30)
        )
        
        db.add(menu)

    db.commit()
    print(f"✅ 총 {db.query(models.Menu).count()}개의 메뉴 데이터 주입이 완료되었습니다!")

    # 4. 테스트 유저 생성 (ID: 1)
    test_user = models.User(
        username="test_user",
        dietary_label="none",
        spicy_threshold=3,
        saltiness_preference=3,
        lunch_budget_max=15000
    )
    db.add(test_user)
    db.commit()
    print("👤 테스트 유저(ID: 1) 생성 완료")

    db.close()

if __name__ == "__main__":
    seed_db()