"""
추천 엔드포인트 직접 테스트
"""
import requests
import json

RENDER_URL = "https://menu-recommand-app.onrender.com"

def test_recommendation_endpoint():
    """추천 엔드포인트 직접 테스트"""
    
    print("🎯 추천 엔드포인트 직접 테스트")
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
    
    # 라우터 확인
    print("\n🔍 라우터 확인:")
    
    # 1. 기본 라우터 정보
    try:
        response = requests.get(f"{RENDER_URL}/docs", timeout=10)
        print(f"   API 문서: {response.status_code}")
    except Exception as e:
        print(f"   API 문서 접근 실패: {e}")
    
    # 2. 추천 라우터 테스트
    print("\n📋 추천 라우터 테스트:")
    
    # GET /api/recommend/
    try:
        response = requests.get(
            f"{RENDER_URL}/api/recommend/",
            headers=headers,
            timeout=10
        )
        print(f"   GET /api/recommend/: {response.status_code}")
        if response.status_code != 405:
            print(f"      응답: {response.text[:100]}...")
    except Exception as e:
        print(f"   GET /api/recommend/: 실패 - {e}")
    
    # GET /api/recommend/recommendations
    try:
        response = requests.get(
            f"{RENDER_URL}/api/recommend/recommendations",
            headers=headers,
            timeout=10
        )
        print(f"   GET /api/recommend/recommendations: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"      ✅ 성공: {len(data)}개 추천")
        else:
            print(f"      응답: {response.text[:100]}...")
    except Exception as e:
        print(f"   GET /api/recommend/recommendations: 실패 - {e}")
    
    # POST /api/recommend/
    try:
        response = requests.post(
            f"{RENDER_URL}/api/recommend/",
            headers=headers,
            timeout=10
        )
        print(f"   POST /api/recommend/: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"      ✅ 성공: {len(data)}개 추천")
        else:
            print(f"      응답: {response.text[:100]}...")
    except Exception as e:
        print(f"   POST /api/recommend/: 실패 - {e}")
    
    # POST /api/recommend/ (빈 바디)
    try:
        response = requests.post(
            f"{RENDER_URL}/api/recommend/",
            json={},
            headers=headers,
            timeout=10
        )
        print(f"   POST /api/recommend/ (빈 바디): {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"      ✅ 성공: {len(data)}개 추천")
        else:
            print(f"      응답: {response.text[:100]}...")
    except Exception as e:
        print(f"   POST /api/recommend/ (빈 바디): 실패 - {e}")
    
    # POST /api/recommend/ (user_profile만)
    try:
        response = requests.post(
            f"{RENDER_URL}/api/recommend/",
            json={"user_profile": {"spicy_threshold": 3}},
            headers=headers,
            timeout=10
        )
        print(f"   POST /api/recommend/ (user_profile): {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"      ✅ 성공: {len(data)}개 추천")
        else:
            print(f"      응답: {response.text[:100]}...")
    except Exception as e:
        print(f"   POST /api/recommend/ (user_profile): 실패 - {e}")

if __name__ == "__main__":
    test_recommendation_endpoint()
