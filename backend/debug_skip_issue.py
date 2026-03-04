"""
skip=0 문제 상세 디버깅
"""
import requests

RENDER_URL = "https://menu-recommand-app.onrender.com"

def debug_skip_issue():
    """skip=0 문제 상세 디버깅"""
    
    print("🔍 skip=0 문제 상세 디버깅")
    print("=" * 40)
    
    # 로그인
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
            print("✅ 로그인 성공")
        else:
            print(f"❌ 로그인 실패: {login_response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ 로그인 실패: {e}")
        return
    
    # 다양한 skip 값 테스트
    test_cases = [
        {"skip": 0, "limit": 5},
        {"skip": 1, "limit": 5},
        {"skip": 2, "limit": 5},
        {"skip": 0, "limit": 10},
        {"skip": 1, "limit": 10},
        {"skip": 0},
        {"skip": 1},
        {"limit": 5},
        {}
    ]
    
    print("\n📋 다양한 파라미터 테스트:")
    
    for params in test_cases:
        try:
            response = requests.get(
                f"{RENDER_URL}/api/menus",
                params=params,
                headers=headers,
                timeout=10
            )
            
            print(f"   파라미터 {params}: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"      ✅ 성공: {len(data)}개 메뉴")
            elif response.status_code == 500:
                print(f"      ❌ 500 오류")
            else:
                print(f"      ⚠️ 다른 오류: {response.status_code}")
                
        except Exception as e:
            print(f"   파라미터 {params}: 실패 - {e}")
    
    # 직접 URL 테스트
    print("\n🔗 직접 URL 테스트:")
    direct_urls = [
        "/api/menus",
        "/api/menus?skip=0",
        "/api/menus?skip=1", 
        "/api/menus?limit=5",
        "/api/menus?skip=0&limit=5",
        "/api/menus?skip=1&limit=5"
    ]
    
    for url_suffix in direct_urls:
        try:
            response = requests.get(f"{RENDER_URL}{url_suffix}", headers=headers, timeout=10)
            print(f"   {url_suffix}: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"      ✅ 성공: {len(data)}개 메뉴")
            elif response.status_code == 500:
                print(f"      ❌ 500 오류")
                
        except Exception as e:
            print(f"   {url_suffix}: 실패 - {e}")

if __name__ == "__main__":
    debug_skip_issue()
