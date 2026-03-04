import requests
import json

BASE_URL = "https://menu-recommand-app.onrender.com"

def check_database_status():
    """데이터베이스 상태 확인"""
    print("🔍 데이터베이스 상태 확인")
    print("=" * 50)
    
    # 메뉴 데이터 확인 (이건 작동함)
    try:
        response = requests.get(f"{BASE_URL}/api/menus")
        if response.status_code == 200:
            menus = response.json()
            print(f"✅ 메뉴 데이터: {len(menus)}개")
        else:
            print(f"❌ 메뉴 데이터 오류: {response.status_code}")
    except Exception as e:
        print(f"❌ 메뉴 데이터 확인 실패: {e}")
    
    # 사용자 관련 API 테스트
    print("\n👤 사용자 관련 API 테스트")
    
    # 회원가입 시도 (상세 오류 확인)
    signup_data = {
        "username": "debug_user",
        "email": "debug@example.com", 
        "nickname": "debug_user",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
        print(f"회원가입 상태: {response.status_code}")
        print(f"회원가입 응답: {response.text}")
        
        if response.status_code == 500:
            print("🚨 회원가입 500 오류 - 서버 내부 문제!")
            
    except Exception as e:
        print(f"❌ 회원가입 테스트 실패: {e}")
    
    # 로그인 시도 (상세 오류 확인)
    login_data = {
        "username": "aaa",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login-json", json=login_data)
        print(f"로그인 상태: {response.status_code}")
        print(f"로그인 응답: {response.text}")
        
        if response.status_code == 401:
            print("🚨 로그인 401 오류 - 사용자 없음 또는 비밀번호 틀림!")
            
    except Exception as e:
        print(f"❌ 로그인 테스트 실패: {e}")

def check_api_endpoints():
    """API 엔드포인트 상태 확인"""
    print("\n🔗 API 엔드포인트 상태 확인")
    print("=" * 50)
    
    endpoints = [
        ("/", "홈"),
        ("/docs", "API 문서"),
        ("/api/menus", "메뉴 목록"),
        ("/api/weather/seoul", "날씨 정보"),
        ("/api/auth/signup", "회원가입"),
        ("/api/auth/login-json", "로그인")
    ]
    
    for endpoint, name in endpoints:
        try:
            if endpoint in ["/api/auth/signup", "/api/auth/login-json"]:
                # POST 요청은 GET으로 테스트
                response = requests.get(f"{BASE_URL}{endpoint}")
            else:
                response = requests.get(f"{BASE_URL}{endpoint}")
            
            status = "✅" if response.status_code in [200, 405] else "❌"
            print(f"{status} {name}: {response.status_code}")
            
        except Exception as e:
            print(f"❌ {name}: 연결 실패 - {e}")

if __name__ == "__main__":
    check_api_endpoints()
    check_database_status()
