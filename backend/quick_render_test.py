"""
빠른 Render 배포 테스트
"""
import requests

url = "https://menu-recommand-app.onrender.com"

# 1. 서버 상태
try:
    r = requests.get(url, timeout=5)
    print(f"서버 상태: {r.status_code} - {r.json()}")
except Exception as e:
    print(f"서버 연결 실패: {e}")

# 2. 메뉴 목록
try:
    r = requests.get(f"{url}/api/menus", timeout=5)
    print(f"메뉴 목록: {r.status_code} - {len(r.json())}개 메뉴")
except Exception as e:
    print(f"메뉴 조회 실패: {e}")

# 3. 로그인
try:
    r = requests.post(f"{url}/api/auth/login-json", 
                     json={"username": "aaa", "password": "password123"}, 
                     timeout=5)
    print(f"로그인: {r.status_code} - {r.json()}")
except Exception as e:
    print(f"로그인 실패: {e}")
