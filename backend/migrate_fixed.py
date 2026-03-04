"""
수정된 SQLite → TiDB Cloud MySQL 데이터 마이그레이션 스크립트
"""

import sqlite3
import os
import pymysql
from datetime import datetime

def migrate_data_fixed():
    """SQLite 데이터를 MySQL로 마이그레이션 (수정 버전)"""
    
    # 1. SQLite 연결
    try:
        sqlite_conn = sqlite3.connect('restaurant_app.db')
        sqlite_conn.row_factory = sqlite3.Row
        print("✅ SQLite 데이터베이스 연결 성공")
    except Exception as e:
        print(f"❌ SQLite 연결 실패: {e}")
        return False
    
    # 2. MySQL 연결
    try:
        mysql_conn = pymysql.connect(
            host="gateway01.ap-northeast-1.prod.aws.tidbcloud.com",
            port=4000,
            user="3bJdto8FKWk47Fu.root",
            password="NWOZOcYDO8W5nMk2",
            database="test",
            ssl={"ssl": True},
            charset='utf8mb4'
        )
        mysql_cursor = mysql_conn.cursor()
        print("✅ TiDB Cloud MySQL 연결 성공")
    except Exception as e:
        print(f"❌ MySQL 연결 실패: {e}")
        return False
    
    try:
        # 3. user_accounts 마이그레이션
        print("\n👤 user_accounts 테이블 마이그레이션 중...")
        cursor = sqlite_conn.execute("SELECT * FROM user_accounts")
        for row in cursor.fetchall():
            try:
                insert_sql = """
                    INSERT INTO user_accounts (username, email, nickname, hashed_password, created_at) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                mysql_cursor.execute(insert_sql, (
                    row['username'],
                    row['email'], 
                    row['nickname'],
                    row['hashed_password'],
                    row['created_at']
                ))
            except Exception as e:
                print(f"  ⚠️ user_accounts 데이터 삽입 중 오류: {e}")
        
        # 4. menus 마이그레이션
        print("\n🍽️ menus 테이블 마이그레이션 중...")
        cursor = sqlite_conn.execute("SELECT * FROM menus")
        for row in cursor.fetchall():
            try:
                insert_sql = """
                    INSERT INTO menus (menu_name, category, image_url, price, matching_weather, 
                                   suitable_ground_size, is_quick_meal, is_lunch_available) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                mysql_cursor.execute(insert_sql, (
                    row['menu_name'],
                    row['category'],
                    row['image_url'],
                    row['price'],
                    row['matching_weather'],
                    row['suitable_ground_size'],
                    bool(row['is_quick_meal']),
                    bool(row['is_lunch_available'])
                ))
            except Exception as e:
                print(f"  ⚠️ menus 데이터 삽입 중 오류: {e}")
        
        # 5. user_profiles 마이그레이션
        print("\n👤 user_profiles 테이블 마이그레이션 중...")
        cursor = sqlite_conn.execute("SELECT * FROM user_profiles")
        for row in cursor.fetchall():
            try:
                insert_sql = """
                    INSERT INTO user_profiles (user_id, dietary_label, allergies, spicy_threshold, 
                                         saltiness_preference, lunch_budget_max, is_adventurous) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                mysql_cursor.execute(insert_sql, (
                    row['user_id'],
                    row['dietary_label'],
                    row['allergies'],
                    row['spicy_threshold'],
                    row['saltiness_preference'],
                    row['lunch_budget_max'],
                    bool(row['is_adventurous'])
                ))
            except Exception as e:
                print(f"  ⚠️ user_profiles 데이터 삽입 중 오류: {e}")
        
        # 6. menu_details 마이그레이션
        print("\n🍽️ menu_details 테이블 마이그레이션 중...")
        cursor = sqlite_conn.execute("SELECT * FROM menu_details")
        for row in cursor.fetchall():
            try:
                insert_sql = """
                    INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, 
                                          serving_temperature, texture, revisit_rate, avg_waiting_time, 
                                          ad_suspicion_index, real_satisfaction_score) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                mysql_cursor.execute(insert_sql, (
                    row['menu_id'],
                    row['spicy_level'],
                    row['saltiness_level'],
                    row['heaviness'],
                    row['serving_temperature'],
                    row['texture'],
                    row['revisit_rate'],
                    row['avg_waiting_time'],
                    row['ad_suspicion_index'],
                    row['real_satisfaction_score']
                ))
            except Exception as e:
                print(f"  ⚠️ menu_details 데이터 삽입 중 오류: {e}")
        
        # 7. user_histories 마이그레이션
        print("\n📜 user_histories 테이블 마이그레이션 중...")
        cursor = sqlite_conn.execute("SELECT * FROM user_histories")
        for row in cursor.fetchall():
            try:
                insert_sql = """
                    INSERT INTO user_histories (user_id, menu_id, last_visit_date, visit_count, 
                                           last_eaten_category, last_eaten_menu, recent_menus, 
                                           user_rating, is_revisit_intended, feedback_comment) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                mysql_cursor.execute(insert_sql, (
                    row['user_id'],
                    row['menu_id'],
                    row['last_visit_date'],
                    row['visit_count'],
                    row['last_eaten_category'],
                    row['last_eaten_menu'],
                    row['recent_menus'],
                    row['user_rating'],
                    bool(row['is_revisit_intended']),
                    row['feedback_comment']
                ))
            except Exception as e:
                print(f"  ⚠️ user_histories 데이터 삽입 중 오류: {e}")
        
        # 8. recommendation_feedbacks 마이그레이션
        print("\n📝 recommendation_feedbacks 테이블 마이그레이션 중...")
        cursor = sqlite_conn.execute("SELECT * FROM recommendation_feedbacks")
        for row in cursor.fetchall():
            try:
                insert_sql = """
                    INSERT INTO recommendation_feedbacks (user_id, menu_name, feedback_type, 
                                                     category, score, created_at) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                mysql_cursor.execute(insert_sql, (
                    row['user_id'],
                    row['menu_name'],
                    row['feedback_type'],
                    row['category'],
                    row['score'],
                    row['created_at']
                ))
            except Exception as e:
                print(f"  ⚠️ recommendation_feedbacks 데이터 삽입 중 오류: {e}")
        
        # 변경사항 커밋
        mysql_conn.commit()
        print("\n✅ 데이터 마이그레이션 완료!")
        
        # 9. 마이그레이션 결과 확인
        print("\n📊 마이그레이션 결과 확인:")
        tables = ['user_accounts', 'menus', 'user_profiles', 'menu_details', 'user_histories', 'recommendation_feedbacks']
        for table in tables:
            try:
                mysql_cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = mysql_cursor.fetchone()[0]
                print(f"  {table}: {count}개 레코드")
            except Exception as e:
                print(f"  {table}: 확인 실패 - {e}")
        
    except Exception as e:
        print(f"❌ 마이그레이션 중 오류 발생: {e}")
        mysql_conn.rollback()
        return False
    
    finally:
        sqlite_conn.close()
        mysql_conn.close()
    
    return True

if __name__ == "__main__":
    print("🚀 SQLite → TiDB Cloud MySQL 데이터 마이그레이션 시작 (수정 버전)")
    print("=" * 60)
    
    if migrate_data_fixed():
        print("\n🎉 마이그레이션 성공 완료!")
    else:
        print("\n💥 마이그레이션 실패!")
