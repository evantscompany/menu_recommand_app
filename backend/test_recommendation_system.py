"""
메뉴 추천 시스템 테스트
"""

import requests
import json
import time

LOCAL_URL = "http://127.0.0.1:8000"

class RecommendationTest:
    def __init__(self):
        self.auth_token = None
        
    def login_and_get_token(self):
        """로그인하여 토큰 얻기"""
        print("🔑 로그인하여 토큰 얻기...")
        
        try:
            login_data = {
                "username": "aaa",
                "password": "password123"
            }
            
            response = requests.post(
                f"{LOCAL_URL}/api/auth/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("access_token")
                print("✅ 로그인 성공")
                print(f"🔑 토큰: {self.auth_token[:20]}...")
                return True
            else:
                print(f"❌ 로그인 실패: {response.status_code}")
                print(f"📄 응답: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 로그인 오류: {e}")
            return False
    
    def test_basic_recommendation(self):
        """기본 메뉴 추천 테스트"""
        print("\n🍽 1. 기본 메뉴 추천 테스트")
        print("=" * 50)
        
        if not self.auth_token:
            print("❌ 인증 토큰 없음")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            start_time = time.time()
            
            response = requests.get(
                f"{LOCAL_URL}/api/recommend/",
                headers=headers,
                timeout=15
            )
            
            end_time = time.time()
            
            print(f"   상태 코드: {response.status_code}")
            print(f"   응답 시간: {end_time - start_time:.2f}초")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 메뉴 추천 성공")
                print(f"🍽 추천 메뉴: {data[0].get('menu_name', 'N/A') if data and len(data) > 0 else 'N/A'}")
                print(f"📍 추천 이유: {data[0].get('description', 'N/A') if data and len(data) > 0 else 'N/A'}")
                print(f"⭐ 평점: {data[0].get('details', {}).get('rating', 'N/A') if data and len(data) > 0 else 'N/A'}")
                return True
            else:
                print(f"❌ 메뉴 추천 실패: {response.status_code}")
                print(f"📄 응답: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 메뉴 추천 오류: {e}")
            return False
    
    def test_recommendation_with_weather(self):
        """날씨 정보 포함 메뉴 추천 테스트"""
        print("\n🌡️ 2. 날씨 정보 포함 메뉴 추천 테스트")
        print("=" * 50)
        
        if not self.auth_token:
            print("❌ 인증 토큰 없음")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            start_time = time.time()
            
            response = requests.get(
                f"{LOCAL_URL}/api/recommend/?weather=seoul",
                headers=headers,
                timeout=15
            )
            
            end_time = time.time()
            
            print(f"   상태 코드: {response.status_code}")
            print(f"   응답 시간: {end_time - start_time:.2f}초")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 날씨 포함 메뉴 추천 성공")
                print(f"🍽 추천 메뉴: {data.get('restaurant_name', 'N/A')}")
                print(f"🌡️ 날씨: {data.get('weather', 'N/A')}")
                print(f"⭐ 평점: {data.get('rating', 'N/A')}")
                return True
            else:
                print(f"❌ 날씨 포함 메뉴 추천 실패: {response.status_code}")
                print(f"📄 응답: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 날씨 포함 메뉴 추천 오류: {e}")
            return False
    
    def test_recommendation_multiple_times(self):
        """여러 번 메뉴 추천 테스트 (일관성 확인)"""
        print("\n🔄 3. 여러 번 메뉴 추천 테스트 (일관성 확인)")
        print("=" * 50)
        
        if not self.auth_token:
            print("❌ 인증 토큰 없음")
            return False
        
        success_count = 0
        total_tests = 3
        
        for i in range(total_tests):
            print(f"\n   테스트 {i+1}/{total_tests}:")
            
            try:
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                start_time = time.time()
                
                response = requests.get(
                    f"{LOCAL_URL}/api/recommend/",
                    headers=headers,
                    timeout=10
                )
                
                end_time = time.time()
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ 성공 ({end_time - start_time:.2f}초)")
                    print(f"   🍽 메뉴: {data.get('restaurant_name', 'N/A')}")
                    success_count += 1
                else:
                    print(f"   ❌ 실패 ({response.status_code})")
                    print(f"   📄 응답: {response.text[:100]}...")
                
                time.sleep(1)  # 1초 대기
                
            except Exception as e:
                print(f"   ❌ 오류: {e}")
        
        success_rate = (success_count / total_tests) * 100
        print(f"\n   📊 성공률: {success_rate:.1f}% ({success_count}/{total_tests})")
        return success_rate == 100
    
    def test_recommendation_performance(self):
        """메뉴 추천 성능 테스트"""
        print("\n⚡ 4. 메뉴 추천 성능 테스트")
        print("=" * 50)
        
        if not self.auth_token:
            print("❌ 인증 토큰 없음")
            return False
        
        response_times = []
        
        for i in range(5):
            try:
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                start_time = time.time()
                
                response = requests.get(
                    f"{LOCAL_URL}/api/recommend/",
                    headers=headers,
                    timeout=10
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                
                if response.status_code == 200:
                    response_times.append(response_time)
                    print(f"   테스트 {i+1}: {response_time:.3f}초 ✅")
                else:
                    print(f"   테스트 {i+1}: 실패 ({response.status_code}) ❌")
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"   테스트 {i+1}: 오류 {e} ❌")
        
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
            
            print(f"\n   📊 성능 분석:")
            print(f"   평균 응답 시간: {avg_time:.3f}초")
            print(f"   최소 응답 시간: {min_time:.3f}초")
            print(f"   최대 응답 시간: {max_time:.3f}초")
            print(f"   성공 테스트: {len(response_times)}/5")
            
            return avg_time < 3.0  # 3초 이하면 양호
        else:
            return False
    
    def run_all_recommendation_tests(self):
        """전체 메뉴 추천 테스트 실행"""
        print("🚀 메뉴 추천 시스템 전체 테스트")
        print("=" * 60)
        print(f"🌐 로컬 서버 주소: {LOCAL_URL}")
        print("=" * 60)
        
        # 1. 로그인
        if not self.login_and_get_token():
            print("❌ 로그인 실패로 테스트 중단")
            return
        
        # 2. 기본 추천 테스트
        basic_success = self.test_basic_recommendation()
        
        # 3. 날씨 포함 추천 테스트
        weather_success = self.test_recommendation_with_weather()
        
        # 4. 여러 번 추천 테스트
        consistency_success = self.test_recommendation_multiple_times()
        
        # 5. 성능 테스트
        performance_success = self.test_recommendation_performance()
        
        # 결과 요약
        self.print_summary(basic_success, weather_success, consistency_success, performance_success)
    
    def print_summary(self, basic, weather, consistency, performance):
        """테스트 결과 요약"""
        print("\n🎯 메뉴 추천 테스트 결과 요약")
        print("=" * 60)
        
        results = {
            "기본 추천": basic,
            "날씨 포함 추천": weather,
            "일관성 테스트": consistency,
            "성능 테스트": performance
        }
        
        total_tests = len(results)
        passed_tests = sum(1 for result in results.values() if result)
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"📊 전체 테스트: {total_tests}개")
        print(f"✅ 성공: {passed_tests}개")
        print(f"❌ 실패: {total_tests - passed_tests}개")
        print(f"📈 성공률: {success_rate:.1f}%")
        
        print("\n📋 상세 결과:")
        for test_name, result in results.items():
            status = "✅" if result else "❌"
            print(f"  {status} {test_name}")
        
        print("\n🎯 최종 평가:")
        if success_rate == 100:
            print("🎉 메뉴 추천 시스템 완벽하게 작동합니다!")
            print("✅ Render 배포 준비 완료!")
        elif success_rate >= 75:
            print("👍 메뉴 추천 시스템 대부분 정상 작동합니다!")
            print("⚠️ 일부 기능만 수정하면 됩니다.")
        else:
            print("⚠️ 메뉴 추천 시스템에 문제가 있습니다.")
            print("🔧 추가적인 디버깅이 필요합니다.")
        
        print("=" * 60)

if __name__ == "__main__":
    tester = RecommendationTest()
    tester.run_all_recommendation_tests()
