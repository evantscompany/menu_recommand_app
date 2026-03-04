"""
Render 서버 로그 및 상세 테스트
"""
import requests
import time

def check_render_health():
    """Render 서버 상세 상태 확인"""
    
    RENDER_URL = "https://menu-recommand-app.onrender.com"
    
    print("🔍 Render 서버 상세 상태 확인")
    print("=" * 50)
    
    # 1. 기본 상태 확인
    try:
        response = requests.get(RENDER_URL, timeout=30)
        print(f"✅ 서버 응답: {response.status_code}")
        print(f"   응답 시간: {response.elapsed.total_seconds():.2f}초")
        print(f"   응답: {response.json()}")
    except Exception as e:
        print(f"❌ 서버 연결 실패: {e}")
        return
    
    # 2. 헬스 체크 엔드포인트 테스트
    endpoints = [
        ("/api/menus", "메뉴 목록"),
        ("/api/auth/login-json", "로그인"),
        ("/api/users/me", "사용자 정보"),
        ("/api/recommend/", "추천 시스템")
    ]
    
    print(f"\n📋 API 엔드포인트 테스트:")
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{RENDER_URL}{endpoint}", timeout=10)
            status_icon = "✅" if response.status_code == 200 else "❌"
            print(f"   {status_icon} {name}: {response.status_code}")
            
            if response.status_code != 200:
                print(f"      응답: {response.text[:100]}...")
        except Exception as e:
            print(f"   ❌ {name}: 연결 실패 - {e}")
    
    # 3. POST 요청 테스트
    print(f"\n📝 POST 요청 테스트:")
    
    # 로그인 테스트
    try:
        login_data = {"username": "aaa", "password": "password123"}
        response = requests.post(
            f"{RENDER_URL}/api/auth/login-json",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"   로그인: {response.status_code}")
        if response.status_code != 200:
            print(f"      응답: {response.text}")
    except Exception as e:
        print(f"   로그인: 실패 - {e}")
    
    # 4. 데이터베이스 연결 테스트
    print(f"\n🗄️ 데이터베이스 연결 테스트:")
    try:
        # 간단한 메뉴 조회로 DB 연결 확인
        response = requests.get(f"{RENDER_URL}/api/menus?limit=1", timeout=10)
        if response.status_code == 200:
            menus = response.json()
            if len(menus) > 0:
                print(f"   ✅ DB 연결 정상 (메뉴 데이터 있음)")
            else:
                print(f"   ⚠️ DB 연결됨 but 데이터 없음")
        else:
            print(f"   ❌ DB 연결 문제: {response.status_code}")
            print(f"      응답: {response.text[:100]}...")
    except Exception as e:
        print(f"   ❌ DB 테스트 실패: {e}")
    
    print(f"\n🎯 진단 결과:")
    print(f"   - 서버는 실행 중이지만 API 엔드포인트에 문제")
    print(f"   - 데이터베이스 연결 또는 코드 문제 가능성")
    print(f"   - Render 로그 확인 필요")

if __name__ == "__main__":
    check_render_health()
