"""
간단한 추천 시스템 테스트
"""
import os
import sys
sys.path.append('.')

from app.database_mysql import SessionLocal
from app import models, crud
from app.core.weather_service import weather_service

def test_recommendation_simple():
    """간단한 추천 시스템 테스트"""
    
    print("🎯 간단한 추천 시스템 테스트")
    print("=" * 50)
    
    # 1. DB 연결
    try:
        db = SessionLocal()
        print("✅ DB 연결 성공")
    except Exception as e:
        print(f"❌ DB 연결 실패: {e}")
        return
    
    # 2. 사용자 확인
    try:
        user = crud.get_user_by_username(db, username="aaa")
        if user:
            print(f"✅ 사용자 확인: {user.username}")
            
            # 사용자 프로필 확인
            if hasattr(user, 'profile') and user.profile:
                print(f"   프로필: 예산 {user.profile.lunch_budget_max}원, 맵기 {user.profile.spicy_threshold}")
            else:
                print("   ⚠️ 프로필 없음")
        else:
            print("❌ 사용자 없음")
            return
            
    except Exception as e:
        print(f"❌ 사용자 확인 실패: {e}")
        return
    
    # 3. 메뉴 조회
    try:
        menus = crud.get_menus(db, skip=1, limit=5)
        print(f"✅ 메뉴 조회 성공: {len(menus)}개")
        
        if len(menus) > 0:
            print(f"   첫 메뉴: {menus[0].menu_name} ({menus[0].category})")
            
    except Exception as e:
        print(f"❌ 메뉴 조회 실패: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. 날씨 데이터
    try:
        weather_data = weather_service.get_current_weather("Seoul")
        print(f"✅ 날씨 데이터: {weather_data.get('weather', 'N/A')} {weather_data.get('temp', 'N/A')}°C")
        
    except Exception as e:
        print(f"❌ 날씨 데이터 실패: {e}")
        return
    
    # 5. 추천 알고리즘 테스트
    try:
        from app.core.algorithm import calculate_recommendation_score, generate_recommendation_reason
        
        if user.profile and len(menus) > 0:
            menu = menus[0]
            
            # 점수 계산
            score = calculate_recommendation_score(
                menu=menu,
                user=user.profile,
                daily_inquiry=None,
                weather_data=weather_data,
                history=None,
                db=db
            )
            print(f"✅ 추천 점수 계산: {score:.2f}")
            
            # 추천 이유 생성
            reason = generate_recommendation_reason(menu, weather_data, user=user, db=db)
            print(f"✅ 추천 이유: {reason}")
            
    except Exception as e:
        print(f"❌ 추천 알고리즘 실패: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 6. 전체 추천 로직 시뮬레이션
    try:
        # 모든 메뉴 조회
        all_menus = crud.get_menus(db, skip=1, limit=20)
        print(f"\n🎯 전체 추천 로직 시뮬레이션 ({len(all_menus)}개 메뉴):")
        
        scored_items = []
        for menu in all_menus:
            score = calculate_recommendation_score(
                menu=menu,
                user=user.profile,
                daily_inquiry=None,
                weather_data=weather_data,
                history=None,
                db=db
            )
            if score >= 0:
                scored_items.append((score, menu))
        
        # 정렬
        scored_items.sort(key=lambda x: x[0], reverse=True)
        
        print(f"   점수 계산된 메뉴: {len(scored_items)}개")
        
        if len(scored_items) > 0:
            print("   상위 3개 추천:")
            for i, (score, menu) in enumerate(scored_items[:3], 1):
                print(f"   {i}위: {menu.menu_name} ({score:.2f}점)")
        
        print("✅ 전체 추천 로직 성공")
        
    except Exception as e:
        print(f"❌ 전체 추천 로직 실패: {e}")
        import traceback
        traceback.print_exc()
        return
    
    finally:
        db.close()
        print("\n✅ 테스트 완료")

if __name__ == "__main__":
    test_recommendation_simple()
