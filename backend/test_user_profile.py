"""
UserProfile 관계 테스트
"""
import requests

RENDER_URL = "https://menu-recommand-app.onrender.com"

def test_user_profile():
    """UserProfile 관계 테스트"""
    
    print("🔍 UserProfile 관계 테스트")
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
    
    # 사용자 정보 확인
    try:
        response = requests.get(f"{RENDER_URL}/api/users/me", headers=headers, timeout=10)
        
        print(f"\n👤 사용자 정보 조회: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"   사용자: {user_data.get('username', 'N/A')}")
            print(f"   이메일: {user_data.get('email', 'N/A')}")
            
            # profile 정보 확인
            if 'profile' in user_data:
                profile = user_data['profile']
                print(f"   프로필 존재: {profile}")
                
                if profile:
                    print(f"   예산: {profile.get('lunch_budget_max', 'N/A')}")
                    print(f"   맵기: {profile.get('spicy_threshold', 'N/A')}")
                else:
                    print("   ⚠️ 프로필이 None입니다")
            else:
                print("   ❌ 프로필 키가 없습니다")
                
        else:
            print(f"   응답: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ 사용자 정보 조회 실패: {e}")
    
    # 메뉴 추천 시도
    try:
        response = requests.get(f"{RENDER_URL}/api/recommend/recommendations", headers=headers, timeout=10)
        
        print(f"\n🎯 메뉴 추천 시도: {response.status_code}")
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"   추천 성공: {len(recommendations)}개")
        else:
            print(f"   응답: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ 메뉴 추천 실패: {e}")

if __name__ == "__main__":
    test_user_profile()
