#!/usr/bin/env python3
"""
프론트엔드 담당자용 메뉴 데이터 추출 스크립트
restaurant_app.db의 menus와 menu_details 테이블 데이터를 SQL 파일로 추출합니다.
"""

import sqlite3
import os
from datetime import datetime

def export_menu_data():
    """메뉴와 메뉴 상세 데이터를 SQL 파일로 추출"""
    
    # DB 파일 경로
    db_path = "restaurant_app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ 데이터베이스 파일을 찾을 수 없습니다: {db_path}")
        return
    
    # 출력 파일명 (타임스탬프 포함)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"menu_data_for_frontend_{timestamp}.sql"
    
    try:
        # DB 연결
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # SQL 파일 내용 초기화
        sql_content = f"""-- 메뉴 데이터 추출 (생성일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
-- 프론트엔드 담당자용 데이터
-- 실행 전: 기존 테이블이 있다면 삭제 후 생성

-- 기존 테이블 삭제 (선택사항)
-- DROP TABLE IF EXISTS menu_details;
-- DROP TABLE IF EXISTS menus;

-- 테이블 생성
CREATE TABLE IF NOT EXISTS menus (
    menu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    image_url VARCHAR(500),
    price INTEGER DEFAULT 8000,
    matching_weather VARCHAR(100),
    suitable_ground_size INTEGER,
    is_quick_meal BOOLEAN DEFAULT 1,
    is_lunch_available BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS menu_details (
    detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_id INTEGER NOT NULL,
    spicy_level INTEGER DEFAULT 1,
    saltiness_level INTEGER DEFAULT 3,
    heaviness REAL DEFAULT 0.5,
    serving_temperature VARCHAR(50) DEFAULT 'hot',
    texture VARCHAR(50) DEFAULT 'normal',
    revisit_rate REAL DEFAULT 0.8,
    avg_waiting_time INTEGER DEFAULT 15,
    ad_suspicion_index REAL DEFAULT 0.1,
    real_satisfaction_score REAL DEFAULT 4.0,
    FOREIGN KEY (menu_id) REFERENCES menus (menu_id)
);

-- 메뉴 데이터 삽입
"""

        # menus 테이블 데이터 추출
        cursor.execute("""
            SELECT menu_id, menu_name, category, image_url, price, 
                   matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available
            FROM menus 
            ORDER BY menu_id
        """)
        
        menus_data = cursor.fetchall()
        print(f"📊 메뉴 데이터 {len(menus_data)}개 추출 중...")
        
        for row in menus_data:
            (menu_id, menu_name, category, image_url, price, 
             matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) = row
            
            # SQL 인젝션 방지를 위한 문자열 처리
            menu_name = menu_name.replace("'", "''") if menu_name else ''
            category = category.replace("'", "''") if category else ''
            image_url = image_url.replace("'", "''") if image_url else ''
            matching_weather = matching_weather.replace("'", "''") if matching_weather else ''
            
            sql_content += f"""INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES ({menu_id}, '{menu_name}', '{category}', '{image_url}', {price}, '{matching_weather}', {suitable_ground_size if suitable_ground_size is not None else 'NULL'}, {1 if is_quick_meal else 0}, {1 if is_lunch_available else 0});

"""
        
        # menu_details 테이블 데이터 추출
        cursor.execute("""
            SELECT menu_id, spicy_level, saltiness_level, heaviness,
                   serving_temperature, texture, revisit_rate, avg_waiting_time,
                   ad_suspicion_index, real_satisfaction_score
            FROM menu_details 
            ORDER BY menu_id
        """)
        
        details_data = cursor.fetchall()
        print(f"📋 메뉴 상세 데이터 {len(details_data)}개 추출 중...")
        
        for row in details_data:
            (menu_id, spicy_level, saltiness_level, heaviness,
             serving_temperature, texture, revisit_rate, avg_waiting_time,
             ad_suspicion_index, real_satisfaction_score) = row
            
            # 문자열 처리
            serving_temperature = serving_temperature.replace("'", "''") if serving_temperature else 'hot'
            texture = texture.replace("'", "''") if texture else 'normal'
            
            sql_content += f"""INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES ({menu_id}, {spicy_level}, {saltiness_level}, {heaviness}, '{serving_temperature}', '{texture}', {revisit_rate}, {avg_waiting_time}, {ad_suspicion_index}, {real_satisfaction_score});

"""
        
        # 인덱스 생성
        sql_content += """
-- 인덱스 생성 (성능 최적화)
CREATE INDEX IF NOT EXISTS idx_menus_category ON menus(category);
CREATE INDEX IF NOT EXISTS idx_menus_name ON menus(menu_name);
CREATE INDEX IF NOT EXISTS idx_menus_price ON menus(price);
CREATE INDEX IF NOT EXISTS idx_menu_details_menu_id ON menu_details(menu_id);

-- 데이터 추출 완료
-- 총 메뉴 수: """ + str(len(menus_data)) + """
-- 총 상세 정보 수: """ + str(len(details_data)) + """
"""

        # 파일 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sql_content)
        
        print(f"✅ SQL 파일 생성 완료: {output_file}")
        print(f"📁 파일 위치: {os.path.abspath(output_file)}")
        print(f"📊 메뉴 데이터: {len(menus_data)}개")
        print(f"📋 상세 정보: {len(details_data)}개")
        print(f"\n📌 프론트엔드 담당자 안내:")
        print(f"   1. 이 SQL 파일을 데이터베이스에서 실행하세요")
        print(f"   2. SQLite: sqlite3 your_database.db < {output_file}")
        print(f"   3. MySQL: mysql -u username -p database_name < {output_file}")
        print(f"   4. PostgreSQL: psql -d database_name -f {output_file}")
        
    except Exception as e:
        print(f"❌ 데이터 추출 중 오류 발생: {e}")
        
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("🚀 프론트엔드용 메뉴 데이터 추출 시작...")
    export_menu_data()
    print("✅ 작업 완료!")
