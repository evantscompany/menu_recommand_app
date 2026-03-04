"""
UserProfile.profile 속성 오류 디버깅
"""
import os
import sys
sys.path.append('.')

from app.database_mysql import SessionLocal
from app import models, crud

def debug_profile_error():
    """UserProfile.profile 속성 오류 디버깅"""
    
    print("🔍 UserProfile.profile 속성 오류 디버깅")
    print("=" * 50)
    
    # DB 연결
    db = SessionLocal()
    
    try:
        # 1. 사용자 확인
        user = crud.get_user_by_username(db, username="aaa")
        if not user:
            print("❌ 사용자 없음")
            return
        
        print(f"✅ 사용자: {user.username}")
        print(f"   사용자 타입: {type(user)}")
        print(f"   사용자 속성: {[attr for attr in dir(user) if not attr.startswith('_')]}")
        
        # 2. profile 속성 확인
        if hasattr(user, 'profile'):
            profile = user.profile
            print(f"   profile 속성 존재: {profile}")
            print(f"   profile 타입: {type(profile)}")
            
            if profile:
                print(f"   profile 속성: {[attr for attr in dir(profile) if not attr.startswith('_')]}")
                print(f"   예산: {getattr(profile, 'lunch_budget_max', '없음')}")
                print(f"   맵기: {getattr(profile, 'spicy_threshold', '없음')}")
            else:
                print("   ⚠️ profile이 None입니다")
        else:
            print("   ❌ profile 속성이 없습니다")
            
        # 3. 직접 profile 조회 시도
        print(f"\n🔍 직접 profile 조회 시도:")
        try:
            from app.models import UserProfile
            direct_profile = db.query(UserProfile).filter(UserProfile.user_id == user.user_id).first()
            print(f"   직접 조회된 profile: {direct_profile}")
            
            if direct_profile:
                print(f"   직접 조회된 예산: {direct_profile.lunch_budget_max}")
                print(f"   직접 조회된 맵기: {direct_profile.spicy_threshold}")
            else:
                print("   ⚠️ 직접 조회된 profile이 None입니다")
                
        except Exception as e:
            print(f"   ❌ 직접 profile 조회 실패: {e}")
        
        # 4. UserAccount 모델 확인
        print(f"\n🔍 UserAccount 모델 확인:")
        print(f"   UserAccount.__tablename__: {models.UserAccount.__tablename__}")
        print(f"   UserAccount.relationships: {[rel for rel in models.UserAccount.__mapper__.relationships if hasattr(rel, 'key')]}")
        
        # 5. UserProfile 모델 확인
        print(f"\n🔍 UserProfile 모델 확인:")
        if hasattr(models, 'UserProfile'):
            print(f"   UserProfile.__tablename__: {models.UserProfile.__tablename__}")
            print(f"   UserProfile.relationships: {[rel for rel in models.UserProfile.__mapper__.relationships if hasattr(rel, 'key')]}")
        else:
            print("   ❌ UserProfile 모델이 없습니다")
        
        print("\n✅ 디버깅 완료")
        
    except Exception as e:
        print(f"❌ 디버깅 실패: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == "__main__":
    debug_profile_error()
