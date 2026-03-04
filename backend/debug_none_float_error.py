"""
NoneType과 float 비교 오류 디버깅
"""
import os
import sys
sys.path.append('.')

from app.database_mysql import SessionLocal
from app import models, crud
from app.core.weather_service import weather_service
from app.core.algorithm import calculate_recommendation_score, generate_recommendation_reason

def debug_none_float_error():
    """NoneType과 float 비교 오류 디버깅"""
    
    print("🔍 NoneType과 float 비교 오류 디버깅")
    print("=" * 50)
    
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
        menus = crud.get_menus(db, skip=1, limit=3)
        print(f"✅ 메뉴: {len(menus)}개")
        
        # 3. 날씨 데이터
        weather_data = weather_service.get_current_weather("Seoul")
        print(f"✅ 날씨: {weather_data}")
        
        # 4. 추천 점수 계산 디버깅
        print(f"\n🎯 추천 점수 계산 디버깅:")
        
        for i, menu in enumerate(menus[:3], 1):
            print(f"\n   {i}번째 메뉴: {menu.menu_name}")
            
            # 메뉴 상세 정보 확인
            if menu.details:
                print(f"      상세 정보: 존재")
                print(f"      매운맛: {menu.details.spicy_level}")
                print(f"      짠맛: {menu.details.saltiness_level}")
                print(f"      만족도: {menu.details.real_satisfaction_score}")
            else:
                print(f"      상세 정보: 없음")
            
            # 점수 계산 시도
            try:
                score = calculate_recommendation_score(
                    menu=menu,
                    user=user.profile,
                    daily_inquiry=None,
                    weather_data=weather_data,
                    history=None,
                    db=db
                )
                print(f"      점수 계산 성공: {score}")
                
            except Exception as e:
                print(f"      ❌ 점수 계산 실패: {e}")
                import traceback
                traceback.print_exc()
        
        # 5. 추천 이유 생성 디버깅
        print(f"\n📝 추천 이유 생성 디버깅:")
        
        if menus:
            menu = menus[0]
            try:
                reason = generate_recommendation_reason(menu, weather_data, user=user, db=db)
                print(f"   추천 이유: {reason}")
                
            except Exception as e:
                print(f"   ❌ 추천 이유 생성 실패: {e}")
                import traceback
                traceback.print_exc()
        
        print("\n✅ 디버깅 완료")
        
    except Exception as e:
        print(f"❌ 전체 디버깅 실패: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == "__main__":
    debug_none_float_error()
