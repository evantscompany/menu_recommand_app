"""
Render 환경에서 날씨 서비스 테스트
"""
import requests
import json

RENDER_URL = "https://menu-recommand-app.onrender.com"

def test_weather_render():
    """Render 환경에서 날씨 서비스 테스트"""
    
    print("🌤️ Render 환경 날씨 서비스 테스트")
    print("=" * 50)
    
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
    
    # 날씨 관련 엔드포인트 테스트
    print("\n🌤️ 날씨 관련 엔드포인트 테스트:")
    
    # 1. 날씨 엔드포인트 확인
    weather_endpoints = [
        "/api/weather/seoul",
        "/api/weather",
        "/api/weather/서울"
    ]
    
    for endpoint in weather_endpoints:
        try:
            response = requests.get(f"{RENDER_URL}{endpoint}", timeout=10)
            print(f"   {endpoint}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"      ✅ 성공: {data}")
            else:
                print(f"      응답: {response.text[:50]}...")
        except Exception as e:
            print(f"   {endpoint}: 실패 - {e}")
    
    # 2. 간단한 추천 시도 (날씨 데이터 사용)
    print("\n🎯 간단한 추천 시도:")
    try:
        response = requests.post(
            f"{RENDER_URL}/api/recommend/recommendations",
            headers=headers,
            timeout=10
        )
        print(f"   추천 시도: {response.status_code}")
        if response.status_code == 500:
            print(f"      500 오류: {response.text}")
        elif response.status_code == 200:
            data = response.json()
            print(f"      ✅ 성공: {len(data)}개 추천")
    except Exception as e:
        print(f"   추천 시도 실패: {e}")
    
    # 3. 사용자 정보 확인 (프로필 포함)
    print("\n👤 사용자 정보 확인:")
    try:
        response = requests.get(f"{RENDER_URL}/api/users/me", headers=headers, timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            print(f"   사용자: {user_data.get('username', 'N/A')}")
            print(f"   이메일: {user_data.get('email', 'N/A')}")
            
            # 프로필 정보 확인
            if 'profile' in user_data:
                profile = user_data['profile']
                print(f"   프로필: 예산 {profile.get('lunch_budget_max', 'N/A')}원")
                print(f"   프로필: 맵기 {profile.get('spicy_threshold', 'N/A')}")
            else:
                print("   ⚠️ 프로필 정보 없음")
        else:
            print(f"   사용자 정보 조회 실패: {response.status_code}")
    except Exception as e:
        print(f"   사용자 정보 조회 실패: {e}")

if __name__ == "__main__":
    test_weather_render()
