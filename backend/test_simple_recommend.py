"""
간단한 추천 테스트 - 로컬에서 직접 테스트
"""
import os
import sys
sys.path.append('.')

from app.database_mysql import SessionLocal
from app import models, crud
from app.core.weather_service import weather_service
from app.core.algorithm import calculate_recommendation_score, generate_recommendation_reason

def test_simple_recommend():
    """간단한 추천 테스트"""
    
    print("🎯 간단한 추천 테스트")
    print("=" * 40)
    
    # DB 연결
    db = SessionLocal()
    
    try:
        # 1. 사용자 확인
        user = crud.get_user_by_username(db, username="aaa")
        if not user or not user.profile:
            print("❌ 사용자 또는 프로필 없음")
            return
        
        print(f"✅ 사용자: {user.username}")
        print(f"   프로필: 예산 {user.profile.lunch_budget_max}원, 맵기 {user.profile.spicy_threshold}")
        
        # 2. 메뉴 조회
        menus = crud.get_menus(db, skip=1, limit=5)
        print(f"✅ 메뉴: {len(menus)}개")
        
        # 3. 날씨 데이터
        weather_data = weather_service.get_current_weather("Seoul")
        print(f"✅ 날씨: {weather_data.get('weather', 'N/A')} {weather_data.get('temp', 'N/A')}°C")
        
        # 4. 추천 점수 계산
        scored_items = []
        for menu in menus:
            try:
                score = calculate_recommendation_score(
                    menu=menu,
                    user=user.profile,
                    daily_inquiry=None,
                    weather_data=weather_data,
                    history=None,
                    db=db
                )
                scored_items.append((score, menu))
                print(f"   {menu.menu_name}: {score:.2f}점")
                
            except Exception as e:
                print(f"   ❌ {menu.menu_name}: 점수 계산 실패 - {e}")
        
        # 5. 정렬
        scored_items.sort(key=lambda x: x[0], reverse=True)
        print(f"\n🎯 추천 결과:")
        for i, (score, menu) in enumerate(scored_items[:3], 1):
            print(f"   {i}위: {menu.menu_name} ({score:.2f}점)")
        
        # 6. 추천 이유 생성 테스트
        if scored_items:
            menu = scored_items[0][1]
            try:
                reason = generate_recommendation_reason(menu, weather_data, user=user, db=db)
                print(f"\n📝 추천 이유: {reason}")
            except Exception as e:
                print(f"❌ 추천 이유 생성 실패: {e}")
        
        print("\n✅ 로컬 테스트 완료")
        
    except Exception as e:
        print(f"❌ 전체 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == "__main__":
    test_simple_recommend()
