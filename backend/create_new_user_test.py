"""
새로운 사용자 생성 및 테스트
"""
import requests
import random
import string

RENDER_URL = "https://menu-recommand-app.onrender.com"

def generate_random_user():
    """랜덤 사용자 정보 생성"""
    random_num = random.randint(1000, 9999)
    return {
        "username": f"testuser{random_num}",
        "email": f"testuser{random_num}@example.com",
        "nickname": f"테스트유저{random_num}",
        "password": "testpass123",
        "dietary_label": "none",
        "allergies": "",
        "spicy_threshold": 3,
        "saltiness_preference": 3,
        "lunch_budget_max": 12000,
        "is_adventurous": True
    }

def test_new_user_creation():
    """새로운 사용자 생성 테스트"""
    
    print("👤 새로운 사용자 생성 테스트")
    print("=" * 50)
    
    # 1. 새로운 사용자 정보 생성
    new_user = generate_random_user()
    print(f"📝 생성할 사용자 정보:")
    print(f"   아이디: {new_user['username']}")
    print(f"   이메일: {new_user['email']}")
    print(f"   닉네임: {new_user['nickname']}")
    print(f"   비밀번호: {new_user['password']}")
    print(f"   예산: {new_user['lunch_budget_max']}원")
    print(f"   맵기: {new_user['spicy_threshold']}")
    
    # 2. 회원가입 시도
    try:
        response = requests.post(
            f"{RENDER_URL}/api/auth/signup",
            json=new_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\n📋 회원가입 시도: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ 회원가입 성공!")
            print(f"   생성된 사용자 ID: {result.get('user_id', 'N/A')}")
            print(f"   생성된 사용자명: {result.get('username', 'N/A')}")
            
            # 3. 생성된 사용자로 로그인 테스트
            print(f"\n🔐 생성된 사용자로 로그인 테스트:")
            login_response = requests.post(
                f"{RENDER_URL}/api/auth/login-json",
                json={"username": new_user['username'], "password": new_user['password']},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if login_response.status_code == 200:
                token = login_response.json().get("access_token", "")
                print("✅ 로그인 성공!")
                print(f"   토큰: {token[:20]}...")
                
                # 4. 사용자 정보 확인
                headers = {"Authorization": f"Bearer {token}"}
                user_info_response = requests.get(f"{RENDER_URL}/api/users/me", headers=headers, timeout=10)
                
                if user_info_response.status_code == 200:
                    user_data = user_info_response.json()
                    print("✅ 사용자 정보 확인 성공!")
                    print(f"   사용자: {user_data.get('username', 'N/A')}")
                    print(f"   이메일: {user_data.get('email', 'N/A')}")
                    
                    # profile 정보 확인
                    if 'profile' in user_data:
                        profile = user_data['profile']
                        if profile:
                            print(f"   프로필 예산: {profile.get('lunch_budget_max', 'N/A')}")
                            print(f"   프로필 맵기: {profile.get('spicy_threshold', 'N/A')}")
                        else:
                            print("   ⚠️ 프로필 정보 없음")
                    else:
                        print("   ⚠️ profile 키 없음")
                else:
                    print(f"❌ 사용자 정보 확인 실패: {user_info_response.status_code}")
                    print(f"   응답: {user_info_response.text[:200]}...")
                
                # 5. 메뉴 추천 테스트
                print(f"\n🎯 메뉴 추천 테스트:")
                recommend_response = requests.get(f"{RENDER_URL}/api/recommend/recommendations", headers=headers, timeout=10)
                
                if recommend_response.status_code == 200:
                    recommendations = recommend_response.json()
                    print("✅ 메뉴 추천 성공!")
                    print(f"   추천 수: {len(recommendations)}개")
                    if len(recommendations) > 0:
                        print(f"   첫 추천: {recommendations[0].get('menu_name', 'N/A')}")
                else:
                    print(f"❌ 메뉴 추천 실패: {recommend_response.status_code}")
                    print(f"   응답: {recommend_response.text[:200]}...")
                
            else:
                print(f"❌ 로그인 실패: {login_response.status_code}")
                print(f"   응답: {login_response.text[:200]}...")
                
        else:
            print(f"❌ 회원가입 실패: {response.status_code}")
            print(f"   응답: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")

if __name__ == "__main__":
    test_new_user_creation()
