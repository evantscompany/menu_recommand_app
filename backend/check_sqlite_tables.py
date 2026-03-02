import sqlite3

def check_tables():
    """SQLite 데이터베이스 테이블 확인"""
    try:
        conn = sqlite3.connect('restaurant_app.db')
        cursor = conn.cursor()
        
        # 테이블 목록 조회
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        print("📋 SQLite 테이블 목록:")
        for table in tables:
            print(f"  - {table}")
        
        # 각 테이블의 레코드 수 확인
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count}개 레코드")
            except Exception as e:
                print(f"  {table}: 확인 실패 - {e}")
        
        conn.close()
        return tables
        
    except Exception as e:
        print(f"❌ SQLite 확인 실패: {e}")
        return []

if __name__ == "__main__":
    check_tables()
