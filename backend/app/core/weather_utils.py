"""
날씨 데이터 표준화 및 유틸리티 함수
"""
from typing import Dict, List, Optional
from enum import Enum

class WeatherType(Enum):
    """표준 날씨 타입"""
    CLEAR = "Clear"
    CLOUDS = "Clouds"
    RAIN = "Rain"
    SNOW = "Snow"
    THUNDERSTORM = "Thunderstorm"
    DRIZZLE = "Drizzle"
    MIST = "Mist"
    FOG = "Fog"

class WeatherMatcher:
    """날씨-메뉴 매칭 유틸리티"""
    
    # 날씨 키워드 매핑
    WEATHER_KEYWORDS = {
        WeatherType.CLEAR: ["맑음", "clear", "sunny", "화창", "晴天"],
        WeatherType.CLOUDS: ["흐림", "cloudy", "구름", "多云", "曇り"],
        WeatherType.RAIN: ["비", "rain", "비옴", "雨", "降雨", "강수"],
        WeatherType.SNOW: ["눈", "snow", "눈옴", "雪", "降雪"],
        WeatherType.THUNDERSTORM: ["뇌우", "thunderstorm", "천둥", "雷", "雷雨"],
        WeatherType.DRIZZLE: ["이슬비", "drizzle", "가랑비", "小雨"],
        WeatherType.MIST: ["안개", "mist", "薄雾"],
        WeatherType.FOG: ["짙은안개", "fog", "濃霧"]
    }
    
    # 날씨별 추천 메뉴 카테고리
    WEATHER_MENU_CATEGORIES = {
        WeatherType.CLEAR: ["샐러드", "냉면", "국수", "가벼운요리", "야외음식"],
        WeatherType.CLOUDS: ["한식", "중식", "양식", "일식"],  # 모든 메뉴 가능
        WeatherType.RAIN: ["국물요리", "찌개", "탕", "국밥", "따뜻한요리"],
        WeatherType.SNOW: ["국물요리", "찌개", "탕", "매운요리", "따뜻한요리"],
        WeatherType.THUNDERSTORM: ["국물요리", "집밥", "간편식"],
        WeatherType.DRIZZLE: ["국물요리", "따뜻한요리"],
        WeatherType.MIST: ["따뜻한요리", "차"],
        WeatherType.FOG: ["따뜻한요리", "국물요리"]
    }
    
    @staticmethod
    def normalize_weather_string(weather_str: str) -> WeatherType:
        """
        다양한 날씨 문자열을 표준 WeatherType으로 변환
        """
        if not weather_str:
            return WeatherType.CLEAR
        
        weather_str = weather_str.strip().lower()
        
        # 직접 매칭
        for weather_type in WeatherType:
            if weather_type.value.lower() in weather_str:
                return weather_type
        
        # 키워드 매칭
        for weather_type, keywords in WeatherMatcher.WEATHER_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in weather_str:
                    return weather_type
        
        # 기본값
        return WeatherType.CLEAR
    
    @staticmethod
    def get_weather_score_bonus(menu_category: str, weather_type: WeatherType) -> float:
        """
        메뉴 카테고리와 날씨에 따른 보너스 점수 계산
        """
        preferred_categories = WeatherMatcher.WEATHER_MENU_CATEGORIES.get(weather_type, [])
        
        # 완전 일치
        if any(cat in menu_category for cat in preferred_categories):
            return 15.0
        
        # 부분 일치
        for preferred_cat in preferred_categories:
            if preferred_cat in menu_category or menu_category in preferred_cat:
                return 8.0
        
        return 0.0
    
    @staticmethod
    def parse_weather_data(weather_data: Dict) -> Dict:
        """
        기상청 API 데이터를 표준화된 형식으로 변환
        """
        if not weather_data:
            return {
                "weather_type": WeatherType.CLEAR,
                "weather": WeatherType.CLEAR.value,
                "temp": 20.0,
                "is_rainy": False,
                "is_snowy": False,
                "is_hot": False,
                "is_cold": False,
                "is_clear": True,
                "humidity": 50.0
            }
        
        # 날씨 타입 표준화
        raw_weather = weather_data.get("weather", "Clear")
        weather_type = WeatherMatcher.normalize_weather_string(raw_weather)
        
        temp = float(weather_data.get("temp", 20.0))
        humidity = float(weather_data.get("humidity", 50.0))
        
        return {
            "weather_type": weather_type,
            "weather": weather_type.value,
            "temp": temp,
            "is_rainy": weather_type in [WeatherType.RAIN, WeatherType.DRIZZLE, WeatherType.THUNDERSTORM],
            "is_snowy": weather_type == WeatherType.SNOW,
            "is_hot": temp > 28,
            "is_cold": temp < 10,
            "is_clear": weather_type == WeatherType.CLEAR,
            "humidity": humidity,
            "description": weather_data.get("description", "")
        }
    
    @staticmethod
    def check_menu_weather_match(menu_matching_weather: str, current_weather: WeatherType) -> bool:
        """
        메뉴의 matching_weather 필드와 현재 날씨 매칭 확인
        """
        if not menu_matching_weather:
            return True  # 매칭 정보 없으면 모든 날씨에 가능
        
        menu_weather_type = WeatherMatcher.normalize_weather_string(menu_matching_weather)
        
        # 완전 일치
        if menu_weather_type == current_weather:
            return True
        
        # 유사 날씨 그룹 매칭
        weather_groups = {
            "rainy": [WeatherType.RAIN, WeatherType.DRIZZLE, WeatherType.THUNDERSTORM],
            "cold": [WeatherType.SNOW, WeatherType.CLEAR],  # 맑은 날도 추울 수 있음
            "cloudy": [WeatherType.CLOUDS, WeatherType.MIST, WeatherType.FOG]
        }
        
        for group, weather_types in weather_groups.items():
            if current_weather in weather_types and menu_weather_type in weather_types:
                return True
        
        return False
