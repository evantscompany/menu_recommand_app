"""
테스트 사용자 생성 스크립트
"""
import requests

RENDER_URL = "https://menu-recommand-app.onrender.com"

def create_test_user():
    """테스트 사용자 생성"""
    
    print("👤 테스트 사용자 생성")
    print("=" * 30)
    
    # 새로운 사용자 정보
    new_user = {
        "username": "testuser2024",
        "email": "testuser2024@example.com", 
        "nickname": "테스트유저2024",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{RENDER_URL}/api/auth/signup",
            json=new_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"회원가입 시도: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ 회원가입 성공!")
            print(f"📝 생성된 계정 정보:")
            print(f"   아이디: {new_user['username']}")
            print(f"   비밀번호: {new_user['password']}")
            print(f"   이메일: {new_user['email']}")
            print(f"   닉네임: {new_user['nickname']}")
            
            # 생성된 사용자로 로그인 테스트
            print(f"\n🔐 생성된 계정으로 로그인 테스트:")
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
                return True
            else:
                print(f"❌ 로그인 실패: {login_response.text}")
                return False
                
        else:
            print(f"❌ 회원가입 실패: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 회원가입 실패: {e}")
        return False

if __name__ == "__main__":
    success = create_test_user()
    
    if success:
        print(f"\n🎉 테스트 계정 생성 완료!")
        print(f"🌐 서비스 주소: {RENDER_URL}")
    else:
        print(f"\n💥 테스트 계정 생성 실패!")
