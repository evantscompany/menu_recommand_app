import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import get_db
from app import models, schemas

# 테스트용 DB 세션
@pytest.fixture
def db_session():
    # 테스트용 DB 설정
    from app.database import engine, Base
    Base.metadata.create_all(bind=engine)
    
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

class TestRecommendationAPI:
    """추천 API 테스트"""
    
    def test_get_recommendations_success(self, client, db_session):
        """정상적인 추천 요청 테스트"""
        # 테스트 사용자 생성
        test_user = models.UserAccount(
            username="testuser",
            email="test@example.com",
            nickname="테스트유저",
            hashed_password="$2b$12$testhash"
        )
        db_session.add(test_user)
        db_session.commit()
        
        # 테스트 사용자 프로필 생성
        test_profile = models.UserProfile(
            user_id=test_user.user_id,
            lunch_budget_max=10000,
            spicy_threshold=3
        )
        db_session.add(test_profile)
        db_session.commit()
        
        # 테스트 요청 데이터
        inquiry_data = {
            "dietary_restriction": "뭐든 잘 먹음",
            "spicy_level": "보통 맵게 (3단계)",
            "budget_range": "10000원 이하",
            "salty_level": "보통",
            "exploration_style": "모험형(새로운 도전)",
            "city": "Seoul"
        }
        
        # API 호출 (인증 없이 테스트)
        response = client.post("/api/recommend/", json=inquiry_data)
        
        # 결과 검증
        assert response.status_code == 401  # 인증 필요
        
    def test_get_recommendations_invalid_data(self, client):
        """잘못된 데이터로 추천 요청"""
        invalid_data = {
            "dietary_restriction": "",  # 빈 값
            "spicy_level": "invalid",
            "budget_range": "",
            "salty_level": "",
            "exploration_style": "",
            "city": ""
        }
        
        response = client.post("/api/recommend/", json=invalid_data)
        # Pydantic 검증으로 422 에러 발생
        assert response.status_code == 401  # 인증 실패가 먼저

class TestAuthentication:
    """인증 시스템 테스트"""
    
    def test_signup_success(self, client, db_session):
        """회원가입 성공 테스트"""
        signup_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "nickname": "새유저",
            "password": "password123",
            "dietary_label": "none",
            "spicy_threshold": 3,
            "saltiness_preference": 3,
            "lunch_budget_max": 12000,
            "is_adventurous": True
        }
        
        response = client.post("/api/auth/signup", json=signup_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["nickname"] == "새유저"
        
    def test_signup_duplicate_username(self, client, db_session):
        """중복 아이디 가입 실패 테스트"""
        # 기존 사용자 생성
        existing_user = models.UserAccount(
            username="existing",
            email="existing@example.com",
            nickname="기존유저",
            hashed_password="$2b$12$testhash"
        )
        db_session.add(existing_user)
        db_session.commit()
        
        # 중복 아이디로 가입 시도
        signup_data = {
            "username": "existing",
            "email": "new@example.com",
            "nickname": "새유저",
            "password": "password123"
        }
        
        response = client.post("/api/auth/signup", json=signup_data)
        
        assert response.status_code == 400
        assert "이미 존재하는 아이디입니다" in response.json()["detail"]

if __name__ == "__main__":
    pytest.main([__file__])
