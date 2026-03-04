"""
Render 서버 간단 기능 테스트
"""
import requests
import json

RENDER_URL = "https://menu-recommand-app.onrender.com"

def test_simple_functions():
    """간단한 기능 테스트"""
    
    print("🔍 Render 서버 간단 기능 테스트")
    print("=" * 40)
    
    # 1. 서버 상태
    try:
        response = requests.get(RENDER_URL, timeout=10)
        print(f"✅ 서버 상태: {response.status_code}")
        print(f"   응답: {response.json()}")
    except Exception as e:
        print(f"❌ 서버 연결 실패: {e}")
        return
    
    # 2. 메뉴 목록
    try:
        response = requests.get(f"{RENDER_URL}/api/menus", timeout=10)
        print(f"\n📋 메뉴 목록: {response.status_code}")
        if response.status_code == 200:
            menus = response.json()
            print(f"   메뉴 수: {len(menus)}개")
            if len(menus) > 0:
                print(f"   첫 메뉴: {menus[0].get('menu_name', 'N/A')}")
        else:
            print(f"   응답: {response.text}")
    except Exception as e:
        print(f"❌ 메뉴 조회 실패: {e}")
    
    # 3. 회원가입 테스트
    try:
        new_user = {
            "username": "testuser123",
            "email": "test@example.com",
            "nickname": "테스트유저",
            "password": "password123"
        }
        
        response = requests.post(
            f"{RENDER_URL}/api/auth/register",
            json=new_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\n👤 회원가입: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   결과: {result}")
            print(f"   ✅ 회원가입 성공!")
            print(f"   📝 테스트 계정 정보:")
            print(f"      아이디: {new_user['username']}")
            print(f"      비밀번호: {new_user['password']}")
        else:
            print(f"   응답: {response.text}")
            
    except Exception as e:
        print(f"❌ 회원가입 실패: {e}")
    
    # 4. 로그인 테스트 (기존 사용자)
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
        
        print(f"\n🔐 로그인 (aaa): {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token", "")
            print(f"   ✅ 로그인 성공!")
            print(f"   토큰: {token[:20]}...")
            
            # 5. 사용자 정보 조회
            headers = {"Authorization": f"Bearer {token}"}
            user_response = requests.get(f"{RENDER_URL}/api/users/me", headers=headers, timeout=10)
            
            print(f"\n👤 사용자 정보: {user_response.status_code}")
            if user_response.status_code == 200:
                user_info = user_response.json()
                print(f"   사용자: {user_info.get('username', 'N/A')}")
                print(f"   이메일: {user_info.get('email', 'N/A')}")
            else:
                print(f"   응답: {user_response.text}")
                
        else:
            print(f"   응답: {response.text}")
            
    except Exception as e:
        print(f"❌ 로그인 실패: {e}")

if __name__ == "__main__":
    test_simple_functions()
