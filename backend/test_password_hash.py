import os
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from app.models import UserAccount

# TiDB Cloud 연결 정보
TIDB_HOST = "gateway01.ap-northeast-1.prod.aws.tidbcloud.com"
TIDB_PORT = 4000
TIDB_USER = "3bJdto8FKWk47Fu.root"
TIDB_PASSWORD = "NWOZOcYDO8W5nMk2"
TIDB_DATABASE = "test"

def test_password_verification():
    """비밀번호 해시 검증 테스트"""
    print("🔍 비밀번호 해시 검증 테스트")
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
        
        # 테스트 유저 "aaa" 정보 조회
        result = session.execute(text("SELECT user_id, username, hashed_password FROM user_accounts WHERE username = 'aaa'"))
        user_data = result.fetchone()
        
        if user_data:
            user_id, username, hashed_password = user_data
            print(f"✅ 사용자 찾음: {username}")
            print(f"🔐 해시된 비밀번호: {hashed_password}")
            
            # 비밀번호 검증 테스트
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            test_passwords = ["password123", "password", "123456", "admin"]
            
            for test_pwd in test_passwords:
                try:
                    is_valid = pwd_context.verify(test_pwd, hashed_password)
                    print(f"🔑 '{test_pwd}' 검증: {'✅ 성공' if is_valid else '❌ 실패'}")
                    
                    if is_valid:
                        print(f"🎉 비밀번호 '{test_pwd}'가 일치합니다!")
                        break
                        
                except Exception as e:
                    print(f"❌ '{test_pwd}' 검증 오류: {e}")
            
            # 새로운 해시 생성 테스트
            print("\n🔄 새로운 해시 생성 테스트:")
            new_hash = pwd_context.hash("password123")
            print(f"새로운 해시: {new_hash}")
            
            # 새로운 해시 검증
            is_new_valid = pwd_context.verify("password123", new_hash)
            print(f"새로운 해시 검증: {'✅ 성공' if is_new_valid else '❌ 실패'}")
            
        else:
            print("❌ 사용자 'aaa'를 찾을 수 없음")
        
        session.close()
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")

if __name__ == "__main__":
    test_password_verification()
