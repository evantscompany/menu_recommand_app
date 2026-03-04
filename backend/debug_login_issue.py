import requests
import json

BASE_URL = "https://menu-recommand-app.onrender.com"

def test_login_detailed():
    """로그인 문제 상세 분석"""
    print("🔍 로그인 문제 상세 분석")
    print("=" * 50)
    
    # 1. 기존 테스트 유저로 로그인 시도
    print("\n1. 기존 테스트 유저 로그인 시도")
    login_data = {
        "username": "aaa",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login-json", json=login_data)
        print(f"상태 코드: {response.status_code}")
        print(f"응답: {response.text}")
        
        if response.status_code == 200:
            print("✅ 로그인 성공!")
            return response.json()
        else:
            print("❌ 로그인 실패")
            
    except Exception as e:
        print(f"❌ 요청 실패: {e}")
    
    # 2. 회원가입 시도 (새 유저 생성)
    print("\n2. 새 유저 회원가입 시도")
    signup_data = {
        "username": "testuser_new",
        "email": "testuser_new@example.com",
        "nickname": "testuser_new",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
        print(f"상태 코드: {response.status_code}")
        print(f"응답: {response.text}")
        
        if response.status_code == 201:
            print("✅ 회원가입 성공!")
            
            # 새 유저로 로그인 시도
            print("\n3. 새 유저 로그인 시도")
            new_login_data = {
                "username": "testuser_new",
                "password": "password123"
            }
            
            response = requests.post(f"{BASE_URL}/api/auth/login-json", json=new_login_data)
            print(f"상태 코드: {response.status_code}")
            print(f"응답: {response.text}")
            
            if response.status_code == 200:
                print("✅ 새 유저 로그인 성공!")
                return response.json()
            else:
                print("❌ 새 유저 로그인 실패")
        else:
            print("❌ 회원가입 실패")
            
    except Exception as e:
        print(f"❌ 요청 실패: {e}")
    
    return None

def test_server_health():
    """서버 상태 확인"""
    print("\n🏥 서버 상태 확인")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"서버 상태: {response.status_code}")
        print(f"응답: {response.text}")
        
        response = requests.get(f"{BASE_URL}/docs")
        print(f"API 문서: {response.status_code}")
        
        response = requests.get(f"{BASE_URL}/api/menus")
        print(f"메뉴 API: {response.status_code}")
        
    except Exception as e:
        print(f"❌ 서버 상태 확인 실패: {e}")

if __name__ == "__main__":
    test_server_health()
    test_login_detailed()
