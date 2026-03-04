"""
Render 서버 CRUD 함수 테스트
"""
import requests
import json

RENDER_URL = "https://menu-recommand-app.onrender.com"

def test_render_crud():
    """Render 서버 CRUD 함수 테스트"""
    
    print("🔍 Render 서버 CRUD 함수 테스트")
    print("=" * 50)
    
    # 1. 로그인
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
    
    # 2. 직접 API 테스트 (CRUD 함수 호출)
    print("\n📋 메뉴 CRUD 함수 테스트:")
    
    # get_menus 함수 테스트
    try:
        # 직접 API 호출 대신, 에러 상세 정보를 얻기 위해 다른 방법 시도
        print("   get_menus 함수 호출...")
        
        # 파라미터를 다르게 시도
        test_params = [
            {},
            {"skip": 0},
            {"limit": 5},
            {"skip": 0, "limit": 5},
            {"skip": 1, "limit": 3}
        ]
        
        for params in test_params:
            try:
                response = requests.get(
                    f"{RENDER_URL}/api/menus",
                    params=params,
                    headers=headers,
                    timeout=10
                )
                
                print(f"   파라미터 {params}: {response.status_code}")
                
                if response.status_code == 500:
                    # 500 오류의 상세 내용 확인
                    print(f"      오류 내용: {response.text}")
                    
                    # 에러가 JSON 형식인지 확인
                    try:
                        error_json = response.json()
                        print(f"      에러 JSON: {error_json}")
                    except:
                        pass
                        
                elif response.status_code == 200:
                    data = response.json()
                    print(f"      성공: {len(data)}개 메뉴")
                    
            except Exception as e:
                print(f"   파라미터 {params}: 요청 실패 - {e}")
    
    except Exception as e:
        print(f"   CRUD 테스트 실패: {e}")
    
    # 3. 다른 엔드포인트 테스트
    print("\n🔍 다른 엔드포인트 테스트:")
    
    other_endpoints = [
        ("/api/users", "GET", "사용자 목록"),
        ("/api/users/me", "GET", "현재 사용자"),
    ]
    
    for endpoint, method, description in other_endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{RENDER_URL}{endpoint}", headers=headers, timeout=10)
            
            print(f"   {description}: {response.status_code}")
            
            if response.status_code != 200:
                print(f"      응답: {response.text[:200]}...")
            else:
                data = response.json()
                if isinstance(data, list):
                    print(f"      성공: {len(data)}개 항목")
                else:
                    print(f"      성공: {type(data).__name__}")
                    
        except Exception as e:
            print(f"   {description}: 실패 - {e}")
    
    # 4. 추천 시스템 디버깅
    print("\n🎯 추천 시스템 디버깅:")
    
    try:
        # 간단한 추천 데이터
        simple_recommend = {"user_profile": {"spicy_threshold": 3}}
        
        response = requests.post(
            f"{RENDER_URL}/api/recommend/",
            json=simple_recommend,
            headers=headers,
            timeout=10
        )
        
        print(f"   간단 추천: {response.status_code}")
        if response.status_code == 500:
            print(f"      오류: {response.text}")
            
    except Exception as e:
        print(f"   추천 시스템 실패: {e}")

if __name__ == "__main__":
    test_render_crud()
