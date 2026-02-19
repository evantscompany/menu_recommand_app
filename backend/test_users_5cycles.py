import requests
import json
import pandas as pd
from datetime import datetime
import time

# API 기본 설정
BASE_URL = "http://localhost:8000"
TEST_USERS = [
    {"username": "aaa", "password": "password123", "nickname": "매운맛 애호가"},
    {"username": "bbb", "password": "password123", "nickname": "건강식 애호가"},
    {"username": "ccc", "password": "password123", "nickname": "중용파"}
]

class MenuRecommendationTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.results = []
        self.session = requests.Session()
    
    def login(self, username, password):
        """로그인하여 토큰 발급"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                data={"username": username, "password": password}
            )
            if response.status_code == 200:
                token_data = response.json()
                token = token_data.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {token}"})
                return token, token_data
            else:
                print(f"❌ {username} 로그인 실패: {response.status_code}")
                return None, None
        except Exception as e:
            print(f"❌ {username} 로그인 오류: {e}")
            return None, None
    
    def get_recommendations(self):
        """추천 받기"""
        try:
            response = self.session.post(f"{self.base_url}/api/recommend/")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 추천 실패: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ 추천 오류: {e}")
            return None
    
    def select_menu(self, menu_id):
        """메뉴 선택"""
        try:
            response = self.session.post(f"{self.base_url}/api/recommend/select/{menu_id}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 메뉴 선택 실패: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ 메뉴 선택 오류: {e}")
            return None
    
    def submit_feedback(self, menu_name, category, feedback_type, score):
        """피드백 제출"""
        try:
            feedback_data = {
                "menu_name": menu_name,
                "category": category,
                "feedback_type": feedback_type,
                "score": score
            }
            response = self.session.post(
                f"{self.base_url}/api/recommend/feedback/instant",
                json=feedback_data
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 피드백 제출 실패: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ 피드백 제출 오류: {e}")
            return None
    
    def get_user_profile(self):
        """사용자 프로필 조회"""
        try:
            response = self.session.get(f"{self.base_url}/api/users/me")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 프로필 조회 실패: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ 프로필 조회 오류: {e}")
            return None
    
    def test_user_cycle(self, user_info, cycle_num):
        """사용자별 테스트 사이클"""
        username = user_info["username"]
        password = user_info["password"]
        
        print(f"\n🔄 {username} 사용자 {cycle_num}번째 테스트 시작")
        
        # 1. 로그인
        token, login_data = self.login(username, password)
        if not token:
            return None
        
        # 2. 프로필 조회
        profile = self.get_user_profile()
        if profile:
            profile_info = profile.get('profile', {})
            spicy_level = profile_info.get('spicy_threshold', 'N/A') if profile_info else 'N/A'
            print(f"   👤 프로필: {profile['nickname']} (맵기: {spicy_level})")
        
        # 3. 추천 받기
        recommendations = self.get_recommendations()
        if not recommendations or len(recommendations) == 0:
            return None
        
        print(f"   🎯 추천 받음: {len(recommendations)}개 메뉴")
        
        # 4. 첫 번째 메뉴 선택 및 피드백
        selected_menu = recommendations[0]
        menu_name = selected_menu["menu_name"]
        category = selected_menu["category"]
        match_rate = selected_menu["match_rate"]
        
        print(f"   🍽️ 선택: {menu_name} ({category}) - {match_rate}%")
        
        # 메뉴 선택
        select_result = self.select_menu(selected_menu["menu_id"])
        if select_result:
            print(f"   ✅ 선택 완료: {select_result['message']}")
        
        # 피드백 제출 (사용자 성향에 따른 피드백)
        feedback_type, feedback_score = self.get_feedback_by_user_type(username, menu_name, category)
        
        feedback_result = self.submit_feedback(menu_name, category, feedback_type, feedback_score)
        if feedback_result:
            print(f"   💬 피드백: {feedback_type} ({feedback_score}점)")
        
        # 결과 저장
        result = {
            "username": username,
            "cycle": cycle_num,
            "menu_name": menu_name,
            "category": category,
            "match_rate": match_rate,
            "feedback_type": feedback_type,
            "feedback_score": feedback_score,
            "description": selected_menu.get("description", ""),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.results.append(result)
        return result
    
    def get_feedback_by_user_type(self, username, menu_name, category):
        """사용자 타입에 따른 피드백 생성"""
        if username == "aaa":  # 매운맛 애호가
            if category in ["한식", "중식", "아시안"]:
                return "excellent", 4.8
            elif category in ["일식", "분식"]:
                return "neutral", 3.5
            else:
                return "good", 4.2
        elif username == "bbb":  # 건강식 애호가
            if category in ["샐러드", "디저트", "카페"]:
                return "excellent", 4.9
            elif category in ["한식", "중식"]:
                return "neutral", 3.2
            else:
                return "good", 4.0
        else:  # ccc 중용파
            if category in ["한식", "일식"]:
                return "good", 4.1
            elif category in ["중식", "아시안"]:
                return "neutral", 3.6
            else:
                return "good", 4.0
    
    def run_full_test(self):
        """전체 테스트 실행"""
        print("🚀 메뉴 추천 시스템 전체 테스트 시작")
        print(f"📊 테스트 사용자: {[user['username'] for user in TEST_USERS]}")
        print(f"🔄 사용자별 테스트 횟수: 5번")
        
        start_time = time.time()
        
        # 각 사용자별 5번 테스트
        for user_info in TEST_USERS:
            username = user_info["username"]
            print(f"\n👤 {username} 사용자 테스트 시작 ({user_info['nickname']})")
            
            for cycle in range(1, 6):  # 5번 테스트
                result = self.test_user_cycle(user_info, cycle)
                if result:
                    print(f"   ✅ {cycle}번째 테스트 완료")
                else:
                    print(f"   ❌ {cycle}번째 테스트 실패")
                
                # 잠시 대기 (서버 부하 방지)
                time.sleep(0.5)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n⏱️ 전체 테스트 완료 (소요 시간: {total_time:.2f}초)")
        self.analyze_results()
        self.save_results()
    
    def analyze_results(self):
        """결과 분석"""
        if not self.results:
            print("❌ 분석할 결과가 없습니다.")
            return
        
        print(f"\n📊 테스트 결과 분석 (총 {len(self.results)}건)")
        
        # 사용자별 결과
        user_results = {}
        for result in self.results:
            username = result["username"]
            if username not in user_results:
                user_results[username] = []
            user_results[username].append(result)
        
        print(f"\n👤 사용자별 결과:")
        for username, results in user_results.items():
            avg_match = sum(r["match_rate"] for r in results) / len(results)
            avg_score = sum(r["feedback_score"] for r in results) / len(results)
            categories = list(set(r["category"] for r in results))
            
            print(f"   {username}:")
            print(f"     테스트 횟수: {len(results)}")
            print(f"     평균 매칭률: {avg_match:.1f}%")
            print(f"     평균 피드백 점수: {avg_score:.2f}")
            print(f"     추천 카테고리: {', '.join(categories)}")
        
        # 카테고리별 분석
        category_count = {}
        for result in self.results:
            category = result["category"]
            category_count[category] = category_count.get(category, 0) + 1
        
        print(f"\n🍽️ 카테고리별 추천 횟수:")
        for category, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
            print(f"   {category}: {count}회")
        
        # 피드백 타입별 분석
        feedback_count = {}
        for result in self.results:
            feedback_type = result["feedback_type"]
            feedback_count[feedback_type] = feedback_count.get(feedback_type, 0) + 1
        
        print(f"\n💬 피드백 타입별 분석:")
        for feedback_type, count in sorted(feedback_count.items(), key=lambda x: x[1], reverse=True):
            print(f"   {feedback_type}: {count}회")
    
    def save_results(self):
        """결과 저장"""
        if not self.results:
            print("❌ 저장할 결과가 없습니다.")
            return
        
        # DataFrame으로 변환
        df = pd.DataFrame(self.results)
        
        # Excel 파일로 저장
        filename = f"recommendation_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 전체 결과
            df.to_excel(writer, sheet_name='전체 결과', index=False)
            
            # 사용자별 요약
            user_summary = df.groupby('username').agg({
                'match_rate': ['mean', 'std'],
                'feedback_score': ['mean', 'std'],
                'category': 'nunique',
                'menu_name': 'nunique'
            }).round(2)
            user_summary.columns = ['평균 매칭률', '매칭률 표준편차', '평균 피드백 점수', '피드백 점수 표준편차', '카테고리 수', '메뉴 수']
            user_summary.to_excel(writer, sheet_name='사용자별 요약')
            
            # 카테고리별 분석
            category_analysis = df.groupby('category').agg({
                'username': 'count',
                'match_rate': 'mean',
                'feedback_score': 'mean'
            }).round(2)
            category_analysis.columns = ['추천 횟수', '평균 매칭률', '평균 피드백 점수']
            category_analysis.to_excel(writer, sheet_name='카테고리별 분석')
            
            # 피드백 분석
            feedback_analysis = df.groupby('feedback_type').agg({
                'username': 'count',
                'match_rate': 'mean',
                'feedback_score': 'mean'
            }).round(2)
            feedback_analysis.columns = ['피드백 횟수', '평균 매칭률', '평균 피드백 점수']
            feedback_analysis.to_excel(writer, sheet_name='피드백 분석')
        
        print(f"\n💾 결과 저장 완료: {filename}")
        print(f"   📊 총 {len(self.results)}건의 테스트 결과")
        print(f"   📋 4개 시트로 구성된 상세 분석 보고서")

if __name__ == "__main__":
    # 테스트 실행
    tester = MenuRecommendationTester()
    tester.run_full_test()
