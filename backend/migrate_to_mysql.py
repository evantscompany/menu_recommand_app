"""
SQLite에서 TiDB Cloud MySQL로 데이터 마이그레이션 스크립트
"""

import sqlite3
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sys
from datetime import datetime

# MySQL 연결 설정 (TiDB Cloud)
MYSQL_HOST = os.getenv("TIDB_HOST", "gateway01.ap-northeast-1.prod.aws.tidbcloud.com")
MYSQL_PORT = os.getenv("TIDB_PORT", "4000")
MYSQL_USER = os.getenv("TIDB_USER", "3bJdto8FKWk47Fu.root")
MYSQL_PASSWORD = os.getenv("TIDB_PASSWORD", "NWOZOcYDO8W5nMk2")
MYSQL_DATABASE = os.getenv("TIDB_DATABASE", "test")

# SQLite 파일 경로
SQLITE_DB_PATH = "./restaurant_app.db"

def migrate_data():
    """SQLite 데이터를 MySQL로 마이그레이션"""
    
    # 1. SQLite 연결
    try:
        sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
        sqlite_conn.row_factory = sqlite3.Row
        print("✅ SQLite 데이터베이스 연결 성공")
    except Exception as e:
        print(f"❌ SQLite 연결 실패: {e}")
        return False
    
    # 2. MySQL 연결
    try:
        mysql_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
        mysql_engine = create_engine(mysql_url)
        mysql_session = sessionmaker(bind=mysql_engine)()
        print("✅ TiDB Cloud MySQL 연결 성공")
    except Exception as e:
        print(f"❌ MySQL 연결 실패: {e}")
        return False
    
    try:
        # 3. 테이블 구조 확인 및 데이터 마이그레이션
        
        # user_accounts 테이블 마이그레이션
        print("\n� user_accounts 테이블 마이그레이션 중...")
        cursor = sqlite_conn.execute("SELECT * FROM user_accounts")
        for row in cursor.fetchall():
            try:
                # created_at 변환 (SQLite 문자열 → MySQL datetime)
                created_at = row['created_at']
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                
                insert_sql = text("""
                    INSERT INTO user_accounts (username, email, nickname, hashed_password, created_at) 
                    VALUES (:username, :email, :nickname, :hashed_password, :created_at)
                """)
                
                mysql_session.execute(insert_sql, {
                    'username': row['username'],
                    'email': row['email'],
                    'nickname': row['nickname'],
                    'hashed_password': row['hashed_password'],
                    'created_at': created_at
                })
            except Exception as e:
                print(f"  ⚠️ user_accounts 데이터 삽입 중 오류: {e}")
        
        # menus 테이블 마이그레이션
        print("\n🍽️ menus 테이블 마이그레이션 중...")
        cursor = sqlite_conn.execute("SELECT * FROM menus")
        for row in cursor.fetchall():
            try:
                insert_sql = text("""
                    INSERT INTO menus (menu_name, category, image_url, price, matching_weather, 
                                   suitable_ground_size, is_quick_meal, is_lunch_available) 
                    VALUES (:menu_name, :category, :image_url, :price, :matching_weather, 
                           :suitable_ground_size, :is_quick_meal, :is_lunch_available)
                """)
                
                mysql_session.execute(insert_sql, {
                    'menu_name': row['menu_name'],
                    'category': row['category'],
                    'image_url': row['image_url'],
                    'price': row['price'],
                    'matching_weather': row['matching_weather'],
                    'suitable_ground_size': row['suitable_ground_size'],
                    'is_quick_meal': bool(row['is_quick_meal']),
                    'is_lunch_available': bool(row['is_lunch_available'])
                })
            except Exception as e:
                print(f"  ⚠️ menus 데이터 삽입 중 오류: {e}")
        
        # menu_details 테이블 마이그레이션
        print("\n🍽️ menu_details 테이블 마이그레이션 중...")
        cursor = sqlite_conn.execute("SELECT * FROM menu_details")
        for row in cursor.fetchall():
            try:
                insert_sql = text("""
                    INSERT INTO menu_details (menu_id, spicy_level, texture, heaviness, 
                                          temperature, cooking_time, description) 
                    VALUES (:menu_id, :spicy_level, :texture, :heaviness, 
                           :temperature, :cooking_time, :description)
                """)
                
                mysql_session.execute(insert_sql, {
                    'menu_id': row['menu_id'],
                    'spicy_level': row['spicy_level'],
                    'texture': row['texture'],
                    'heaviness': row['heaviness'],
                    'temperature': row['temperature'],
                    'cooking_time': row['cooking_time'],
                    'description': row['description']
                })
            except Exception as e:
                print(f"  ⚠️ menu_details 데이터 삽입 중 오류: {e}")
        
        # user_histories 테이블 마이그레이션
        print("\n📜 user_histories 테이블 마이그레이션 중...")
        cursor = sqlite_conn.execute("SELECT * FROM user_histories")
        for row in cursor.fetchall():
            try:
                insert_sql = text("""
                    INSERT INTO user_histories (user_id, menu_id, selected_at, feedback_score) 
                    VALUES (:user_id, :menu_id, :selected_at, :feedback_score)
                """)
                
                mysql_session.execute(insert_sql, {
                    'user_id': row['user_id'],
                    'menu_id': row['menu_id'],
                    'selected_at': row['selected_at'],
                    'feedback_score': row['feedback_score']
                })
            except Exception as e:
                print(f"  ⚠️ user_histories 데이터 삽입 중 오류: {e}")
        
        # recommendation_feedbacks 테이블 마이그레이션
        print("\n📝 recommendation_feedbacks 테이블 마이그레이션 중...")
        cursor = sqlite_conn.execute("SELECT * FROM recommendation_feedbacks")
        for row in cursor.fetchall():
            try:
                insert_sql = text("""
                    INSERT INTO recommendation_feedbacks (menu_id, feedback_type, score, created_at) 
                    VALUES (:menu_id, :feedback_type, :score, :created_at)
                """)
                
                mysql_session.execute(insert_sql, {
                    'menu_id': row['menu_id'],
                    'feedback_type': row['feedback_type'],
                    'score': row['score'],
                    'created_at': row['created_at']
                })
            except Exception as e:
                print(f"  ⚠️ recommendation_feedbacks 데이터 삽입 중 오류: {e}")
        
        # 변경사항 커밋
        mysql_session.commit()
        print("\n✅ 데이터 마이그레이션 완료!")
        
        # 4. 마이그레이션 결과 확인
        print("\n📊 마이그레이션 결과 확인:")
        tables = ['user_accounts', 'menus', 'user_profiles', 'menu_details', 'user_histories', 'recommendation_feedbacks']
        for table in tables:
            try:
                result = mysql_session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.fetchone()[0]
                print(f"  {table}: {count}개 레코드")
            except Exception as e:
                print(f"  {table}: 확인 실패 - {e}")
        
    except Exception as e:
        print(f"❌ 마이그레이션 중 오류 발생: {e}")
        mysql_session.rollback()
        return False
    
    finally:
        sqlite_conn.close()
        mysql_session.close()
    
    return True

if __name__ == "__main__":
    print("🚀 SQLite → TiDB Cloud MySQL 데이터 마이그레이션 시작")
    print("=" * 50)
    
    # 환경 변수 확인
    if not all([MYSQL_USER, MYSQL_PASSWORD]):
        print("❌ 환경 변수 설정 필요:")
        print("  TIDB_USER, TIDB_PASSWORD 환경 변수를 설정해주세요.")
        print("  또는 .env.production 파일을 생성하세요.")
        sys.exit(1)
    
    # 마이그레이션 실행
    if migrate_data():
        print("\n🎉 마이그레이션 성공 완료!")
    else:
        print("\n💥 마이그레이션 실패!")
        sys.exit(1)
