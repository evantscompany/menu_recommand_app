"""
메뉴 관련 500 오류 디버깅 스크립트
"""
import requests
import json

RENDER_URL = "https://menu-recommand-app.onrender.com"

def debug_menu_error():
    """메뉴 500 오류 상세 디버깅"""
    
    print("🔍 메뉴 500 오류 디버깅")
    print("=" * 40)
    
    # 1. 로그인하여 토큰 받기
    try:
        login_response = requests.post(
            f"{RENDER_URL}/api/auth/login-json",
            json={"username": "aaa", "password": "password123"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if login_response.status_code == 200:
            token = login_response.json().get("access_token", "")
            print("✅ 로그인 성공")
        else:
            print(f"❌ 로그인 실패: {login_response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ 로그인 실패: {e}")
        return
    
    # 2. 다양한 메뉴 엔드포인트 테스트
    menu_endpoints = [
        ("/api/menus", "기본 메뉴 목록"),
        ("/api/menus?skip=0&limit=5", "파라미터 있는 메뉴 목록"),
        ("/api/menus?skip=0", "skip만 있는 메뉴 목록"),
        ("/api/menus?limit=5", "limit만 있는 메뉴 목록"),
    ]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    for endpoint, description in menu_endpoints:
        try:
            print(f"\n📋 {description} 테스트:")
            print(f"   URL: {endpoint}")
            
            response = requests.get(f"{RENDER_URL}{endpoint}", headers=headers, timeout=10)
            
            print(f"   상태 코드: {response.status_code}")
            
            if response.status_code == 500:
                print("   ❌ 500 Internal Server Error")
                print(f"   응답: {response.text}")
            elif response.status_code == 200:
                data = response.json()
                print(f"   ✅ 성공: {len(data)}개 메뉴")
            else:
                print(f"   ⚠️ 다른 오류: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 요청 실패: {e}")
    
    # 3. POST 요청 테스트 (메뉴 생성)
    try:
        print(f"\n📝 메뉴 생성 테스트:")
        new_menu = {
            "menu_name": "테스트 메뉴",
            "category": "테스트",
            "image_url": "test.jpg",
            "price": 10000,
            "is_lunch_available": True,
            "matching_weather": "맑음",
            "matching_mood": "기분 좋음",
            "suitable_ground_size": "소규모",
            "is_quick_meal": True
        }
        
        response = requests.post(
            f"{RENDER_URL}/api/menus",
            json=new_menu,
            headers=headers,
            timeout=10
        )
        
        print(f"   상태 코드: {response.status_code}")
        print(f"   응답: {response.text}")
        
    except Exception as e:
        print(f"   ❌ 메뉴 생성 실패: {e}")
    
    # 4. 추천 시스템 테스트
    try:
        print(f"\n🎯 추천 시스템 테스트:")
        recommendation_data = {
            "user_profile": {
                "spicy_threshold": 3,
                "saltiness_preference": 3,
                "lunch_budget_max": 12000,
                "is_adventurous": True
            }
        }
        
        response = requests.post(
            f"{RENDER_URL}/api/recommend/",
            json=recommendation_data,
            headers=headers,
            timeout=10
        )
        
        print(f"   상태 코드: {response.status_code}")
        print(f"   응답: {response.text}")
        
    except Exception as e:
        print(f"   ❌ 추천 시스템 실패: {e}")
    
    # 5. 날씨 엔드포인트 테스트
    try:
        print(f"\n🌤️ 날씨 엔드포인트 테스트:")
        weather_endpoints = [
            "/api/weather/seoul",
            "/api/weather",
            "/api/weather/서울"
        ]
        
        for endpoint in weather_endpoints:
            response = requests.get(f"{RENDER_URL}{endpoint}", timeout=10)
            print(f"   {endpoint}: {response.status_code}")
            if response.status_code != 404:
                print(f"      응답: {response.text[:100]}...")
                
    except Exception as e:
        print(f"   ❌ 날씨 테스트 실패: {e}")

if __name__ == "__main__":
    debug_menu_error()
