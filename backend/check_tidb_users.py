import os
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# TiDB Cloud 연결 정보
TIDB_HOST = "gateway01.ap-northeast-1.prod.aws.tidbcloud.com"
TIDB_PORT = 4000
TIDB_USER = "3bJdto8FKWk47Fu.root"
TIDB_PASSWORD = "NWOZOcYDO8W5nMk2"
TIDB_DATABASE = "test"

def check_tidb_connection():
    """TiDB Cloud 연결 및 사용자 테이블 확인"""
    print("🔍 TiDB Cloud 사용자 테이블 확인")
    print("=" * 50)
    
    try:
        # 데이터베이스 연결
        engine = create_engine(
            f"mysql+pymysql://{TIDB_USER}:{TIDB_PASSWORD}@{TIDB_HOST}:{TIDB_PORT}/{TIDB_DATABASE}",
            connect_args={
                "ssl": {
                    "ssl_ca": "/etc/ssl/cert.pem",
                    "ssl_verify_cert": False
                }
            }
        )
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print("✅ TiDB Cloud 연결 성공!")
        
        # 테이블 목록 확인
        print("\n📋 테이블 목록 확인:")
        result = session.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result.fetchall()]
        print(f"테이블: {tables}")
        
        # user_accounts 테이블 확인
        if "user_accounts" in tables:
            print("\n👤 user_accounts 테이블 확인:")
            result = session.execute(text("SELECT COUNT(*) FROM user_accounts"))
            count = result.fetchone()[0]
            print(f"사용자 수: {count}")
            
            if count > 0:
                result = session.execute(text("SELECT user_id, username, email, nickname FROM user_accounts LIMIT 5"))
                users = result.fetchall()
                print("사용자 목록:")
                for user in users:
                    print(f"  ID: {user[0]}, 사용자: {user[1]}, 이메일: {user[2]}, 닉네임: {user[3]}")
            else:
                print("❌ 사용자 데이터 없음!")
        else:
            print("❌ user_accounts 테이블 없음!")
        
        # user_profiles 테이블 확인
        if "user_profiles" in tables:
            print("\n🎯 user_profiles 테이블 확인:")
            result = session.execute(text("SELECT COUNT(*) FROM user_profiles"))
            count = result.fetchone()[0]
            print(f"프로필 수: {count}")
        else:
            print("❌ user_profiles 테이블 없음!")
        
        # 메뉴 테이블 확인 (비교용)
        if "menus" in tables:
            print("\n🍽️ menus 테이블 확인:")
            result = session.execute(text("SELECT COUNT(*) FROM menus"))
            count = result.fetchone()[0]
            print(f"메뉴 수: {count}")
        else:
            print("❌ menus 테이블 없음!")
        
        session.close()
        
    except Exception as e:
        print(f"❌ TiDB Cloud 연결 실패: {e}")
        print("🔧 환경 변수 확인 필요:")
        print(f"   TIDB_HOST: {TIDB_HOST}")
        print(f"   TIDB_PORT: {TIDB_PORT}")
        print(f"   TIDB_USER: {TIDB_USER}")
        print(f"   TIDB_DATABASE: {TIDB_DATABASE}")

if __name__ == "__main__":
    check_tidb_connection()
