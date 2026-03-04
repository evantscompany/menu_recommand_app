"""
간단한 TiDB Cloud 테이블 확인
"""

import pymysql

def check_tables():
    """MySQL 테이블 확인"""
    try:
        # 직접 연결
        conn = pymysql.connect(
            host="gateway01.ap-northeast-1.prod.aws.tidbcloud.com",
            port=4000,
            user="3bJdto8FKWk47Fu.root",
            password="NWOZOcYDO8W5nMk2",
            database="test",
            ssl={"ssl": True}
        )
        
        cursor = conn.cursor()
        
        # 테이블 목록 조회
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("📋 TiDB Cloud 테이블 목록:")
        for table in tables:
            table_name = table[0]
            print(f"  - {table_name}")
            
            # 레코드 수 확인
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"    {count}개 레코드")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ MySQL 확인 실패: {e}")
        return False

if __name__ == "__main__":
    check_tables()
