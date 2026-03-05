#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render 배포 환경 API 테스트 스크립트
"""
import requests
import json

BASE_URL = "https://menu-recommand-app.onrender.com"

def test_server():
    """서버 상태 확인"""
    print("\n=== 1. 서버 상태 확인 ===")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=30)
        if response.status_code == 200:
            print(f"✅ 서버 응답: {response.json()['message']}")
            return True
        else:
            print(f"❌ 서버 응답 실패: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 서버 연결 에러: {e}")
        return False

def test_signup():
    """회원가입 테스트"""
    print("\n=== 2. 회원가입 테스트 ===")
    signup_data = {
        "username": "produser",
        "password": "prod1234",
        "email": "prod@example.com",
        "nickname": "프로덕션유저",
        "dietary_label": "none",
        "allergies": None,
        "spicy_threshold": 3,
        "saltiness_preference": 3,
        "lunch_budget_max": 12000,
        "is_adventurous": True
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/signup",
            json=signup_data,
            timeout=30
        )
        if response.status_code == 201:
            data = response.json()
            print(f"✅ 회원가입 성공!")
            print(f"   사용자 ID: {data.get('user_id')}")
            print(f"   사용자명: {data.get('username')}")
            return True
        else:
            error = response.json()
            if "already exists" in str(error) or "이미 존재" in str(error):
                print(f"⚠️  이미 존재하는 사용자입니다. 로그인 테스트를 진행합니다.")
                return True
            else:
                print(f"❌ 회원가입 실패: {error}")
                return False
    except Exception as e:
        print(f"❌ 회원가입 에러: {e}")
        return False

def test_login():
    """로그인 테스트"""
    print("\n=== 3. 로그인 테스트 ===")
    login_data = {
        "username": "produser",
        "password": "prod1234"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data=login_data,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"✅ 로그인 성공!")
            print(f"   액세스 토큰: {token[:50]}...")
            return token
        else:
            print(f"❌ 로그인 실패: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ 로그인 에러: {e}")
        return None

def test_menus():
    """메뉴 조회 및 날씨 데이터 확인"""
    print("\n=== 4. 메뉴 조회 및 날씨 데이터 확인 ===")
    try:
        response = requests.get(f"{BASE_URL}/api/menus?limit=10", timeout=30)
        if response.status_code == 200:
            menus = response.json()
            print(f"✅ 메뉴 조회 성공! 총 {len(menus)}개 메뉴 조회됨")
            
            # 날씨 데이터 확인
            weather_count = 0
            for menu in menus:
                weather = menu.get('matching_weather')
                if weather:
                    weather_count += 1
                print(f"   - {menu['menu_name']} (카테고리: {menu['category']}, 가격: {menu['price']}원, 날씨: {weather or 'N/A'})")
            
            print(f"\n   📊 날씨 데이터 통계: {weather_count}/{len(menus)} 메뉴에 날씨 정보 있음")
            return weather_count > 0
        else:
            print(f"❌ 메뉴 조회 실패: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ 메뉴 조회 에러: {e}")
        return False

def test_recommendation(token):
    """메뉴 추천 테스트"""
    print("\n=== 5. 메뉴 추천 알고리즘 테스트 ===")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    recommend_data = {
        "weather": "Rain",
        "mood": "Comfortable",
        "group_size": 2,
        "budget": 15000
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/recommend/",
            headers=headers,
            json=recommend_data,
            timeout=60
        )
        if response.status_code == 200:
            recommendations = response.json()
            if isinstance(recommendations, list):
                print(f"✅ 메뉴 추천 성공! 총 {len(recommendations)}개 추천됨")
                for i, rec in enumerate(recommendations[:5], 1):
                    print(f"   {i}. {rec.get('menu_name', 'N/A')} (점수: {rec.get('score', 'N/A')}, 이유: {rec.get('reason', 'N/A')})")
            else:
                print(f"✅ 메뉴 추천 성공!")
                print(f"   응답: {recommendations}")
            return True
        else:
            print(f"❌ 메뉴 추천 실패: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ 메뉴 추천 에러: {e}")
        return False

def test_user_profile(token):
    """사용자 프로필 조회 테스트"""
    print("\n=== 6. 사용자 프로필 조회 테스트 ===")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/users/me",
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ 프로필 조회 성공!")
            print(f"   사용자명: {profile.get('username')}")
            print(f"   이메일: {profile.get('email')}")
            print(f"   닉네임: {profile.get('nickname')}")
            return True
        else:
            print(f"❌ 프로필 조회 실패: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ 프로필 조회 에러: {e}")
        return False

def main():
    """전체 테스트 실행"""
    print("=" * 60)
    print("🚀 Render 배포 환경 API 전체 기능 테스트")
    print(f"🌐 URL: {BASE_URL}")
    print("=" * 60)
    
    results = {}
    
    # 1. 서버 상태 확인
    results['server'] = test_server()
    
    if not results['server']:
        print("\n❌ 서버 연결 실패. 테스트를 중단합니다.")
        return
    
    # 2. 회원가입
    results['signup'] = test_signup()
    
    # 3. 로그인
    token = test_login()
    results['login'] = token is not None
    
    if not token:
        print("\n❌ 로그인 실패로 이후 테스트를 진행할 수 없습니다.")
        return
    
    # 4. 메뉴 조회 및 날씨 데이터 확인
    results['menus_weather'] = test_menus()
    
    # 5. 메뉴 추천
    results['recommendation'] = test_recommendation(token)
    
    # 6. 사용자 프로필
    results['profile'] = test_user_profile(token)
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 Render 배포 환경 테스트 결과 요약")
    print("=" * 60)
    for test_name, result in results.items():
        status = "✅ 성공" if result else "❌ 실패"
        print(f"{test_name:20s}: {status}")
    
    # 전체 성공 여부
    all_success = all(results.values())
    print("\n" + "=" * 60)
    if all_success:
        print("🎉 모든 테스트 성공! 배포 환경이 정상 작동합니다.")
    else:
        print("⚠️  일부 테스트 실패. 위 결과를 확인하세요.")
    print("=" * 60)
    
    print("\n" + "=" * 60)
    print("🔑 프로덕션 테스트 계정 정보")
    print("=" * 60)
    print("아이디: produser")
    print("비밀번호: prod1234")
    print("=" * 60)

if __name__ == "__main__":
    main()
