"""
메뉴 API 디버깅 테스트
"""
import requests

RENDER_URL = "https://menu-recommand-app.onrender.com"

def test_menu_api():
    """메뉴 API 상세 테스트"""
    
    print("🔍 메뉴 API 디버깅 테스트")
    print("=" * 40)
    
    # 1. 기본 메뉴 목록
    try:
        response = requests.get(f"{RENDER_URL}/api/menus", timeout=10)
        print(f"📋 메뉴 목록: {response.status_code}")
        if response.status_code != 200:
            print(f"   응답: {response.text}")
    except Exception as e:
        print(f"❌ 메뉴 목록 실패: {e}")
    
    # 2. 파라미터 있는 메뉴 목록
    try:
        response = requests.get(f"{RENDER_URL}/api/menus?skip=0&limit=10", timeout=10)
        print(f"📋 메뉴 목록 (파라미터): {response.status_code}")
        if response.status_code != 200:
            print(f"   응답: {response.text}")
    except Exception as e:
        print(f"❌ 메뉴 목록 (파라미터) 실패: {e}")
    
    # 3. 단일 메뉴 조회 시도
    try:
        response = requests.get(f"{RENDER_URL}/api/menus/1", timeout=10)
        print(f"📋 단일 메뉴: {response.status_code}")
        if response.status_code != 200:
            print(f"   응답: {response.text}")
    except Exception as e:
        print(f"❌ 단일 메뉴 실패: {e}")
    
    # 4. 로그인 후 메뉴 조회
    try:
        login_response = requests.post(
            f"{RENDER_URL}/api/auth/login-json",
            json={"username": "aaa", "password": "password123"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if login_response.status_code == 200:
            token = login_response.json().get("access_token", "")
            headers = {"Authorization": f"Bearer {token}"}
            
            menu_response = requests.get(f"{RENDER_URL}/api/menus", headers=headers, timeout=10)
            print(f"📋 로그인 후 메뉴: {menu_response.status_code}")
            if menu_response.status_code == 200:
                menus = menu_response.json()
                print(f"   메뉴 수: {len(menus)}개")
                if len(menus) > 0:
                    print(f"   첫 메뉴: {menus[0].get('menu_name', 'N/A')}")
            else:
                print(f"   응답: {menu_response.text}")
        else:
            print(f"❌ 로그인 실패: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ 로그인 후 메뉴 실패: {e}")

if __name__ == "__main__":
    test_menu_api()
