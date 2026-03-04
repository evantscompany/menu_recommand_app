"""
메뉴 추천 시스템 디버깅
"""
import requests

RENDER_URL = "https://menu-recommand-app.onrender.com"

def debug_recommendation():
    """메뉴 추천 시스템 디버깅"""
    
    print("🎯 메뉴 추천 시스템 디버깅")
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
    
    # 다양한 추천 데이터 테스트
    test_cases = [
        {
            "name": "최소 데이터",
            "data": {"user_profile": {"spicy_threshold": 3}}
        },
        {
            "name": "기본 데이터",
            "data": {
                "user_profile": {
                    "spicy_threshold": 3,
                    "saltiness_preference": 3,
                    "lunch_budget_max": 12000,
                    "is_adventurous": True
                }
            }
        },
        {
            "name": "전체 데이터",
            "data": {
                "user_profile": {
                    "spicy_threshold": 3,
                    "saltiness_preference": 3,
                    "lunch_budget_max": 12000,
                    "is_adventurous": True,
                    "dietary_label": "일반",
                    "allergies": "없음"
                }
            }
        }
    ]
    
    for test_case in test_cases:
        try:
            print(f"\n📋 {test_case['name']} 테스트:")
            
            response = requests.post(
                f"{RENDER_URL}/api/recommend/",
                json=test_case['data'],
                headers=headers,
                timeout=10
            )
            
            print(f"   상태 코드: {response.status_code}")
            
            if response.status_code == 200:
                recommendations = response.json()
                print(f"   ✅ 성공: {len(recommendations)}개 추천")
                if len(recommendations) > 0:
                    print(f"   📝 첫 추천: {recommendations[0].get('menu_name', 'N/A')}")
            elif response.status_code == 500:
                print(f"   ❌ 500 오류: {response.text}")
            else:
                print(f"   ⚠️ 다른 오류: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 요청 실패: {e}")
    
    # 추천 엔드포인트 확인
    print(f"\n🔍 추천 엔드포인트 확인:")
    try:
        # GET 요청 시도
        response = requests.get(f"{RENDER_URL}/api/recommend/", headers=headers, timeout=10)
        print(f"   GET /api/recommend/: {response.status_code}")
        
        if response.status_code != 405:  # Method Not Allowed가 아니면
            print(f"      응답: {response.text[:100]}...")
            
    except Exception as e:
        print(f"   GET 요청 실패: {e}")
    
    # 다른 추천 관련 엔드포인트 확인
    other_endpoints = [
        "/api/recommend",
        "/api/recommendation",
        "/api/recommendations"
    ]
    
    for endpoint in other_endpoints:
        try:
            response = requests.post(
                f"{RENDER_URL}{endpoint}",
                json={"user_profile": {"spicy_threshold": 3}},
                headers=headers,
                timeout=10
            )
            print(f"   POST {endpoint}: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"      ✅ 성공: {len(data)}개")
            elif response.status_code != 404:
                print(f"      응답: {response.text[:50]}...")
                
        except Exception as e:
            print(f"   {endpoint}: 실패 - {e}")

if __name__ == "__main__":
    debug_recommendation()
