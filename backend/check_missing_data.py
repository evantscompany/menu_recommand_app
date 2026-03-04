"""
마이그레이션되지 않은 데이터 확인
"""

import sqlite3
import pymysql

def check_missing_data():
    """SQLite와 TiDB Cloud 데이터 비교"""
    
    # 1. SQLite 데이터 확인
    try:
        sqlite_conn = sqlite3.connect('restaurant_app.db')
        sqlite_conn.row_factory = sqlite3.Row
        
        print("📋 SQLite 원본 데이터:")
        tables = ['user_accounts', 'menus', 'user_profiles', 'menu_details', 'user_histories', 'recommendation_feedbacks']
        
        for table in tables:
            try:
                cursor = sqlite_conn.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count}개 레코드")
            except Exception as e:
                print(f"  {table}: 확인 실패 - {e}")
        
        sqlite_conn.close()
        
    except Exception as e:
        print(f"❌ SQLite 확인 실패: {e}")
        return
    
    # 2. TiDB Cloud 데이터 확인
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
        
        print("\n📋 TiDB Cloud 마이그레이션된 데이터:")
        
        for table in tables:
            try:
                mysql_cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = mysql_cursor.fetchone()[0]
                print(f"  {table}: {count}개 레코드")
            except Exception as e:
                print(f"  {table}: 확인 실패 - {e}")
        
        mysql_conn.close()
        
    except Exception as e:
        print(f"❌ TiDB Cloud 확인 실패: {e}")
        return
    
    # 3. menu_details 상세 확인
    print("\n🔍 menu_details 테이블 상세 확인:")
    
    try:
        sqlite_conn = sqlite3.connect('restaurant_app.db')
        sqlite_conn.row_factory = sqlite3.Row
        
        cursor = sqlite_conn.execute("SELECT * FROM menu_details LIMIT 3")
        print("  SQLite menu_details 샘플 데이터:")
        for row in cursor.fetchall():
            print(f"    {dict(row)}")
        
        sqlite_conn.close()
        
    except Exception as e:
        print(f"❌ SQLite menu_details 확인 실패: {e}")

if __name__ == "__main__":
    check_missing_data()
