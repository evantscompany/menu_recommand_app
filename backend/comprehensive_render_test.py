"""
Render 배포된 서버 전체 기능 테스트 및 디버깅
"""
import requests
import json
from datetime import datetime

RENDER_URL = "https://menu-recommand-app.onrender.com"

class RenderTester:
    def __init__(self):
        self.token = None
        self.test_results = {}
    
    def log_result(self, test_name, success, details=""):
        """테스트 결과 기록"""
        status = "✅" if success else "❌"
        self.test_results[test_name] = {"success": success, "details": details}
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
    
    def test_server_health(self):
        """서버 상태 테스트"""
        try:
            response = requests.get(RENDER_URL, timeout=10)
            if response.status_code == 200:
                self.log_result("서버 상태", True, f"응답: {response.json()}")
                return True
            else:
                self.log_result("서버 상태", False, f"상태 코드: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("서버 상태", False, f"연결 실패: {e}")
            return False
    
    def test_login(self, username="aaa", password="password123"):
        """로그인 테스트"""
        try:
            response = requests.post(
                f"{RENDER_URL}/api/auth/login-json",
                json={"username": username, "password": password},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token", "")
                self.log_result("로그인", True, f"토큰: {self.token[:20]}...")
                return True
            else:
                self.log_result("로그인", False, f"상태 코드: {response.status_code}, 응답: {response.text}")
                return False
        except Exception as e:
            self.log_result("로그인", False, f"요청 실패: {e}")
            return False
    
    def test_user_info(self):
        """사용자 정보 조회 테스트"""
        if not self.token:
            self.log_result("사용자 정보", False, "로그인 토큰 없음")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{RENDER_URL}/api/users/me", headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                self.log_result("사용자 정보", True, f"사용자: {user_data.get('username', 'N/A')}")
                return True
            else:
                self.log_result("사용자 정보", False, f"상태 코드: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("사용자 정보", False, f"요청 실패: {e}")
            return False
    
    def test_menu_list(self):
        """메뉴 목록 조회 테스트"""
        try:
            response = requests.get(f"{RENDER_URL}/api/menus", timeout=10)
            
            if response.status_code == 200:
                menus = response.json()
                self.log_result("메뉴 목록", True, f"메뉴 수: {len(menus)}개")
                return True
            else:
                error_detail = response.text[:200] if response.text else "내용 없음"
                self.log_result("메뉴 목록", False, f"상태 코드: {response.status_code}, 오류: {error_detail}")
                return False
        except Exception as e:
            self.log_result("메뉴 목록", False, f"요청 실패: {e}")
            return False
    
    def test_menu_with_auth(self):
        """인증된 메뉴 목록 조회 테스트"""
        if not self.token:
            self.log_result("인증된 메뉴 목록", False, "로그인 토큰 없음")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{RENDER_URL}/api/menus", headers=headers, timeout=10)
            
            if response.status_code == 200:
                menus = response.json()
                self.log_result("인증된 메뉴 목록", True, f"메뉴 수: {len(menus)}개")
                return True
            else:
                error_detail = response.text[:200] if response.text else "내용 없음"
                self.log_result("인증된 메뉴 목록", False, f"상태 코드: {response.status_code}, 오류: {error_detail}")
                return False
        except Exception as e:
            self.log_result("인증된 메뉴 목록", False, f"요청 실패: {e}")
            return False
    
    def test_recommendation(self):
        """메뉴 추천 테스트"""
        if not self.token:
            self.log_result("메뉴 추천", False, "로그인 토큰 없음")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
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
                self.log_result("메뉴 추천", True, f"추천 수: {len(recommendations)}개")
                return True
            else:
                error_detail = response.text[:200] if response.text else "내용 없음"
                self.log_result("메뉴 추천", False, f"상태 코드: {response.status_code}, 오류: {error_detail}")
                return False
        except Exception as e:
            self.log_result("메뉴 추천", False, f"요청 실패: {e}")
            return False
    
    def test_signup(self):
        """회원가입 테스트"""
        try:
            new_user = {
                "username": f"testuser_{datetime.now().strftime('%H%M%S')}",
                "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
                "nickname": "테스트유저",
                "password": "testpass123"
            }
            
            response = requests.post(
                f"{RENDER_URL}/api/auth/signup",
                json=new_user,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                self.log_result("회원가입", True, f"생성된 사용자: {new_user['username']}")
                return new_user
            else:
                error_detail = response.text[:200] if response.text else "내용 없음"
                self.log_result("회원가입", False, f"상태 코드: {response.status_code}, 오류: {error_detail}")
                return None
        except Exception as e:
            self.log_result("회원가입", False, f"요청 실패: {e}")
            return None
    
    def test_weather(self):
        """날씨 정보 테스트"""
        try:
            response = requests.get(f"{RENDER_URL}/api/weather/seoul", timeout=10)
            
            if response.status_code == 200:
                weather = response.json()
                self.log_result("날씨 정보", True, f"도시: {weather.get('city', 'N/A')}")
                return True
            else:
                self.log_result("날씨 정보", False, f"상태 코드: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("날씨 정보", False, f"요청 실패: {e}")
            return False
    
    def debug_database_connection(self):
        """데이터베이스 연결 디버깅"""
        print("\n🔍 데이터베이스 연결 디버깅")
        print("-" * 40)
        
        # 로컬에서 DB 연결 테스트
        try:
            import os
            import pymysql
            
            conn = pymysql.connect(
                host=os.getenv("TIDB_HOST", "gateway01.ap-northeast-1.prod.aws.tidbcloud.com"),
                port=int(os.getenv("TIDB_PORT", "4000")),
                user=os.getenv("TIDB_USER", "3bJdto8FKWk47Fu.root"),
                password=os.getenv("TIDB_PASSWORD", "NWOZOcYDO8W5nMk2"),
                database=os.getenv("TIDB_DATABASE", "test"),
                ssl={"ssl": True},
                charset='utf8mb4'
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM menus")
            count = cursor.fetchone()[0]
            
            print(f"✅ 로컬 DB 연결 성공: menus 테이블 {count}개 레코드")
            conn.close()
            
        except Exception as e:
            print(f"❌ 로컬 DB 연결 실패: {e}")
    
    def run_all_tests(self):
        """전체 테스트 실행"""
        print("🚀 Render 배포된 서버 전체 기능 테스트")
        print("=" * 60)
        print(f"📍 테스트 대상: {RENDER_URL}")
        print(f"📅 테스트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 기본 테스트
        self.test_server_health()
        self.test_login()
        self.test_user_info()
        
        # 메뉴 관련 테스트
        self.test_menu_list()
        self.test_menu_with_auth()
        
        # 기능 테스트
        self.test_recommendation()
        self.test_signup()
        self.test_weather()
        
        # 결과 요약
        print("\n" + "=" * 60)
        print("🎯 테스트 결과 요약")
        print("=" * 60)
        
        success_count = sum(1 for result in self.test_results.values() if result["success"])
        total_count = len(self.test_results)
        
        for test_name, result in self.test_results.items():
            status = "✅" if result["success"] else "❌"
            print(f"{status} {test_name}")
        
        print(f"\n📊 전체 성공률: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
        
        # 실패한 테스트 분석
        failed_tests = [name for name, result in self.test_results.items() if not result["success"]]
        if failed_tests:
            print(f"\n🚨 실패한 기능: {', '.join(failed_tests)}")
            self.debug_database_connection()
        
        return success_count == total_count

if __name__ == "__main__":
    tester = RenderTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 모든 기능이 정상 작동합니다!")
    else:
        print("\n⚠️ 일부 기능에서 문제가 발견되었습니다.")
        print("🔧 디버깅 정보를 확인하세요.")
