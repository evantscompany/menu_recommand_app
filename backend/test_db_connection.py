"""
데이터베이스 연결 및 모델 테스트
"""
import os
import sys
sys.path.append('.')

from app.database_mysql import engine, SessionLocal
from app import models
from sqlalchemy import text

def test_database_and_models():
    """데이터베이스 연결 및 모델 테스트"""
    
    print("🔍 데이터베이스 연결 및 모델 테스트")
    print("=" * 50)
    
    try:
        # 1. 데이터베이스 연결 테스트
        print("1. 데이터베이스 연결 테스트...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            print(f"   ✅ 연결 성공: {version}")
        
        # 2. 세션 생성
        print("\n2. 세션 생성 테스트...")
        db = SessionLocal()
        print("   ✅ 세션 생성 성공")
        
        # 3. 모델 테이블 생성 테스트
        print("\n3. 테이블 생성 테스트...")
        try:
            models.Base.metadata.create_all(bind=engine)
            print("   ✅ 테이블 생성 성공")
        except Exception as e:
            print(f"   ❌ 테이블 생성 실패: {e}")
            return False
        
        # 4. Menu 모델 테스트
        print("\n4. Menu 모델 테스트...")
        try:
            menu_count = db.query(models.Menu).count()
            print(f"   ✅ Menu 모델 정상: {menu_count}개 레코드")
            
            # 첫 번째 메뉴 조회
            if menu_count > 0:
                first_menu = db.query(models.Menu).first()
                print(f"   📝 첫 메뉴: {first_menu.menu_name} ({first_menu.category})")
                
                # 관계 테스트
                if hasattr(first_menu, 'details') and first_menu.details:
                    print(f"   🔗 상세 정보 연결됨: {first_menu.details.detail_id}")
                else:
                    print("   ⚠️ 상세 정보 연결 안됨")
            
        except Exception as e:
            print(f"   ❌ Menu 모델 실패: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # 5. UserAccount 모델 테스트
        print("\n5. UserAccount 모델 테스트...")
        try:
            user_count = db.query(models.UserAccount).count()
            print(f"   ✅ UserAccount 모델 정상: {user_count}개 레코드")
            
            if user_count > 0:
                first_user = db.query(models.UserAccount).first()
                print(f"   📝 첫 사용자: {first_user.username} ({first_user.email})")
            
        except Exception as e:
            print(f"   ❌ UserAccount 모델 실패: {e}")
            return False
        
        # 6. CRUD 함수 테스트
        print("\n6. CRUD 함수 테스트...")
        try:
            from app import crud
            
            # get_menus 함수 테스트
            menus = crud.get_menus(db, skip=0, limit=5)
            print(f"   ✅ get_menus 함수 정상: {len(menus)}개 메뉴")
            
            # get_user_by_username 함수 테스트
            user = crud.get_user_by_username(db, username="aaa")
            if user:
                print(f"   ✅ get_user_by_username 함수 정상: {user.username}")
            else:
                print("   ⚠️ get_user_by_username: 사용자 없음")
                
        except Exception as e:
            print(f"   ❌ CRUD 함수 실패: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # 7. 테이블 구조 확인
        print("\n7. 테이블 구조 확인...")
        try:
            with engine.connect() as conn:
                result = conn.execute(text("DESCRIBE menus"))
                columns = result.fetchall()
                print(f"   📋 menus 테이블 컬럼 수: {len(columns)}")
                for col in columns[:5]:  # 처음 5개만
                    print(f"      - {col[0]}: {col[1]}")
                
        except Exception as e:
            print(f"   ❌ 테이블 구조 확인 실패: {e}")
        
        db.close()
        print("\n✅ 모든 테스트 통과!")
        return True
        
    except Exception as e:
        print(f"❌ 데이터베이스 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_database_and_models()
