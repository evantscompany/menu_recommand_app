"""
menu_details 마이그레이션 디버깅 스크립트
"""

import sqlite3
import pymysql

def debug_menu_details():
    """menu_details 마이그레이션 문제 디버깅"""
    
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
        # 3. 데이터 구조 확인
        print("\n🔍 데이터 구조 확인:")
        cursor = sqlite_conn.execute("SELECT * FROM menu_details LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            print(f"  SQLite 컬럼 수: {len(row)}")
            print(f"  컬럼 이름: {list(row.keys())}")
            
            for i, value in enumerate(row):
                print(f"    [{i}] {list(row.keys())[i]}: {value} (타입: {type(value)})")
        
        # 4. 테이블 구조 확인
        print("\n🔍 MySQL 테이블 구조 확인:")
        mysql_cursor.execute("DESCRIBE menu_details")
        columns = mysql_cursor.fetchall()
        for col in columns:
            print(f"  MySQL 컬럼: {col}")
        
        # 5. 가장 간단한 INSERT 시도
        print("\n🧪 가장 간단한 INSERT 시도:")
        
        if row:
            try:
                # 첫 번째 데이터로 가장 간단한 INSERT
                simple_insert = """INSERT INTO menu_details (detail_id, menu_id) VALUES (%s, %s)"""
                mysql_cursor.execute(simple_insert, (row[0], row[1]))
                mysql_conn.commit()
                print("  ✅ 간단 INSERT 성공!")
                return True
                
            except Exception as e:
                print(f"  ❌ 간단 INSERT 실패: {type(e).__name__}: {e}")
                
                # PyMySQL 버전 확인
                print(f"\n📋 PyMySQL 정보:")
                print(f"  버전: {pymysql.__version__}")
                print(f"  MySQL 연결 정보: {mysql_conn.get_host_info()}")
                
                # 문자열 인코딩 테스트
                try:
                    test_sql = "SELECT %s"
                    test_cursor = mysql_conn.cursor()
                    test_cursor.execute(test_sql, ("테스트",))
                    print("  ✅ 문자열 인코딩 정상")
                except Exception as encoding_error:
                    print(f"  ❌ 문자열 인코딩 오류: {encoding_error}")
                
                return False
        
    except Exception as e:
        print(f"❌ 디버깅 중 오류: {e}")
        return False
    
    finally:
        sqlite_conn.close()
        mysql_conn.close()

if __name__ == "__main__":
    print("🔍 menu_details 마이그레이션 디버깅 시작")
    print("=" * 50)
    
    debug_menu_details()
