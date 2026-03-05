from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict

from ...database_mysql import get_db
from ...core.weather_service import weather_service

router = APIRouter()

@router.get("/seoul")
def get_seoul_weather() -> Dict:
    """
    서울 날씨 정보 가져오기
    """
    try:
        weather_data = weather_service.get_current_weather("Seoul")
        
        if weather_data:
            return {
                "city": "Seoul",
                "temperature": weather_data.get("temperature", 20.0),
                "weather_condition": weather_data.get("weather_condition", "Clear"),
                "weather_description": weather_data.get("weather_description", "맑음"),
                "is_rainy": weather_data.get("is_rainy", False),
                "is_cold": weather_data.get("is_cold", False),
                "is_hot": weather_data.get("is_hot", False),
                "humidity": weather_data.get("humidity", 50.0),
                "wind_speed": weather_data.get("wind_speed", 2.0),
                "full_description": weather_data.get("full_description", "맑음 (적당함)")
            }
        else:
            return {
                "city": "Seoul",
                "temperature": 20.0,
                "weather_condition": "Clear",
                "weather_description": "맑음",
                "is_rainy": False,
                "is_cold": False,
                "is_hot": False,
                "humidity": 50.0,
                "wind_speed": 2.0,
                "full_description": "맑음 (적당함)",
                "message": "날씨 API를 사용할 수 없어 기본값을 반환합니다."
            }
            
    except Exception as e:
        print(f"⚠️ 날씨 정보 오류: {e}")
        return {
            "city": "Seoul",
            "temperature": 20.0,
            "weather_condition": "Clear",
            "weather_description": "맑음",
            "is_rainy": False,
            "is_cold": False,
            "is_hot": False,
            "humidity": 50.0,
            "wind_speed": 2.0,
            "full_description": "맑음 (적당함)",
            "message": "날씨 정보를 가져오는 중 오류가 발생했습니다."
        }

@router.get("/{city}")
def get_city_weather(city: str) -> Dict:
    """
    특정 도시 날씨 정보 가져오기
    """
    try:
        weather_data = weather_service.get_current_weather(city)
        
        if weather_data:
            return {
                "city": city,
                "temperature": weather_data.get("temperature", 20.0),
                "weather_condition": weather_data.get("weather_condition", "Clear"),
                "weather_description": weather_data.get("weather_description", "맑음"),
                "is_rainy": weather_data.get("is_rainy", False),
                "is_cold": weather_data.get("is_cold", False),
                "is_hot": weather_data.get("is_hot", False),
                "humidity": weather_data.get("humidity", 50.0),
                "wind_speed": weather_data.get("wind_speed", 2.0),
                "full_description": weather_data.get("full_description", "맑음 (적당함)")
            }
        else:
            return {
                "city": city,
                "temperature": 20.0,
                "weather_condition": "Clear",
                "weather_description": "맑음",
                "is_rainy": False,
                "is_cold": False,
                "is_hot": False,
                "humidity": 50.0,
                "wind_speed": 2.0,
                "full_description": "맑음 (적당함)",
                "message": "날씨 API를 사용할 수 없어 기본값을 반환합니다."
            }
            
    except Exception as e:
        print(f"⚠️ 날씨 정보 오류: {e}")
        return {
            "city": city,
            "temperature": 20.0,
            "weather_condition": "Clear",
            "weather_description": "맑음",
            "is_rainy": False,
            "is_cold": False,
            "is_hot": False,
            "humidity": 50.0,
            "wind_speed": 2.0,
            "full_description": "맑음 (적당함)",
            "message": "날씨 정보를 가져오는 중 오류가 발생했습니다."
        }
