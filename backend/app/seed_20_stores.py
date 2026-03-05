from datetime import datetime
import os
from app.database_mysql import engine, SessionLocal
import app.models as models

#1. 강제 테이블 생성
models.Base.metadata.create_all(bind=engine)


# 현재 파일의 부모 폴더(backend)에 있는 DB 파일을 찾도록 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 만약 backend/app/seed_20_stores.py 위치라면 한 단계 위로 설정
db_path = os.path.join(BASE_DIR, "..", "restaurant_app.db")

def seed_20_stores():
    conn = sqlite3.connect('restaurant_app.db')
    cursor = conn.cursor()

    # 기존 데이터 삭제 (중복 방지)
    cursor.execute("DELETE FROM store_details")
    cursor.execute("DELETE FROM stores")

    # 1. 20개 식당 기본 정보 (stores)
    # 카테고리: 한식, 중식, 일식, 양식, 카페 / price_level: 1~4
    stores_data = [
        (1, '초록뜰 샐러드', '양식', '서울 강남구', '02-111-0001', 'img1.jpg', 1, 'Clear', 'Peaceful', 2, 1),
        (2, '불타는 마라탕', '중식', '서울 서초구', '02-111-0002', 'img2.jpg', 2, 'Rain', 'Excited', 4, 1),
        (3, '담백가정식', '한식', '서울 송파구', '02-111-0003', 'img3.jpg', 2, 'Cloudy', 'Comfortable', 1, 1),
        (4, '버거스테이션', '양식', '서울 마포구', '02-111-0004', 'img4.jpg', 2, 'Clear', 'Young', 2, 1),
        (5, '심야식당 긴자', '일식', '서울 용산구', '02-111-0005', 'img5.jpg', 3, 'Rain', 'Lonely', 2, 1),
        (6, '진짜루손짜장', '중식', '서울 성동구', '02-111-0006', 'img6.jpg', 1, 'Clear', 'Happy', 6, 1),
        (7, '산들채 비건비빔밥', '한식', '서울 종로구', '02-111-0007', 'img7.jpg', 1, 'Clear', 'Healthy', 4, 1),
        (8, '파스타노바', '양식', '서울 영등포구', '02-111-0008', 'img8.jpg', 3, 'Clear', 'Romantic', 2, 1),
        (9, '돈카츠 명가', '일식', '서울 관악구', '02-111-0009', 'img9.jpg', 2, 'Clear', 'Focused', 1, 1),
        (10, '무한조개구이', '한식', '서울 광진구', '02-111-0010', 'img10.jpg', 4, 'Cloudy', 'Excited', 8, 1),
        (11, '베지터블 커리', '인도식', '서울 강북구', '02-111-0011', 'img11.jpg', 2, 'Cloudy', 'Calm', 2, 1),
        (12, '우동사무소', '일식', '서울 성북구', '02-111-0012', 'img12.jpg', 1, 'Rain', 'Lonely', 1, 1),
        (13, '황궁쟁반짜장', '중식', '서울 노원구', '02-111-0013', 'img13.jpg', 2, 'Clear', 'Busy', 4, 1),
        (14, '본가삼계탕', '한식', '서울 동작구', '02-111-0014', 'img14.jpg', 3, 'Snow', 'Healthy', 4, 1),
        (15, '피자헤븐', '양식', '서울 서대문구', '02-111-0015', 'img15.jpg', 2, 'Clear', 'Happy', 4, 1),
        (16, '스시웨이', '일식', '서울 강동구', '02-111-0016', 'img16.jpg', 4, 'Clear', 'Special', 2, 1),
        (17, '두부한상', '한식', '서울 은평구', '02-111-0017', 'img17.jpg', 1, 'Clear', 'Comfortable', 4, 1),
        (18, '멕시칸타코', '기타', '서울 중구', '02-111-0018', 'img18.jpg', 2, 'Clear', 'Young', 2, 1),
        (19, '탄탄멘공방', '일식', '서울 금천구', '02-111-0019', 'img19.jpg', 2, 'Rain', 'Focused', 1, 1),
        (20, '포남베트남', '기타', '서울 양천구', '02-111-0020', 'img20.jpg', 2, 'Cloudy', 'Busy', 2, 1)
    ]

    cursor.executemany("""
        INSERT INTO stores (store_id, store_name, category, address, phone_number, image_url, price_level, matching_weather, matching_mood, suitable_ground_size, is_lunch_available)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, stores_data)

    # 2. 20개 식당 상세 정보 (store_details)
    # spicy_level(1~5), saltiness(1~5), revisit_rate(0~1), ad_suspicion(0~1)
    details_data = [
        (1, 1, 1, 2, 1.5, 'Cold', 'Crispy', 0.85, 5, 0.02, 4.9),
        (2, 2, 5, 4, 4.0, 'Hot', 'Chewy', 0.70, 20, 0.15, 4.1),
        (3, 3, 2, 2, 2.5, 'Warm', 'Soft', 0.90, 10, 0.01, 4.7),
        (4, 4, 1, 3, 4.0, 'Warm', 'Crispy', 0.80, 15, 0.08, 4.3),
        (5, 5, 1, 3, 3.0, 'Cold', 'Soft', 0.95, 30, 0.03, 4.6),
        (6, 6, 3, 4, 3.5, 'Hot', 'Chewy', 0.65, 10, 0.12, 3.9),
        (7, 7, 1, 2, 2.0, 'Warm', 'Soft', 0.88, 5, 0.01, 4.5),
        (8, 8, 2, 3, 3.5, 'Warm', 'Soft', 0.75, 25, 0.05, 4.4),
        (9, 9, 1, 3, 4.0, 'Warm', 'Crispy', 0.82, 15, 0.04, 4.2),
        (10, 10, 4, 4, 5.0, 'Hot', 'Chewy', 0.78, 40, 0.20, 4.0),
        (11, 11, 3, 3, 3.5, 'Hot', 'Soft', 0.85, 15, 0.03, 4.5),
        (12, 12, 1, 2, 2.0, 'Warm', 'Soft', 0.92, 10, 0.01, 4.8),
        (13, 13, 3, 4, 4.0, 'Hot', 'Chewy', 0.72, 15, 0.10, 4.1),
        (14, 14, 1, 2, 3.5, 'Hot', 'Soft', 0.89, 20, 0.02, 4.7),
        (15, 15, 2, 3, 3.5, 'Warm', 'Crispy', 0.77, 20, 0.09, 4.2),
        (16, 16, 1, 2, 2.5, 'Cold', 'Soft', 0.91, 35, 0.04, 4.6),
        (17, 17, 1, 2, 2.0, 'Warm', 'Soft', 0.87, 10, 0.01, 4.4),
        (18, 18, 3, 3, 2.5, 'Warm', 'Crispy', 0.80, 10, 0.06, 4.3),
        (19, 19, 4, 4, 4.0, 'Hot', 'Chewy', 0.84, 15, 0.05, 4.5),
        (20, 20, 2, 3, 3.0, 'Hot', 'Soft', 0.86, 10, 0.02, 4.4)
    ]

    cursor.executemany("""
        INSERT INTO store_details (detail_id, store_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, details_data)

    conn.commit()
    conn.close()
    print(f"✅ 총 20개의 식당과 상세 정보가 주입되었습니다.")

if __name__ == "__main__":
    seed_20_stores()