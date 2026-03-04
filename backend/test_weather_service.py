"""
날씨 서비스 테스트
"""
import os
import sys
sys.path.append('.')

from app.core.weather_service import weather_service

def test_weather_service():
    """날씨 서비스 테스트"""
    
    print("🌤️ 날씨 서비스 테스트")
    print("=" * 40)
    
    # 환경변수 확인
    print("환경변수 확인:")
    print(f"  KMA_API_KEY: {os.getenv('KMA_API_KEY', '설정 안됨')}")
    print(f"  KMA_WEATHER_URL: {os.getenv('KMA_WEATHER_URL', '설정 안됨')}")
    print(f"  SEOUL_NX: {os.getenv('SEOUL_NX', '설정 안됨')}")
    print(f"  SEOUL_NY: {os.getenv('SEOUL_NY', '설정 안됨')}")
    
    print("\n날씨 데이터 가져오기 시도:")
    
    try:
        weather_data = weather_service.get_current_weather("Seoul")
        print(f"✅ 성공: {weather_data}")
        
        # 날씨 데이터 구조 확인
        if isinstance(weather_data, dict):
            print(f"   데이터 타입: dict")
            print(f"   키 목록: {list(weather_data.keys())}")
            
            # 주요 필드 확인
            if 'temperature' in weather_data:
                print(f"   온도: {weather_data['temperature']}")
            if 'weather_condition' in weather_data:
                print(f"   날씨: {weather_data['weather_condition']}")
            if 'humidity' in weather_data:
                print(f"   습도: {weather_data['humidity']}")
                
        else:
            print(f"   데이터 타입: {type(weather_data)}")
            
    except Exception as e:
        print(f"❌ 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_weather_service()
