"""
Render 배포된 서버의 데이터베이스 연결 상태 확인
"""
import requests
import json

RENDER_URL = "https://menu-recommand-app.onrender.com"

def test_db_connection():
    """데이터베이스 연결 테스트"""
    
    print("🔍 Render 서버 데이터베이스 연결 테스트")
    print("=" * 50)
    
    # 1. 기본 상태 확인
    try:
        response = requests.get(f"{RENDER_URL}/", timeout=10)
        print(f"✅ 서버 상태: {response.status_code}")
        print(f"   응답: {response.json()}")
    except Exception as e:
        print(f"❌ 서버 연결 실패: {e}")
        return
    
    # 2. 메뉴 목록 확인 (DB 연결 필요)
    try:
        response = requests.get(f"{RENDER_URL}/api/menus", timeout=10)
        print(f"\n📋 메뉴 목록 조회: {response.status_code}")
        
        if response.status_code == 200:
            menus = response.json()
            print(f"   메뉴 수: {len(menus)}개")
            
            if len(menus) > 0:
                print("   📝 샘플 메뉴:")
                for i, menu in enumerate(menus[:3]):
                    print(f"     {i+1}. {menu.get('menu_name', 'N/A')} ({menu.get('category', 'N/A')}) - {menu.get('price', 'N/A')}원")
            else:
                print("   ⚠️ 메뉴 데이터가 없습니다!")
                print("   🔍 데이터베이스 연결 또는 데이터 마이그레이션 문제 가능성")
        else:
            print(f"   ❌ 오류: {response.text}")
            
    except Exception as e:
        print(f"❌ 메뉴 조회 실패: {e}")
    
    # 3. 사용자 목록 확인
    try:
        response = requests.get(f"{RENDER_URL}/api/users", timeout=10)
        print(f"\n👥 사용자 목록 조회: {response.status_code}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"   사용자 수: {len(users)}개")
            
            if len(users) > 0:
                print("   📝 샘플 사용자:")
                for i, user in enumerate(users[:3]):
                    print(f"     {i+1}. {user.get('username', 'N/A')} ({user.get('email', 'N/A')})")
            else:
                print("   ⚠️ 사용자 데이터가 없습니다!")
        else:
            print(f"   ❌ 오류: {response.text}")
            
    except Exception as e:
        print(f"❌ 사용자 조회 실패: {e}")
    
    # 4. 로그인 시도 (DB 연결 필요)
    try:
        login_data = {
            "username": "aaa",
            "password": "password123"
        }
        
        response = requests.post(
            f"{RENDER_URL}/api/auth/login-json",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\n🔐 로그인 시도: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ 로그인 성공!")
            print(f"   토큰: {result.get('access_token', '')[:20]}...")
        else:
            print(f"   ❌ 로그인 실패: {response.json()}")
            print("   🔍 사용자 데이터가 없거나 비밀번호 불일치 가능성")
            
    except Exception as e:
        print(f"❌ 로그인 테스트 실패: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 진단 결과:")
    print("   - 서버는 정상적으로 실행 중")
    print("   - 메뉴 데이터가 0개이면 DB 연결 문제")
    print("   - 로그인 실패는 사용자 데이터 문제")
    print("   - 환경변수 설정 확인 필요")

if __name__ == "__main__":
    test_db_connection()
