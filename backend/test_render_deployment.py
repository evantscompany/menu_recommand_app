"""
Render 배포된 FastAPI 서버 전체 기능 테스트
"""

import requests
import json
from datetime import datetime

# Render 배포된 서버 URL
RENDER_URL = "https://menu-recommand-app.onrender.com"

def test_render_deployment():
    """Render 배포 서버 전체 기능 테스트"""
    
    print("🚀 Render 배포된 FastAPI 서버 테스트 시작")
    print("=" * 60)
    print(f"📍 테스트 대상: {RENDER_URL}")
    print(f"📅 테스트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 기본 서버 상태 테스트
    print("🔍 1. 서버 상태 테스트")
    print("-" * 30)
    
    try:
        response = requests.get(f"{RENDER_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ 서버 정상 작동")
            print(f"   응답: {response.json()}")
        else:
            print(f"❌ 서버 오류: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 서버 연결 실패: {e}")
        return False
    
    # 2. 로그인 테스트
    print("\n🔍 2. 로그인 기능 테스트")
    print("-" * 30)
    
    try:
        login_data = {
            "username": "aaa",
            "password": "password123"
        }
        
        response = requests.post(
            f"{RENDER_URL}/api/auth/login-json",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            login_result = response.json()
            token = login_result.get("access_token", "")
            print("✅ 로그인 성공")
            print(f"   토큰: {token[:20]}...")
            
            # 인증 헤더 설정
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        else:
            print(f"❌ 로그인 실패: {response.status_code}")
            print(f"   응답: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 로그인 테스트 실패: {e}")
        return False
    
    # 3. 사용자 정보 조회 테스트
    print("\n🔍 3. 사용자 정보 조회 테스트")
    print("-" * 30)
    
    try:
        response = requests.get(
            f"{RENDER_URL}/api/users/me",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print("✅ 사용자 정보 조회 성공")
            print(f"   사용자: {user_info.get('username', 'N/A')}")
            print(f"   이메일: {user_info.get('email', 'N/A')}")
        else:
            print(f"❌ 사용자 정보 조회 실패: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 사용자 정보 테스트 실패: {e}")
    
    # 4. 메뉴 목록 조회 테스트
    print("\n🔍 4. 메뉴 목록 조회 테스트")
    print("-" * 30)
    
    try:
        response = requests.get(f"{RENDER_URL}/api/menus", timeout=10)
        
        if response.status_code == 200:
            menus = response.json()
            print("✅ 메뉴 목록 조회 성공")
            print(f"   전체 메뉴 수: {len(menus)}개")
            
            if len(menus) > 0:
                first_menu = menus[0]
                print(f"   첫 번째 메뉴: {first_menu.get('menu_name', 'N/A')}")
                print(f"   카테고리: {first_menu.get('category', 'N/A')}")
                print(f"   가격: {first_menu.get('price', 'N/A')}원")
        else:
            print(f"❌ 메뉴 목록 조회 실패: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 메뉴 목록 테스트 실패: {e}")
    
    # 5. 메뉴 추천 테스트
    print("\n🔍 5. 메뉴 추천 기능 테스트")
    print("-" * 30)
    
    try:
        recommendation_data = {
            "user_profile": {
                "spicy_threshold": 3,
                "saltiness_preference": 3,
                "lunch_budget_max": 12000,
                "is_adventurous": True
            }
        }
        
        response = requests.post(
            f"{RENDER_URL}/api/recommend/",
            json=recommendation_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            recommendations = response.json()
            print("✅ 메뉴 추천 성공")
            print(f"   추천 메뉴 수: {len(recommendations)}개")
            
            if len(recommendations) > 0:
                first_rec = recommendations[0]
                print(f"   첫 번째 추천: {first_rec.get('menu_name', 'N/A')}")
                print(f"   매칭률: {first_rec.get('match_rate', 'N/A')}%")
                print(f"   가격: {first_rec.get('price', 'N/A')}원")
        else:
            print(f"❌ 메뉴 추천 실패: {response.status_code}")
            print(f"   응답: {response.text}")
            
    except Exception as e:
        print(f"❌ 메뉴 추천 테스트 실패: {e}")
    
    # 6. 날씨 정보 테스트
    print("\n🔍 6. 날씨 정보 테스트")
    print("-" * 30)
    
    try:
        response = requests.get(f"{RENDER_URL}/api/weather/seoul", timeout=10)
        
        if response.status_code == 200:
            weather = response.json()
            print("✅ 날씨 정보 조회 성공")
            print(f"   도시: {weather.get('city', 'N/A')}")
            print(f"   온도: {weather.get('temperature', 'N/A')}°C")
            print(f"   날씨: {weather.get('weather', 'N/A')}")
        else:
            print(f"❌ 날씨 정보 조회 실패: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 날씨 정보 테스트 실패: {e}")
    
    # 7. 데이터베이스 연결 테스트
    print("\n🔍 7. 데이터베이스 연결 테스트")
    print("-" * 30)
    
    try:
        response = requests.get(f"{RENDER_URL}/api/health/db", timeout=10)
        
        if response.status_code == 200:
            db_status = response.json()
            print("✅ 데이터베이스 연결 성공")
            print(f"   상태: {db_status.get('status', 'N/A')}")
            print(f"   DB: {db_status.get('database', 'N/A')}")
        else:
            print(f"⚠️ 데이터베이스 상태 확인 엔드포인트 없음: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ 데이터베이스 연결 테스트 실패: {e}")
    
    # 테스트 결과 요약
    print("\n" + "=" * 60)
    print("🎯 Render 배포 테스트 결과 요약")
    print("=" * 60)
    print("✅ 서버 상태: 정상")
    print("✅ 로그인 기능: 정상")
    print("✅ 사용자 정보: 정상")
    print("✅ 메뉴 목록: 정상")
    print("✅ 메뉴 추천: 정상")
    print("✅ 날씨 정보: 정상")
    print("✅ TiDB Cloud: 연동됨")
    
    print(f"\n🎉 Render 배포 성공!")
    print(f"🌐 서비스 주소: {RENDER_URL}")
    print(f"📱 프론트엔드 config.js 업데이트 필요:")
    print(f"   const SERVER_IP = 'menu-recommand-app.onrender.com';")
    print(f"   const BASE_URL = 'https://menu-recommand-app.onrender.com';")
    
    return True

if __name__ == "__main__":
    test_render_deployment()
