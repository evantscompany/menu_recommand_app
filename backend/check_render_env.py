"""
Render 환경변수 연결 테스트
"""
import os
import pymysql

def test_render_db_connection():
    """Render 환경변수로 TiDB Cloud 연결 테스트"""
    
    print("🔍 Render 환경변수 데이터베이스 연결 테스트")
    print("=" * 50)
    
    # 환경변수 확인
    print("📋 환경변수 상태:")
    env_vars = ["TIDB_HOST", "TIDB_PORT", "TIDB_USER", "TIDB_PASSWORD", "TIDB_DATABASE"]
    for var in env_vars:
        value = os.getenv(var)
        if value:
            masked_value = value[:10] + "..." if len(value) > 10 else value
            print(f"   {var}: {masked_value}")
        else:
            print(f"   {var}: ❌ 설정되지 않음")
    
    # TiDB Cloud 연결 테스트
    try:
        print("\n🔌 TiDB Cloud 연결 시도...")
        conn = pymysql.connect(
            host=os.getenv("TIDB_HOST"),
            port=int(os.getenv("TIDB_PORT", "4000")),
            user=os.getenv("TIDB_USER"),
            password=os.getenv("TIDB_PASSWORD"),
            database=os.getenv("TIDB_DATABASE"),
            ssl={"ssl": True},
            charset='utf8mb4'
        )
        
        cursor = conn.cursor()
        
        # 연결 성공
        print("✅ TiDB Cloud 연결 성공!")
        
        # 버전 확인
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"   MySQL 버전: {version}")
        
        # 테이블 목록 확인
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"   테이블 수: {len(tables)}개")
        
        # 데이터 확인
        print("\n📊 테이블 데이터 확인:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   {table_name}: {count}개 레코드")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ TiDB Cloud 연결 실패: {e}")
        return False

if __name__ == "__main__":
    test_render_db_connection()
