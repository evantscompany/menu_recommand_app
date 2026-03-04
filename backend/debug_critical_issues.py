"""
심각한 문제 디버깅
"""

import requests
import json

BASE_URL = "https://menu-recommand-app.onrender.com"

def debug_login_issue():
    """로그인 문제 디버깅"""
    print("🔍 로그인 문제 디버깅")
    print("=" * 50)
    
    # 1. 기본 로그인
    print("1. 기본 로그인 시도:")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": "aaa", "password": "password123"},
            timeout=10
        )
        print(f"   상태 코드: {response.status_code}")
        print(f"   응답: {response.text[:200]}...")
    except Exception as e:
        print(f"   오류: {e}")
    
    # 2. 헤더 추가
    print("\n2. 헤더 추가 로그인 시도:")
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": "aaa", "password": "password123"},
            headers=headers,
            timeout=10
        )
        print(f"   상태 코드: {response.status_code}")
        print(f"   응답: {response.text[:200]}...")
    except Exception as e:
        print(f"   오류: {e}")
    
    # 3. form-data 시도
    print("\n3. form-data 로그인 시도:")
    try:
        data = {"username": "aaa", "password": "password123"}
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data=data,
            timeout=10
        )
        print(f"   상태 코드: {response.status_code}")
        print(f"   응답: {response.text[:200]}...")
    except Exception as e:
        print(f"   오류: {e}")

def debug_menu_list_issue():
    """메뉴 목록 문제 디버깅"""
    print("\n🔍 메뉴 목록 문제 디버깅")
    print("=" * 50)
    
    # 1. 기본 메뉴 목록
    print("1. 기본 메뉴 목록:")
    try:
        response = requests.get(f"{BASE_URL}/api/menus/", timeout=10)
        print(f"   상태 코드: {response.status_code}")
        print(f"   응답: {response.text[:200]}...")
    except Exception as e:
        print(f"   오류: {e}")
    
    # 2. 메뉴 목록 (슬래시 없음)
    print("\n2. 메뉴 목록 (슬래시 없음):")
    try:
        response = requests.get(f"{BASE_URL}/api/menus", timeout=10)
        print(f"   상태 코드: {response.status_code}")
        print(f"   응답: {response.text[:200]}...")
    except Exception as e:
        print(f"   오류: {e}")

def debug_signup_issue():
    """회원가입 문제 디버깅"""
    print("\n🔍 회원가입 문제 디버깅")
    print("=" * 50)
    
    # 1. 기본 회원가입
    print("1. 기본 회원가입:")
    try:
        signup_data = {
            "username": "testuser12345",
            "password": "password123",
            "nickname": "테스트유저",
            "email": "test12345@example.com"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/signup",
            json=signup_data,
            timeout=10
        )
        print(f"   상태 코드: {response.status_code}")
        print(f"   응답: {response.text[:200]}...")
    except Exception as e:
        print(f"   오류: {e}")
    
    # 2. 최소 필드 회원가입
    print("\n2. 최소 필드 회원가입:")
    try:
        signup_data = {
            "username": "testuser67890",
            "password": "password123"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/signup",
            json=signup_data,
            timeout=10
        )
        print(f"   상태 코드: {response.status_code}")
        print(f"   응답: {response.text[:200]}...")
    except Exception as e:
        print(f"   오류: {e}")

def check_server_logs():
    """서버 로그 확인"""
    print("\n🔍 서버 로그 확인")
    print("=" * 50)
    
    try:
        # Render 로그 페이지 (가능하다면)
        response = requests.get(f"{BASE_URL}/logs", timeout=10)
        print(f"   로그 상태 코드: {response.status_code}")
        if response.status_code == 200:
            print(f"   로그: {response.text[:500]}...")
        else:
            print("   로그 접근 불가")
    except Exception as e:
        print(f"   로그 확인 오류: {e}")

def check_database_connection():
    """데이터베이스 연결 확인"""
    print("\n🔍 데이터베이스 연결 확인")
    print("=" * 50)
    
    try:
        # 데이터베이스 상태 확인 API (있다면)
        response = requests.get(f"{BASE_URL}/api/db/status", timeout=10)
        print(f"   DB 상태 코드: {response.status_code}")
        print(f"   DB 응답: {response.text[:200]}...")
    except Exception as e:
        print(f"   DB 확인 오류: {e}")

if __name__ == "__main__":
    print("🚨 심각한 문제 디버깅 시작")
    print("=" * 60)
    
    debug_login_issue()
    debug_menu_list_issue()
    debug_signup_issue()
    check_server_logs()
    check_database_connection()
    
    print("\n🎯 다음 조치 필요:")
    print("=" * 50)
    print("1. 로그인 API 요청 형식 확인")
    print("2. 메뉴 목록 500 오류 원인 파악")
    print("3. 회원가입 500 오류 원인 파악")
    print("4. 데이터베이스 연결 상태 확인")
    print("5. Render 로그에서 상세 오류 확인")
