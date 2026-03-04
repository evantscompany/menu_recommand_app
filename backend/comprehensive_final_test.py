"""
최종 전체 기능 테스트
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "https://menu-recommand-app.onrender.com"

class ComprehensiveTest:
    def __init__(self):
        self.results = {}
        self.auth_token = None
        
    def test_server_status(self):
        """서버 상태 테스트"""
        print("🔍 1. 서버 상태 테스트")
        print("=" * 50)
        
        try:
            response = requests.get(f"{BASE_URL}/", timeout=10)
            if response.status_code == 200:
                print("✅ 서버 정상 작동")
                self.results['server_status'] = True
                return True
            else:
                print(f"❌ 서버 응답 오류: {response.status_code}")
                self.results['server_status'] = False
                return False
        except Exception as e:
            print(f"❌ 서버 연결 실패: {e}")
            self.results['server_status'] = False
            return False
    
    def test_login(self):
        """로그인 테스트"""
        print("\n🔍 2. 로그인 테스트")
        print("=" * 50)
        
        try:
            login_data = {
                "username": "aaa",
                "password": "password123"
            }
            
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("access_token")
                print("✅ 로그인 성공")
                print(f"🔑 토큰: {self.auth_token[:20]}...")
                self.results['login'] = True
                return True
            else:
                print(f"❌ 로그인 실패: {response.status_code}")
                print(f"📄 응답: {response.text}")
                self.results['login'] = False
                return False
        except Exception as e:
            print(f"❌ 로그인 오류: {e}")
            self.results['login'] = False
            return False
    
    def test_user_info(self):
        """사용자 정보 테스트"""
        print("\n🔍 3. 사용자 정보 테스트")
        print("=" * 50)
        
        if not self.auth_token:
            print("❌ 인증 토큰 없음")
            self.results['user_info'] = False
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.get(
                f"{BASE_URL}/api/users/me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 사용자 정보 조회 성공")
                print(f"👤 사용자: {data.get('username', 'N/A')}")
                self.results['user_info'] = True
                return True
            else:
                print(f"❌ 사용자 정보 실패: {response.status_code}")
                self.results['user_info'] = False
                return False
        except Exception as e:
            print(f"❌ 사용자 정보 오류: {e}")
            self.results['user_info'] = False
            return False
    
    def test_menu_list(self):
        """메뉴 목록 테스트"""
        print("\n🔍 4. 메뉴 목록 테스트")
        print("=" * 50)
        
        try:
            response = requests.get(
                f"{BASE_URL}/api/menus/",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 메뉴 목록 조회 성공")
                print(f"📋 메뉴 수: {len(data) if isinstance(data, list) else 'N/A'}")
                self.results['menu_list'] = True
                return True
            else:
                print(f"❌ 메뉴 목록 실패: {response.status_code}")
                self.results['menu_list'] = False
                return False
        except Exception as e:
            print(f"❌ 메뉴 목록 오류: {e}")
            self.results['menu_list'] = False
            return False
    
    def test_authenticated_menu_list(self):
        """인증된 메뉴 목록 테스트"""
        print("\n🔍 5. 인증된 메뉴 목록 테스트")
        print("=" * 50)
        
        if not self.auth_token:
            print("❌ 인증 토큰 없음")
            self.results['auth_menu_list'] = False
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.get(
                f"{BASE_URL}/api/menus/my",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 인증된 메뉴 목록 조회 성공")
                print(f"📋 메뉴 수: {len(data) if isinstance(data, list) else 'N/A'}")
                self.results['auth_menu_list'] = True
                return True
            else:
                print(f"❌ 인증된 메뉴 목록 실패: {response.status_code}")
                self.results['auth_menu_list'] = False
                return False
        except Exception as e:
            print(f"❌ 인증된 메뉴 목록 오류: {e}")
            self.results['auth_menu_list'] = False
            return False
    
    def test_recommendation(self):
        """메뉴 추천 테스트"""
        print("\n🔍 6. 메뉴 추천 테스트")
        print("=" * 50)
        
        if not self.auth_token:
            print("❌ 인증 토큰 없음")
            self.results['recommendation'] = False
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = requests.get(
                f"{BASE_URL}/api/recommend/",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 메뉴 추천 성공")
                print(f"🍽 추천 메뉴: {data.get('restaurant_name', 'N/A')}")
                self.results['recommendation'] = True
                return True
            else:
                print(f"❌ 메뉴 추천 실패: {response.status_code}")
                print(f"📄 응답: {response.text}")
                self.results['recommendation'] = False
                return False
        except Exception as e:
            print(f"❌ 메뉴 추천 오류: {e}")
            self.results['recommendation'] = False
            return False
    
    def test_signup(self):
        """회원가입 테스트"""
        print("\n🔍 7. 회원가입 테스트")
        print("=" * 50)
        
        try:
            # 랜덤 사용자 데이터 생성
            import random
            random_num = random.randint(1000, 9999)
            signup_data = {
                "username": f"testuser_{random_num}",
                "password": "password123",
                "nickname": f"테스트유저{random_num}",
                "email": f"test{random_num}@example.com"
            }
            
            response = requests.post(
                f"{BASE_URL}/api/auth/signup",
                json=signup_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print("✅ 회원가입 성공")
                self.results['signup'] = True
                return True
            else:
                print(f"❌ 회원가입 실패: {response.status_code}")
                print(f"📄 응답: {response.text}")
                self.results['signup'] = False
                return False
        except Exception as e:
            print(f"❌ 회원가입 오류: {e}")
            self.results['signup'] = False
            return False
    
    def test_weather(self):
        """날씨 정보 테스트"""
        print("\n🔍 8. 날씨 정보 테스트")
        print("=" * 50)
        
        try:
            response = requests.get(
                f"{BASE_URL}/api/weather/seoul",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 날씨 정보 조회 성공")
                print(f"🌡️ 온도: {data.get('temperature', 'N/A')}")
                self.results['weather'] = True
                return True
            else:
                print(f"❌ 날씨 정보 실패: {response.status_code}")
                self.results['weather'] = False
                return False
        except Exception as e:
            print(f"❌ 날씨 정보 오류: {e}")
            self.results['weather'] = False
            return False
    
    def run_all_tests(self):
        """전체 테스트 실행"""
        print("🚀 최종 전체 기능 테스트 시작")
        print("=" * 60)
        print(f"📅 테스트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 서버 주소: {BASE_URL}")
        print("=" * 60)
        
        # 테스트 실행
        tests = [
            ("서버 상태", self.test_server_status),
            ("로그인", self.test_login),
            ("사용자 정보", self.test_user_info),
            ("메뉴 목록", self.test_menu_list),
            ("인증된 메뉴 목록", self.test_authenticated_menu_list),
            ("메뉴 추천", self.test_recommendation),
            ("회원가입", self.test_signup),
            ("날씨 정보", self.test_weather)
        ]
        
        for test_name, test_func in tests:
            try:
                test_func()
                time.sleep(1)  # 잠시 대기
            except Exception as e:
                print(f"❌ {test_name} 테스트 중 오류: {e}")
        
        # 결과 요약
        self.print_summary()
    
    def print_summary(self):
        """테스트 결과 요약"""
        print("\n🎯 테스트 결과 요약")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 전체 테스트: {total_tests}개")
        print(f"✅ 성공: {passed_tests}개")
        print(f"❌ 실패: {failed_tests}개")
        print(f"📈 성공률: {success_rate:.1f}%")
        
        print("\n📋 상세 결과:")
        test_names = {
            'server_status': '서버 상태',
            'login': '로그인',
            'user_info': '사용자 정보',
            'menu_list': '메뉴 목록',
            'auth_menu_list': '인증된 메뉴 목록',
            'recommendation': '메뉴 추천',
            'signup': '회원가입',
            'weather': '날씨 정보'
        }
        
        for key, result in self.results.items():
            status = "✅" if result else "❌"
            test_name = test_names.get(key, key)
            print(f"  {status} {test_name}")
        
        print("\n🎯 최종 평가:")
        if success_rate == 100:
            print("🎉 완벽한 성공! 모든 기능이 정상 작동합니다!")
        elif success_rate >= 80:
            print("👍 대부분 성공! 일부 기능만 수정하면 됩니다.")
        elif success_rate >= 60:
            print("⚠️ 절반 성공! 주요 기능을 점검해야 합니다.")
        else:
            print("❌ 많은 문제가 있습니다. 전체적인 점검이 필요합니다.")
        
        print("=" * 60)

if __name__ == "__main__":
    tester = ComprehensiveTest()
    tester.run_all_tests()
