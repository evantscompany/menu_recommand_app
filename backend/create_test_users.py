#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트용 사용자 데이터 생성 스크립트 (V4 - Path Fixed)
구조: menu_recommand_app (Root - DB 위치) / backend (모듈 위치)
"""

import sys
import os
from datetime import datetime

# 1. 경로 설정
# 현재 스크립트가 있는 루트 폴더 (menu_recommand_app)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, 'backend')

# 모듈 참조를 위해 backend 경로를 sys.path에 추가
sys.path.append(BACKEND_DIR)

try:
    # backend 폴더가 sys.path에 있으므로 app.database로 호출 가능
    from app.database import engine, SessionLocal, Base
    from app.models import UserAccount, UserProfile
except ImportError as e:
    print(f"Error: backend 모듈을 찾을 수 없습니다. (현재 설정 경로: {BACKEND_DIR})")
    print(f"상세 오류: {e}")
    sys.exit(1)

# 작업 디렉토리를 Root로 변경 (상위에 있는 DB를 바로 인식하게 함)
os.chdir(ROOT_DIR)

def hash_password(password: str) -> str:
    """비밀번호 해시화 (bcrypt 사용)"""
    from app.core.security import get_password_hash
    return get_password_hash(password)

def create_test_users():
    """테스트용 사용자 3명 생성"""
    
    print(f"📌 현재 위치: {os.getcwd()}")
    print(f"📌 DB 연결 대상: {engine.url}")

    # 데이터베이스 테이블 생성 (없을 경우에만)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # 사용자 데이터 정의
        users_data = [
            {
                "username": "aaa",
                "email": "aaa@test.com",
                "nickname": "매운맛 애호가",
                "password": "aaa",
                "profile": {
                    "dietary_label": "none",
                    "allergies": None,
                    "spicy_threshold": 5,
                    "saltiness_preference": 4,
                    "lunch_budget_max": 15000,
                    "is_adventurous": True
                }
            },
            {
                "username": "bbb", 
                "email": "bbb@test.com",
                "nickname": "건강식 애호가",
                "password": "bbb",
                "profile": {
                    "dietary_label": "healthy",
                    "allergies": "견과류",
                    "spicy_threshold": 2,
                    "saltiness_preference": 2,
                    "lunch_budget_max": 10000,
                    "is_adventurous": False
                }
            },
            {
                "username": "ccc",
                "email": "ccc@test.com", 
                "nickname": "중용파",
                "password": "ccc",
                "profile": {
                    "dietary_label": "none",
                    "allergies": None,
                    "spicy_threshold": 3,
                    "saltiness_preference": 3,
                    "lunch_budget_max": 12000,
                    "is_adventurous": True
                }
            }
        ]
        
        created_count = 0
        
        for user_data in users_data:
            # 기존 사용자 확인
            existing_user = db.query(UserAccount).filter(UserAccount.username == user_data["username"]).first()
            
            if existing_user:
                print(f"'{user_data['username']}' 사용자는 이미 존재합니다. 건너뜁니다.")
                continue
            
            # 사용자 계정 생성
            new_user = UserAccount(
                username=user_data["username"],
                email=user_data["email"],
                nickname=user_data["nickname"],
                hashed_password=hash_password(user_data["password"]),
                created_at=datetime.now()
            )
            
            db.add(new_user)
            db.flush() # user_id를 얻기 위해 flush
            
            # 사용자 프로필 생성
            new_profile = UserProfile(
                user_id=new_user.user_id,
                dietary_label=user_data["profile"]["dietary_label"],
                allergies=user_data["profile"]["allergies"],
                spicy_threshold=user_data["profile"]["spicy_threshold"],
                saltiness_preference=user_data["profile"]["saltiness_preference"],
                lunch_budget_max=user_data["profile"]["lunch_budget_max"],
                is_adventurous=user_data["profile"]["is_adventurous"]
            )
            
            db.add(new_profile)
            created_count += 1
            print(f"✅ 생성됨: {user_data['username']} ({user_data['nickname']})")
        
        # 모든 작업 완료 후 커밋
        db.commit()
        print(f"\n=== 생성 완료 ===")
        print(f"새로 생성된 사용자: {created_count}명")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        # 오류 상세 내용을 파악하기 위해 raise는 유지하거나 로그를 남깁니다.
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=== 테스트 사용자 생성 스크립트 ===")
    create_test_users()