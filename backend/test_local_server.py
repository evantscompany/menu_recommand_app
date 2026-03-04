"""
로컬 서버 테스트
"""

import requests
import time
import json

LOCAL_URL = "http://127.0.0.1:8000"

class LocalServerTest:
    def __init__(self):
        self.results = {}
        self.auth_token = None
        
    def test_server_status(self):
        """로컬 서버 상태 테스트"""
        print("🔍 1. 로컬 서버 상태 테스트")
        print("=" * 50)
        
        try:
            response = requests.get(f"{LOCAL_URL}/", timeout=5)
            if response.status_code == 200:
                print("✅ 로컬 서버 정상 작동")
                self.results['server_status'] = True
                return True
            else:
                print(f"❌ 로컬 서버 응답 오류: {response.status_code}")
                self.results['server_status'] = False
                return False
        except Exception as e:
            print(f"❌ 로컬 서버 연결 실패: {e}")
            print("   서버가 실행 중인지 확인하세요.")
            self.results['server_status'] = False
            return False
    
    def test_login(self):
        """로컬 로그인 테스트"""
        print("\n🔍 2. 로컬 로그인 테스트")
        print("=" * 50)
        
        try:
            login_data = {
                "username": "aaa",
                "password": "password123"
            }
            
            response = requests.post(
                f"{LOCAL_URL}/api/auth/login",
                json=login_data,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("access_token")
                print("✅ 로컬 로그인 성공")
                print(f"🔑 토큰: {self.auth_token[:20]}...")
                self.results['login'] = True
                return True
            else:
                print(f"❌ 로컬 로그인 실패: {response.status_code}")
                print(f"📄 응답: {response.text}")
                self.results['login'] = False
                return False
        except Exception as e:
            print(f"❌ 로컬 로그인 오류: {e}")
            self.results['login'] = False
            return False
    
    def test_signup(self):
        """로컬 회원가입 테스트"""
        print("\n🔍 3. 로컬 회원가입 테스트")
        print("=" * 50)
        
        try:
            import random
            random_num = random.randint(1000, 9999)
            signup_data = {
                "username": f"localtest_{random_num}",
                "password": "password123",
                "nickname": f"로컬테스트{random_num}",
                "email": f"localtest{random_num}@example.com"
            }
            
            response = requests.post(
                f"{LOCAL_URL}/api/auth/signup",
                json=signup_data,
                timeout=5
            )
            
            if response.status_code in [200, 201]:
                print("✅ 로컬 회원가입 성공")
                self.results['signup'] = True
                return True
            else:
                print(f"❌ 로컬 회원가입 실패: {response.status_code}")
                print(f"📄 응답: {response.text}")
                self.results['signup'] = False
                return False
        except Exception as e:
            print(f"❌ 로컬 회원가입 오류: {e}")
            self.results['signup'] = False
            return False
    
    def test_menu_list(self):
        """로컬 메뉴 목록 테스트"""
        print("\n🔍 4. 로컬 메뉴 목록 테스트")
        print("=" * 50)
        
        try:
            response = requests.get(
                f"{LOCAL_URL}/api/menus/",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 로컬 메뉴 목록 조회 성공")
                print(f"📋 메뉴 수: {len(data) if isinstance(data, list) else 'N/A'}")
                self.results['menu_list'] = True
                return True
            else:
                print(f"❌ 로컬 메뉴 목록 실패: {response.status_code}")
                print(f"📄 응답: {response.text}")
                self.results['menu_list'] = False
                return False
        except Exception as e:
            print(f"❌ 로컬 메뉴 목록 오류: {e}")
            self.results['menu_list'] = False
            return False
    
    def test_weather(self):
        """로컬 날씨 정보 테스트"""
        print("\n🔍 5. 로컬 날씨 정보 테스트")
        print("=" * 50)
        
        try:
            response = requests.get(
                f"{LOCAL_URL}/api/weather/seoul",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 로컬 날씨 정보 조회 성공")
                print(f"🌡️ 온도: {data.get('temperature', 'N/A')}")
                self.results['weather'] = True
                return True
            else:
                print(f"❌ 로컬 날씨 정보 실패: {response.status_code}")
                self.results['weather'] = False
                return False
        except Exception as e:
            print(f"❌ 로컬 날씨 정보 오류: {e}")
            self.results['weather'] = False
            return False
    
    def run_local_tests(self):
        """로컬 서버 전체 테스트 실행"""
        print("🚀 로컬 서버 전체 기능 테스트 시작")
        print("=" * 60)
        print(f"🌐 로컬 서버 주소: {LOCAL_URL}")
        print("=" * 60)
        
        # 테스트 실행
        tests = [
            ("서버 상태", self.test_server_status),
            ("로그인", self.test_login),
            ("회원가입", self.test_signup),
            ("메뉴 목록", self.test_menu_list),
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
        print("\n🎯 로컬 테스트 결과 요약")
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
            'signup': '회원가입',
            'menu_list': '메뉴 목록',
            'weather': '날씨 정보'
        }
        
        for key, result in self.results.items():
            status = "✅" if result else "❌"
            test_name = test_names.get(key, key)
            print(f"  {status} {test_name}")
        
        print("\n🎯 다음 조치 필요:")
        if success_rate == 100:
            print("🎉 완벽한 성공! 로컬 서버는 정상 작동합니다!")
            print("✅ 이제 Render에 푸시해도 됩니다.")
        else:
            print("⚠️ 일부 기능에 문제가 있습니다.")
            print("🔧 문제를 수정한 후 다시 테스트하세요.")
        
        print("=" * 60)

if __name__ == "__main__":
    tester = LocalServerTest()
    tester.run_local_tests()
