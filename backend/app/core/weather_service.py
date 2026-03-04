import requests
import json
import datetime
import os
from typing import Dict, Optional

class WeatherService:
    """실시간 날씨 데이터 서비스"""
    
    def __init__(self):
        # 기상청 API 설정
        self.weather_url = os.getenv("KMA_WEATHER_URL", "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtFcst")
        self.auth_key = os.getenv("KMA_API_KEY", "kZsudkRgRWCbLnZEYMVg5Q")
        
        # 서울 좌표 (기본값)
        self.seoul_coords = {
            "nx": int(os.getenv("SEOUL_NX", 55)),
            "ny": int(os.getenv("SEOUL_NY", 127))
        }
        
        # 날씨 카테고리 매핑
        self.weather_categories = {
            "PTY": "강수 형태",  # 0: 없음, 1: 비, 2: 비/눈, 3: 눈, 4: 소나기
            "REH": "습도",      # %
            "RN1": "1시간 강수량",  # mm
            "T1H": "기온",      # 섭씨
            "UUU": "동서 바람",  # m/s
            "VEC": "풍향",      # deg
            "VVV": "남북 바람",  # m/s
            "WSD": "풍속"       # m/s
        }
    
    def get_current_weather(self, city: str = "Seoul") -> Dict:
        """
        실시간 날씨 정보 가져오기
        기상청 API 사용
        """
        try:
            # 기상청 API 호출
            weather_data = self._fetch_kma_weather()
            if weather_data:
                return weather_data
            else:
                # API 실패 시 시뮬레이션 데이터
                return self._simulate_weather_data(city)
        except Exception as e:
            print(f"⚠️ 날씨 데이터 가져오기 오류: {e}")
            return self._simulate_weather_data(city)
    
    def _fetch_kma_weather(self) -> Dict:
        """기상청 API 호출"""
        try:
            # 기상청 API 안전 시간 계산 (45분 이전)
            now = datetime.datetime.now()
            base_dt = now - datetime.timedelta(minutes=45)
            
            base_date = base_dt.strftime("%Y%m%d")
            base_time = base_dt.strftime("%H30")
            
            print(f"🌤️ 기상청 API 호출: {base_date} {base_time}")
            
            params = {
                "authKey": self.auth_key,
                "numOfRows": 1000,
                "pageNo": 1,
                "base_date": base_date,
                "base_time": base_time,
                "nx": self.seoul_coords["nx"],
                "ny": self.seoul_coords["ny"],
                "dataType": "JSON"
            }
            
            response = requests.get(self.weather_url, params=params, timeout=10)
            
            if response.status_code == 200:
                weather_dict = response.json()
                
                # 응답 안전 체크
                if weather_dict.get("response", {}).get("header", {}).get("resultCode") == "00":
                    return self._parse_kma_weather_data(weather_dict)
                else:
                    print(f"⚠️ 기상청 API 오류: {weather_dict.get('response', {}).get('header', {}).get('resultMsg', '알 수 없는 오류')}")
                    return None
            else:
                print(f"⚠️ 기상청 API 호출 실패: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"⚠️ 기상청 API 오류: {e}")
            return None
    
    def _parse_kma_weather_data(self, weather_dict: Dict) -> Dict:
        """기상청 API 데이터 파싱"""
        try:
            items = weather_dict["response"]["body"]["items"]["item"]
            
            # 날씨 카테고리별 데이터 수집
            weather_data = {}
            
            for item in items:
                category = item["category"]
                value = item["fcstValue"]
                fcst_time = item["fcstTime"]
                
                if category not in weather_data:
                    weather_data[category] = []
                
                weather_data[category].append({
                    "time": fcst_time,
                    "value": value
                })
            
            # 현재 시간 기준으로 가장 가까운 데이터 선택
            current_time = datetime.datetime.now().strftime("%H%M")
            
            def get_current_value(category):
                if category not in weather_data:
                    return None
                
                # 가장 가까운 시간대 데이터 찾기
                closest_item = min(weather_data[category], 
                                key=lambda x: abs(int(x["time"]) - int(current_time)))
                value = closest_item["value"]
                
                # 숫자 값 처리
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return value
            
            # 주요 날씨 정보 추출
            temp = get_current_value("T1H") or 20.0
            humidity = get_current_value("REH") or 50
            precipitation = get_current_value("RN1") or 0.0
            wind_speed = get_current_value("WSD") or 0.0
            precipitation_type = get_current_value("PTY") or 0
            
            # 날씨 상태 판단
            weather = "Clear"
            if str(precipitation_type) in ["1", "4"]:  # 비, 소나기
                weather = "Rain"
            elif str(precipitation_type) == "2":  # 비/눈
                weather = "Rain"
            elif str(precipitation_type) == "3":  # 눈
                weather = "Snow"
            elif float(precipitation) > 0.1:  # 강수량 있음
                weather = "Rain"
            
            # 상세 날씨 정보
            weather_details = {
                "city": "Seoul",
                "weather": weather,
                "temp": temp,
                "temp_min": temp - 2,
                "temp_max": temp + 2,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "precipitation": precipitation,
                "precipitation_type": precipitation_type,
                "description": self._get_weather_description(weather, temp),
                "season": self._get_season_from_temp(temp),
                "is_cold": temp < 10,
                "is_hot": temp > 28,
                "is_rainy": weather in ["Rain", "Drizzle", "Thunderstorm"],
                "is_snowy": weather == "Snow",
                "is_clear": weather == "Clear",
                "is_cloudy": weather == "Clouds",
                "api_source": "KMA",
                "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"🌤️ {weather_details['city']} 날씨: {weather} {temp}°C (습도: {humidity}%)")
            return weather_details
            
        except Exception as e:
            print(f"⚠️ 기상청 데이터 파싱 오류: {e}")
            return None
    
    def _simulate_weather_data(self, city: str) -> Dict:
        """시뮬레이션 날씨 데이터 (테스트용)"""
        import random
        from datetime import datetime
        
        # 계절별 날씨 패턴
        month = datetime.now().month
        weather_patterns = {
            "spring": ["Clear", "Clouds", "Rain"],  # 3-5월
            "summer": ["Clear", "Rain", "Thunderstorm"],  # 6-8월
            "autumn": ["Clear", "Clouds", "Rain"],  # 9-11월
            "winter": ["Clear", "Clouds", "Snow"]  # 12-2월
        }
        
        if month in [3, 4, 5]:
            season = "spring"
            temp_range = (15, 25)
        elif month in [6, 7, 8]:
            season = "summer"
            temp_range = (25, 35)
        elif month in [9, 10, 11]:
            season = "autumn"
            temp_range = (10, 20)
        else:
            season = "winter"
            temp_range = (-5, 10)
        
        weather = random.choice(weather_patterns[season])
        temp = random.randint(*temp_range)
        humidity = random.randint(40, 80)
        wind_speed = random.uniform(0.5, 5.0)
        
        # 날씨 상세 정보
        weather_details = {
            "city": city,
            "weather": weather,
            "temp": temp,
            "temp_min": temp - random.randint(2, 5),
            "temp_max": temp + random.randint(2, 5),
            "humidity": humidity,
            "wind_speed": wind_speed,
            "description": self._get_weather_description(weather, temp),
            "season": season,
            "is_cold": temp < 10,
            "is_hot": temp > 28,
            "is_rainy": weather in ["Rain", "Drizzle", "Thunderstorm"],
            "is_snowy": weather in ["Snow"],
            "is_clear": weather == "Clear",
            "is_cloudy": weather == "Clouds"
        }
        
        print(f"🌤️ {city} 날씨: {weather} {temp}°C ({weather_details['description']})")
        return weather_details
    
    def _parse_weather_data(self, data: Dict) -> Dict:
        """OpenWeatherMap API 데이터 파싱"""
        weather = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        return {
            "city": data["name"],
            "weather": weather,
            "temp": temp,
            "temp_min": temp_min,
            "temp_max": temp_max,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "description": data["weather"][0]["description"],
            "season": self._get_season_from_temp(temp),
            "is_cold": temp < 10,
            "is_hot": temp > 28,
            "is_rainy": weather in ["Rain", "Drizzle", "Thunderstorm"],
            "is_snowy": weather in ["Snow"],
            "is_clear": weather == "Clear",
            "is_cloudy": weather == "Clouds"
        }
    
    def _get_weather_description(self, weather: str, temp: float) -> str:
        """날씨 상세 설명"""
        descriptions = {
            "Clear": "맑음",
            "Clouds": "흐림",
            "Rain": "비",
            "Drizzle": "이슬비",
            "Thunderstorm": "뇌우",
            "Snow": "눈",
            "Mist": "안개",
            "Fog": "짙은 안개"
        }
        
        base_desc = descriptions.get(weather, weather)
        
        # 온도에 따른 추가 설명
        if temp < 0:
            return f"{base_desc} (매우 추움)"
        elif temp < 10:
            return f"{base_desc} (추움)"
        elif temp < 20:
            return f"{base_desc} (선선함)"
        elif temp < 28:
            return f"{base_desc} (따뜻함)"
        else:
            return f"{base_desc} (더움)"
    
    def _get_season_from_temp(self, temp: float) -> str:
        """온도로 계절 판단"""
        if temp < 10:
            return "winter"
        elif temp < 20:
            return "spring"
        elif temp < 28:
            return "autumn"
        else:
            return "summer"
    
    def get_weather_recommendations(self, weather_data: Dict) -> Dict:
        """날씨 기반 추천 가이드"""
        recommendations = {
            "hot_weather": [],
            "cold_weather": [],
            "rainy_weather": [],
            "snowy_weather": [],
            "clear_weather": []
        }
        
        weather = weather_data["weather"]
        temp = weather_data["temp"]
        
        # 더운 날씨 추천
        if temp > 28:
            recommendations["hot_weather"] = [
                "시원한 면 요리 (냉면, 국수)",
                "가벼운 샐러드",
                "차가운 음료",
                "매운맛이 적은 메뉴"
            ]
        
        # 추운 날씨 추천
        if temp < 10:
            recommendations["cold_weather"] = [
                "따끈한 국물 요리",
                "매운 음식",
                "고칼로리 메뉴",
                "뜨거운 음료"
            ]
        
        # 비 오는 날 추천
        if weather in ["Rain", "Drizzle", "Thunderstorm"]:
            recommendations["rainy_weather"] = [
                "국물이 있는 음식",
                "따끈한 요리",
                "집에서 먹기 좋은 음식",
                "바삭한 튀김류"
            ]
        
        # 눈 오는 날 추천
        if weather == "Snow":
            recommendations["snowy_weather"] = [
                "뜨끈한 국물 요리",
                "매운 음식",
                "고기 요리",
                "따뜻한 음료"
            ]
        
        # 맑은 날 추천
        if weather == "Clear":
            recommendations["clear_weather"] = [
                "신선한 샐러드",
                "가벼운 요리",
                "야외 음식",
                "상쾌한 음료"
            ]
        
        return recommendations

# 전역 인스턴스
weather_service = WeatherService()
