"""
TiDB Cloud 데이터베이스 연결 및 관계 확인 (간단 버전)
"""
import os
import sys
sys.path.append('.')

from app.database_mysql import engine, SessionLocal
from sqlalchemy import text

def check_tidb_simple():
    """TiDB Cloud 데이터베이스 연결 및 관계 확인"""
    
    print("🔍 TiDB Cloud 데이터베이스 연결 및 관계 확인")
    print("=" * 60)
    
    try:
        # 환경 변수 설정
        os.environ["TIDB_HOST"] = "gateway01.ap-northeast-1.prod.aws.tidbcloud.com"
        os.environ["TIDB_PORT"] = "4000"
        os.environ["TIDB_USER"] = "3bJdto8FKWk47Fu.root"
        os.environ["TIDB_PASSWORD"] = "NWOZOcYDO8W5nMk2"
        os.environ["TIDB_DATABASE"] = "test"
        
        with engine.connect() as conn:
            print("✅ TiDB Cloud 연결 성공")
            
            # 1. 전체 테이블 목록 확인
            print(f"\n📋 전체 테이블 목록:")
            result = conn.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            
            for table in tables:
                print(f"   - {table[0]}")
            
            # 2. 데이터 개수 확인
            print(f"\n📊 테이블별 데이터 개수:")
            
            tables_to_check = ['user_accounts', 'user_profiles', 'menus', 'menu_details']
            for table in tables_to_check:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    print(f"   - {table}: {count}개 레코드")
                except Exception as e:
                    print(f"   - {table}: 확인 실패 - {e}")
            
            # 3. user_accounts 구조 확인
            print(f"\n📋 user_accounts 테이블 구조:")
            result = conn.execute(text("DESCRIBE user_accounts"))
            columns = result.fetchall()
            
            for col in columns:
                print(f"   - {col[0]}: {col[1]}")
            
            # 4. user_profiles 구조 확인
            print(f"\n📋 user_profiles 테이블 구조:")
            result = conn.execute(text("DESCRIBE user_profiles"))
            columns = result.fetchall()
            
            for col in columns:
                print(f"   - {col[0]}: {col[1]}")
            
            # 5. aaa 사용자 확인
            print(f"\n👤 aaa 사용자 확인:")
            result = conn.execute(text("SELECT user_id, username, email FROM user_accounts WHERE username = 'aaa'"))
            aaa_account = result.fetchone()
            
            if aaa_account:
                print(f"   ✅ user_accounts 찾음:")
                print(f"      user_id: {aaa_account[0]}")
                print(f"      username: {aaa_account[1]}")
                print(f"      email: {aaa_account[2]}")
                
                # user_profiles 확인
                user_id = aaa_account[0]
                result = conn.execute(text(f"SELECT profile_id, user_id, dietary_label, spicy_threshold FROM user_profiles WHERE user_id = {user_id}"))
                aaa_profile = result.fetchone()
                
                if aaa_profile:
                    print(f"   ✅ user_profiles 찾음:")
                    print(f"      profile_id: {aaa_profile[0]}")
                    print(f"      user_id: {aaa_profile[1]}")
                    print(f"      dietary_label: {aaa_profile[2]}")
                    print(f"      spicy_threshold: {aaa_profile[3]}")
                    
                    print(f"   ✅ 관계 확인:")
                    print(f"      user_accounts.user_id ({aaa_account[0]}) ↔ user_profiles.user_id ({aaa_profile[1]})")
                    print(f"      외래 키 관계 정상!")
                    
                else:
                    print(f"   ❌ user_profiles에서 profile을 찾을 수 없음")
            else:
                print(f"   ❌ user_accounts에서 aaa 사용자를 찾을 수 없음")
            
            # 6. 최신 사용자 목록 확인
            print(f"\n📋 최신 사용자 목록 (최근 5개):")
            result = conn.execute(text("""
                SELECT ua.user_id, ua.username, ua.email, up.profile_id
                FROM user_accounts ua
                LEFT JOIN user_profiles up ON ua.user_id = up.user_id
                ORDER BY ua.user_id DESC
                LIMIT 5
            """))
            
            recent_users = result.fetchall()
            for user in recent_users:
                profile_status = f"✅" if user[3] else "❌"
                print(f"   {profile_status} ID:{user[0]} | {user[1]} | {user[2]} | profile_id:{user[3]}")
            
    except Exception as e:
        print(f"❌ 확인 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_tidb_simple()
