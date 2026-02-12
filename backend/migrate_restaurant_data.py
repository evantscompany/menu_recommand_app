import sqlite3
from datetime import datetime

def migrate_restaurant_data():
    """기존 Menu 테이블을 Restaurant + RestaurantMenu로 정규화"""
    
    conn = sqlite3.connect('restaurant_app.db')
    cursor = conn.cursor()
    
    try:
        print("🔄 데이터 정규화 시작...")
        
        # 1. 새로운 테이블들 생성
        print("📝 새로운 테이블 생성...")
        
        # restaurants 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS restaurants (
                restaurant_id INTEGER PRIMARY KEY,
                restaurant_name VARCHAR NOT NULL,
                address VARCHAR NOT NULL,
                phone_number VARCHAR,
                latitude REAL,
                longitude REAL,
                opening_hours VARCHAR,
                rating REAL DEFAULT 0.0,
                image_url VARCHAR
            )
        ''')
        
        # restaurant_menus 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS restaurant_menus (
                restaurant_menu_id INTEGER PRIMARY KEY,
                restaurant_id INTEGER NOT NULL,
                menu_id INTEGER NOT NULL,
                price INTEGER NOT NULL,
                is_available BOOLEAN DEFAULT 1,
                special_note VARCHAR,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants (restaurant_id),
                FOREIGN KEY (menu_id) REFERENCES menus (menu_id)
            )
        ''')
        
        # 2. 기존 메뉴 데이터 분석 및 식당 데이터 추출
        print("📊 기존 데이터 분석...")
        cursor.execute('''
            SELECT DISTINCT 
                COALESCE(address, '미정') as address,
                COALESCE(phone_number, '미정') as phone_number,
                COUNT(*) as menu_count
            FROM menus 
            GROUP BY address, phone_number
        ''')
        
        restaurant_groups = cursor.fetchall()
        print(f"   발견된 식당 그룹: {len(restaurant_groups)}개")
        
        # 3. 식당 데이터 생성
        restaurant_mapping = {}  # (address, phone) -> restaurant_id
        restaurant_id_counter = 1
        
        for address, phone, menu_count in restaurant_groups:
            # 식당 이름 생성 (주소 기반)
            if address != '미정':
                restaurant_name = f"{address[:10]}의 맛집" if len(address) > 10 else f"{address} 맛집"
            else:
                restaurant_name = f"맛집_{restaurant_id_counter}"
            
            # 식당 데이터 삽입
            cursor.execute('''
                INSERT INTO restaurants 
                (restaurant_id, restaurant_name, address, phone_number, rating)
                VALUES (?, ?, ?, ?, ?)
            ''', (restaurant_id_counter, restaurant_name, address, phone, 4.0))
            
            restaurant_mapping[(address, phone)] = restaurant_id_counter
            restaurant_id_counter += 1
            
            print(f"   식당 생성: {restaurant_name} (메뉴 {menu_count}개)")
        
        # 4. 메뉴-식당 연결 데이터 생성
        print("🔗 메뉴-식당 연결 데이터 생성...")
        cursor.execute('SELECT menu_id, menu_name, address, phone_number, COALESCE(price_level, 8000) FROM menus')
        menus = cursor.fetchall()
        
        for menu_id, menu_name, address, phone, price in menus:
            restaurant_id = restaurant_mapping.get((address, phone), 1)
            
            cursor.execute('''
                INSERT INTO restaurant_menus 
                (restaurant_id, menu_id, price, is_available)
                VALUES (?, ?, ?, ?)
            ''', (restaurant_id, menu_id, price, 1))
        
        # 5. 기존 Menu 테이블에서 식당 관련 컬럼 제거
        print("🗑️ 기존 Menu 테이블 정규화...")
        
        # 새로운 menus 테이블 구조로 백업
        cursor.execute('''
            CREATE TABLE menus_new AS 
            SELECT menu_id, menu_name, category, image_url,
                   matching_weather, matching_mood, suitable_ground_size,
                   is_quick_meal, is_lunch_available
            FROM menus
        ''')
        
        # 기존 테이블 삭제 및 새 테이블로 교체
        cursor.execute('DROP TABLE menus')
        cursor.execute('ALTER TABLE menus_new RENAME TO menus')
        
        # 6. 결과 확인
        print("\n✅ 마이그레이션 완료! 결과 확인:")
        
        cursor.execute('SELECT COUNT(*) FROM restaurants')
        restaurant_count = cursor.fetchone()[0]
        print(f"   식당 수: {restaurant_count}")
        
        cursor.execute('SELECT COUNT(*) FROM restaurant_menus')
        connection_count = cursor.fetchone()[0]
        print(f"   메뉴-식당 연결 수: {connection_count}")
        
        cursor.execute('SELECT COUNT(*) FROM menus')
        menu_count = cursor.fetchone()[0]
        print(f"   메뉴 수: {menu_count}")
        
        # 샘플 데이터 확인
        print("\n📋 샘플 데이터:")
        cursor.execute('''
            SELECT r.restaurant_name, m.menu_name, rm.price 
            FROM restaurants r
            JOIN restaurant_menus rm ON r.restaurant_id = rm.restaurant_id
            JOIN menus m ON rm.menu_id = m.menu_id
            LIMIT 5
        ''')
        
        samples = cursor.fetchall()
        for restaurant, menu, price in samples:
            print(f"   {restaurant} - {menu} ({price}원)")
        
        conn.commit()
        print("\n🎉 데이터 정규화 성공 완료!")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_restaurant_data()
