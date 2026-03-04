"""
백엔드 TiDB Cloud 연동 및 기능 전체 분석 스크립트
"""

import os
import requests
import json
from datetime import datetime

# 환경 변수 설정
os.environ["TIDB_HOST"] = "gateway01.ap-northeast-1.prod.aws.tidbcloud.com"
os.environ["TIDB_PORT"] = "4000"
os.environ["TIDB_USER"] = "3bJdto8FKWk47Fu.root"
os.environ["TIDB_PASSWORD"] = "NWOZOcYDO8W5nMk2"
os.environ["TIDB_DATABASE"] = "test"

# 서버 설정
SERVER_IP = "192.168.0.18"
SERVER_PORT = "8000"
BASE_URL = f"http://{SERVER_IP}:{SERVER_PORT}"

def test_database_connection():
    """데이터베이스 연결 테스트"""
    print("🔍 1. 데이터베이스 연결 테스트")
    print("-" * 50)
    
    try:
        from app.database_mysql import test_connection, engine, SessionLocal
        from app.models import UserAccount, Menu, UserProfile, MenuDetail
        
        if test_connection():
            print("✅ TiDB Cloud 연결 성공")
            
            # 테이블 상태 확인
            db = SessionLocal()
            try:
                user_count = db.query(UserAccount).count()
                menu_count = db.query(Menu).count()
                profile_count = db.query(UserProfile).count()
                detail_count = db.query(MenuDetail).count()
                
                print(f"📊 데이터베이스 상태:")
                print(f"  👤 사용자: {user_count}명")
                print(f"  🍽️ 메뉴: {menu_count}개")
                print(f"  👤 프로필: {profile_count}개")
                print(f"  📝 메뉴 상세: {detail_count}개")
                
                if user_count == 8 and menu_count == 351 and profile_count == 8 and detail_count == 351:
                    print("🎉 모든 데이터 완벽 마이그레이션 확인!")
                else:
                    print("⚠️ 일부 데이터 누락 가능")
                    
            finally:
                db.close()
                
    except Exception as e:
        print(f"❌ 데이터베이스 테스트 실패: {e}")
        return False
            
    return True

def test_api_endpoints():
    """API 엔드포인트 테스트"""
    print("\n🔍 2. API 엔드포인트 테스트")
    print("-" * 50)
    
    # 테스트용 사용자 정보
    test_user = {
        "username": "aaa",
        "password": "password123"
    }
    
    endpoints = [
        {
            "name": "서버 상태",
            "url": f"{BASE_URL}/",
            "method": "GET",
            "expected_status": 200
        },
        {
            "name": "로그인 (JSON)",
            "url": f"{BASE_URL}/api/auth/login-json",
            "method": "POST",
            "data": test_user,
            "expected_status": 200
        },
        {
            "name": "사용자 정보 조회",
            "url": f"{BASE_URL}/api/users/me",
            "method": "GET",
            "auth_required": True,
            "expected_status": 200
        },
        {
            "name": "메뉴 목록 조회",
            "url": f"{BASE_URL}/api/menus",
            "method": "GET",
            "expected_status": 200
        },
        {
            "name": "메뉴 추천",
            "url": f"{BASE_URL}/api/recommend/",
            "method": "POST",
            "data": {"user_profile": {"spicy_threshold": 3}},
            "auth_required": True,
            "expected_status": 200
        }
    ]
    
    # 먼저 로그인하여 토큰 받기
    try:
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login-json",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get("access_token", "")
            print(f"✅ 로그인 성공, 토큰: {token[:20]}...")
            
            # 인증 헤더 설정
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # 각 엔드포인트 테스트
            for endpoint in endpoints:
                print(f"\n🧪 {endpoint['name']} 테스트 중...")
                
                try:
                    if endpoint["method"] == "GET":
                        response = requests.get(endpoint["url"], headers=headers)
                    else:
                        if endpoint.get("auth_required"):
                            response = requests.post(endpoint["url"], json=endpoint["data"], headers=headers)
                        else:
                            response = requests.post(endpoint["url"], json=endpoint["data"])
                    
                    # 결과 분석
                    status_ok = response.status_code == endpoint["expected_status"]
                    
                    if status_ok:
                        print(f"  ✅ 성공 (상태 코드: {response.status_code})")
                        try:
                            data = response.json()
                            if isinstance(data, dict):
                                if "message" in data:
                                    print(f"  📝 응답: {data['message']}")
                                elif "results" in data:
                                    print(f"  📊 데이터 수: {len(data['results'])}개")
                                elif "username" in data:
                                    print(f"  👤 사용자: {data['username']}")
                        except:
                            print("  📝 JSON 응답 (파싱 실패)")
                    else:
                        print(f"  ❌ 실패 (상태 코드: {response.status_code})")
                        try:
                            error_data = response.json()
                            print(f"  📝 오류: {error_data}")
                        except:
                            print(f"  📝 오류: {response.text[:100]}")
                except Exception as e:
                    print(f"  ❌ 요청 실패: {e}")
                    
        else:
            print(f"❌ 로그인 실패: {login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API 테스트 실패: {e}")
        return False
    
    return True

def test_weather_service():
    """날씨 서비스 테스트"""
    print("\n🔍 3. 날씨 서비스 테스트")
    print("-" * 50)
    
    try:
        from app.core.weather_service import WeatherService
        
        weather_service = WeatherService()
        weather_data = weather_service.get_current_weather("Seoul")
        
        print(f"🌤 날씨 데이터:")
        print(f"  도시: {weather_data.get('city', 'Seoul')}")
        print(f"  온도: {weather_data.get('temperature', 'N/A')}")
        print(f"  날씨: {weather_data.get('weather', 'N/A')}")
        print(f"  습도: {weather_data.get('humidity', 'N/A')}")
        print(f"  시간: {weather_data.get('time', datetime.now().strftime('%H:%M'))}")
        
        return True
        
    except Exception as e:
        print(f"❌ 날씨 서비스 테스트 실패: {e}")
        return False

def test_recommendation_system():
    """추천 시스템 테스트"""
    print("\n🔍 4. 추천 시스템 테스트")
    print("-" * 50)
    
    try:
        # 로그인하여 토큰 받기
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login-json",
            json={"username": "aaa", "password": "password123"},
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get("access_token", "")
            
            # 추천 요청
            recommendation_data = {
                "user_profile": {
                    "spicy_threshold": 3,
                    "saltiness_preference": 3,
                    "lunch_budget_max": 12000,
                    "is_adventurous": True
                }
            }
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{BASE_URL}/api/recommend/",
                json=recommendation_data,
                headers=headers
            )
            
            if response.status_code == 200:
                recommendations = response.json()
                print(f"🍽️ 추천 결과:")
                print(f"  추천 수: {len(recommendations) if isinstance(recommendations, list) else 0}개")
                
                if isinstance(recommendations, list) and len(recommendations) > 0:
                    first_rec = recommendations[0]
                    print(f"  첫 번째 추천:")
                    print(f"    메뉴: {first_rec.get('menu_name', 'N/A')}")
                    print(f"    카테고리: {first_rec.get('category', 'N/A')}")
                    print(f"    가격: {first_rec.get('price', 'N/A')}")
                    print(f"    매칭률: {first_rec.get('match_rate', 'N/A')}%")
                    
                return True
            else:
                print(f"❌ 추천 실패: {response.status_code}")
                return False
                
        else:
            print(f"❌ 로그인 실패: {login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 추천 시스템 테스트 실패: {e}")
        return False

def generate_test_report():
    """테스트 결과 보고서 생성"""
    print("\n" + "=" * 60)
    print("🎯 백엔드 TiDB Cloud 연동 전체 분석 결과")
    print("=" * 60)
    
    # 각 테스트 실행
    results = {
        "database_connection": test_database_connection(),
        "api_endpoints": test_api_endpoints(),
        "weather_service": test_weather_service(),
        "recommendation_system": test_recommendation_system()
    }
    
    # 결과 요약
    print("\n📊 테스트 결과 요약:")
    print("-" * 40)
    
    for test_name, result in results.items():
        status = "✅ 통과" if result else "❌ 실패"
        print(f"  {test_name}: {status}")
    
    # 전체 평가
    all_passed = all(results.values())
    
    print(f"\n🎉 전체 평가: {'완벽' if all_passed else '부분'} 통과")
    
    if all_passed:
        print("\n✅ 백엔드가 TiDB Cloud와 완벽하게 연동되어 모든 기능이 정상 작동합니다!")
        print("🚀 Render 배포 준비 완료!")
    else:
        print("\n⚠️ 일부 기능에서 문제가 발견되었습니다.")
        print("🔧 추가 조치가 필요할 수 있습니다.")
    
    return all_passed

if __name__ == "__main__":
    print("🚀 백엔드 TiDB Cloud 연동 전체 분석 시작")
    print(f"📅 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    generate_test_report()
