"""
날씨 서비스 - 기상청 API 오류 수정 버전
"""
import os
import requests
import json
import datetime
from typing import Dict, Optional

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("KMA_API_KEY")
        self.weather_url = os.getenv("KMA_WEATHER_URL")
        self.seoul_nx = os.getenv("SEOUL_NX", "60")
        self.seoul_ny = os.getenv("SEOUL_NY", "127")
    
    def get_current_weather(self, city: str = "Seoul") -> Dict:
        """실시간 날씨 정보 가져오기"""
        try:
            # API 키가 없으면 시뮬레이션 데이터
            if not self.api_key:
                print("⚠️ 기상청 API 키 없음 - 시뮬레이션 데이터 사용")
                return self._simulate_weather_data(city)
            
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
    
    def _fetch_kma_weather(self) -> Optional[Dict]:
        """기상청 API 호출 - 오류 처리 강화"""
        try:
            # 기상청 API 안전 시간 계산 (45분 이전)
            now = datetime.datetime.now()
            base_dt = now - datetime.timedelta(minutes=45)
            
            base_date = base_dt.strftime("%Y%m%d")
            base_time = base_dt.strftime("%H30")
            
            print(f"🌤️ 기상청 API 호출: {base_date} {base_time}")
            
            # API 요청
            params = {
                "serviceKey": self.api_key,
                "numOfRows": "10",
                "pageNo": "1",
                "dataType": "JSON",
                "base_date": base_date,
                "base_time": base_time,
                "nx": self.seoul_nx,
                "ny": self.seoul_ny
            }
            
            response = requests.get(self.weather_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # 응답 데이터 파싱
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            
            if not items:
                print("⚠️ 기상청 데이터 없음")
                return None
            
            # 날씨 정보 추출
            weather_info = {}
            for item in items:
                category = item.get("category")
                value = item.get("obsrValue")
                
                if category == "T1H":  # 기온
                    weather_info["temperature"] = float(value)
                elif category == "PTY":  # 강수 형태
                    # 강수 형태: 0(없음), 1(비), 2(비/눈), 3(눈), 4(소나기)
                    weather_info["precipitation_type"] = value
                elif category == "REH":  # 습도
                    weather_info["humidity"] = float(value)
                elif category == "WSD":  # 풍속
                    weather_info["wind_speed"] = float(value)
            
            # 날씨 상태 결정
            if weather_info:
                return self._parse_weather_info(weather_info)
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️ 기상청 API 요청 오류: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"⚠️ 기상청 JSON 파싱 오류: {e}")
            return None
        except ValueError as e:
            print(f"⚠️ 기상청 데이터 파싱 오류: {e}")
            return None
        except Exception as e:
            print(f"⚠️ 기상청 API 오류: {e}")
            return None
    
    def _parse_weather_info(self, weather_info: Dict) -> Dict:
        """날씨 정보 파싱"""
        try:
            temperature = weather_info.get("temperature", 20.0)
            precipitation_type = weather_info.get("precipitation_type", "0")
            humidity = weather_info.get("humidity", 50.0)
            wind_speed = weather_info.get("wind_speed", 2.0)
            
            # 날씨 상태 결정
            if precipitation_type == "0":
                weather_condition = "Clear"
                is_rainy = False
                weather_desc = "맑음"
            elif precipitation_type in ["1", "2", "4"]:
                weather_condition = "Rain"
                is_rainy = True
                weather_desc = "비"
            elif precipitation_type == "3":
                weather_condition = "Snow"
                is_rainy = False
                weather_desc = "눈"
            else:
                weather_condition = "Clear"
                is_rainy = False
                weather_desc = "맑음"
            
            # 온도 상태
            if temperature >= 25:
                temp_desc = "더움"
            elif temperature <= 10:
                temp_desc = "추움"
            else:
                temp_desc = "적당함"
            
            return {
                "temperature": temperature,
                "weather_condition": weather_condition,
                "weather_description": weather_desc,
                "is_rainy": is_rainy,
                "is_cold": temperature <= 10,
                "is_hot": temperature >= 25,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "temperature_description": temp_desc,
                "full_description": f"{weather_desc} ({temp_desc})"
            }
            
        except Exception as e:
            print(f"⚠️ 날씨 정보 파싱 오류: {e}")
            return None
    
    def _simulate_weather_data(self, city: str) -> Dict:
        """시뮬레이션 날씨 데이터"""
        import random
        
        # 랜덤 날씨 생성
        conditions = ["Clear", "Cloudy", "Rain"]
        weather_condition = random.choice(conditions)
        temperature = random.uniform(15, 25)
        
        is_rainy = weather_condition == "Rain"
        is_cold = temperature <= 10
        is_hot = temperature >= 25
        
        if temperature >= 25:
            temp_desc = "더움"
        elif temperature <= 10:
            temp_desc = "추움"
        else:
            temp_desc = "적당함"
        
        weather_desc = {
            "Clear": "맑음",
            "Cloudy": "흐림", 
            "Rain": "비"
        }.get(weather_condition, "맑음")
        
        return {
            "temperature": temperature,
            "weather_condition": weather_condition,
            "weather_description": weather_desc,
            "is_rainy": is_rainy,
            "is_cold": is_cold,
            "is_hot": is_hot,
            "humidity": random.uniform(40, 80),
            "wind_speed": random.uniform(1, 5),
            "temperature_description": temp_desc,
            "full_description": f"{weather_desc} ({temp_desc})"
        }

# 전역 인스턴스
weather_service = WeatherService()
