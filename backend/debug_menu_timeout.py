"""
메뉴 목록 타임아웃 문제 디버깅
"""

import requests
import time

LOCAL_URL = "http://127.0.0.1:8000"

def debug_menu_timeout():
    """메뉴 목록 타임아웃 문제 디버깅"""
    print("🔍 메뉴 목록 타임아웃 문제 디버깅")
    print("=" * 50)
    
    # 1. 기본 메뉴 목록 (타임아웃)
    print("1. 기본 메뉴 목록 (5초 타임아웃):")
    try:
        start_time = time.time()
        response = requests.get(f"{LOCAL_URL}/api/menus/", timeout=10)
        end_time = time.time()
        
        print(f"   상태 코드: {response.status_code}")
        print(f"   응답 시간: {end_time - start_time:.2f}초")
        if response.status_code == 200:
            data = response.json()
            print(f"   메뉴 수: {len(data) if isinstance(data, list) else 'N/A'}")
        else:
            print(f"   응답: {response.text[:200]}...")
    except Exception as e:
        print(f"   오류: {e}")
    
    # 2. 메뉴 목록 (슬래시 없음)
    print("\n2. 메뉴 목록 (슬래시 없음, 5초 타임아웃):")
    try:
        start_time = time.time()
        response = requests.get(f"{LOCAL_URL}/api/menus", timeout=10)
        end_time = time.time()
        
        print(f"   상태 코드: {response.status_code}")
        print(f"   응답 시간: {end_time - start_time:.2f}초")
        if response.status_code == 200:
            data = response.json()
            print(f"   메뉴 수: {len(data) if isinstance(data, list) else 'N/A'}")
        else:
            print(f"   응답: {response.text[:200]}...")
    except Exception as e:
        print(f"   오류: {e}")
    
    # 3. 메뉴 목록 (짧은 타임아웃)
    print("\n3. 메뉴 목록 (1초 타임아웃):")
    try:
        start_time = time.time()
        response = requests.get(f"{LOCAL_URL}/api/menus/", timeout=5)
        end_time = time.time()
        
        print(f"   상태 코드: {response.status_code}")
        print(f"   응답 시간: {end_time - start_time:.2f}초")
        if response.status_code == 200:
            data = response.json()
            print(f"   메뉴 수: {len(data) if isinstance(data, list) else 'N/A'}")
        else:
            print(f"   응답: {response.text[:200]}...")
    except Exception as e:
        print(f"   오류: {e}")
    
    # 4. API 문서 확인
    print("\n4. API 문서 확인:")
    try:
        response = requests.get(f"{LOCAL_URL}/docs", timeout=5)
        print(f"   API 문서 상태: {response.status_code}")
    except Exception as e:
        print(f"   API 문서 오류: {e}")

if __name__ == "__main__":
    debug_menu_timeout()
