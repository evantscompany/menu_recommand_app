"""
Render에서 직접 profile 관계 테스트
"""
import requests

RENDER_URL = "https://menu-recommand-app.onrender.com"

def test_render_profile_direct():
    """Render에서 직접 profile 관계 테스트"""
    
    print("🔍 Render에서 직접 profile 관계 테스트")
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
                print(f"   profile 타입: {type(profile)}")
                print(f"   profile 내용: {profile}")
                
                if profile:
                    print(f"   spicy_threshold: {profile.get('spicy_threshold', 'N/A')}")
                    print(f"   lunch_budget_max: {profile.get('lunch_budget_max', 'N/A')}")
                else:
                    print("   ⚠️ profile이 None 또는 빈 딕셔너리")
            else:
                print("   ❌ profile 키가 없습니다")
                
        else:
            print(f"   응답 내용: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ 사용자 정보 조회 실패: {e}")
    
    # 메뉴 추천 시도
    try:
        response = requests.get(f"{RENDER_URL}/api/recommend/recommendations", headers=headers, timeout=10)
        
        print(f"\n🎯 메뉴 추천 시도: {response.status_code}")
        
        if response.status_code == 200:
            recommendations = response.json()
            print("✅ 메뉴 추천 성공!")
            print(f"   추천 수: {len(recommendations)}개")
            if len(recommendations) > 0:
                print(f"   첫 추천: {recommendations[0].get('menu_name', 'N/A')}")
        else:
            print(f"❌ 메뉴 추천 실패: {response.status_code}")
            print(f"   응답: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ 메뉴 추천 실패: {e}")

if __name__ == "__main__":
    test_render_profile_direct()
