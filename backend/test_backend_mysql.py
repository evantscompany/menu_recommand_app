"""
TiDB Cloud 백엔드 연동 테스트
"""

import os
from app.database_mysql import engine, SessionLocal
from sqlalchemy import text
from app.models import UserAccount, Menu, UserProfile, MenuDetail

def test_database_connection():
    """데이터베이스 연결 및 데이터 확인"""
    try:
        # 환경 변수 설정
        os.environ["TIDB_HOST"] = "gateway01.ap-northeast-1.prod.aws.tidbcloud.com"
        os.environ["TIDB_PORT"] = "4000"
        os.environ["TIDB_USER"] = "3bJdto8FKWk47Fu.root"
        os.environ["TIDB_PASSWORD"] = "NWOZOcYDO8W5nMk2"
        os.environ["TIDB_DATABASE"] = "test"
        
        print("🔍 TiDB Cloud 데이터베이스 연결 테스트")
        print("=" * 50)
        
        # 1. 연결 테스트
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            print(f"✅ 데이터베이스 연결 성공!")
            print(f"📊 MySQL 버전: {version}")
        
        # 2. 테이블 데이터 확인
        db = SessionLocal()
        try:
            print("\n📋 테이블 데이터 확인:")
            
            # user_accounts
            users = db.query(UserAccount).all()
            print(f"  👤 user_accounts: {len(users)}개 레코드")
            if users:
                print(f"     - 첫번째 사용자: {users[0].username} ({users[0].email})")
            
            # menus
            menus = db.query(Menu).all()
            print(f"  🍽️ menus: {len(menus)}개 레코드")
            if menus:
                print(f"     - 첫번째 메뉴: {menus[0].menu_name} ({menus[0].category})")
            
            # user_profiles
            profiles = db.query(UserProfile).all()
            print(f"  👤 user_profiles: {len(profiles)}개 레코드")
            
            # menu_details
            details = db.query(MenuDetail).all()
            print(f"  📝 menu_details: {len(details)}개 레코드")
            
        finally:
            db.close()
        
        # 3. API 엔드포인트 테스트 준비
        print("\n🚀 FastAPI 서버 테스트 준비 완료!")
        print("   - uvicorn app.main:app --host 0.0.0.0 --port 8000")
        
        return True
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()
