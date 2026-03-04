"""
user_profiles 테이블 확인
"""
import os
import sys
sys.path.append('.')

from app.database_mysql import engine, SessionLocal
from sqlalchemy import text

def check_user_profiles():
    """user_profiles 테이블 확인"""
    
    print("🔍 user_profiles 테이블 확인")
    print("=" * 50)
    
    try:
        # 환경 변수 설정
        os.environ["TIDB_HOST"] = "gateway01.ap-northeast-1.prod.aws.tidbcloud.com"
        os.environ["TIDB_PORT"] = "4000"
        os.environ["TIDB_USER"] = "3bJdto8FKWk47Fu.root"
        os.environ["TIDB_PASSWORD"] = "NWOZOcYDO8W5nMk2"
        os.environ["TIDB_DATABASE"] = "test"
        
        with engine.connect() as conn:
            # 1. 테이블 존재 확인
            result = conn.execute(text("SHOW TABLES LIKE 'user_profiles'"))
            tables = result.fetchall()
            
            print(f"📋 테이블 존재 여부: {len(tables)}개")
            for table in tables:
                print(f"   - {table[0]}")
            
            # 2. 테이블 구조 확인
            if len(tables) > 0:
                result = conn.execute(text("DESCRIBE user_profiles"))
                columns = result.fetchall()
                
                print(f"\n📋 테이블 구조 ({len(columns)}개 컬럼):")
                for col in columns:
                    print(f"   - {col[0]}: {col[1]}")
                
                # 3. 데이터 개수 확인
                result = conn.execute(text("SELECT COUNT(*) FROM user_profiles"))
                count = result.fetchone()[0]
                print(f"\n📊 전체 레코드 수: {count}개")
                
                # 4. aaa 사용자의 profile 확인
                result = conn.execute(text("""
                    SELECT ua.user_id, ua.username, up.profile_id, up.dietary_label, up.spicy_threshold
                    FROM user_accounts ua
                    LEFT JOIN user_profiles up ON ua.user_id = up.user_id
                    WHERE ua.username = 'aaa'
                """))
                
                aaa_profile = result.fetchone()
                if aaa_profile:
                    print(f"\n👤 aaa 사용자 profile:")
                    print(f"   user_id: {aaa_profile[0]}")
                    print(f"   username: {aaa_profile[1]}")
                    print(f"   profile_id: {aaa_profile[2]}")
                    print(f"   dietary_label: {aaa_profile[3]}")
                    print(f"   spicy_threshold: {aaa_profile[4]}")
                else:
                    print("\n❌ aaa 사용자 profile을 찾을 수 없습니다")
                    
            else:
                print("\n❌ user_profiles 테이블이 존재하지 않습니다")
            
    except Exception as e:
        print(f"❌ 확인 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_user_profiles()
