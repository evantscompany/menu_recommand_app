from app.database import SessionLocal
from app import models

# 프로필 조회 문제 디버깅
db = SessionLocal()

print('=== 프로필 조회 422 에러 디버깅 ===')

# 1. 사용자 데이터 확인
users = db.query(models.UserAccount).all()
print(f'1. 사용자 계정: {len(users)}개')

for user in users:
    print(f'   - {user.username}: ID={user.user_id}, email={user.email}, nickname={user.nickname}')
    
    # 2. 프로필 데이터 확인
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user.user_id).first()
    if profile:
        print(f'     프로필: 맵기={profile.spicy_threshold}, 예산={profile.lunch_budget_max}')
    else:
        print(f'     프로필: 없음')

# 3. Pydantic 스키마 테스트
print(f'\n3. Pydantic 스키마 테스트:')
from app.schemas import User

try:
    user = users[0]  # 첫 번째 사용자
    user_data = {
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'nickname': user.nickname,
        'created_at': user.created_at,
        'profile': {
            'spicy_threshold': profile.spicy_threshold if profile else None,
            'saltiness_preference': profile.saltiness_preference if profile else None,
            'lunch_budget_max': profile.lunch_budget_max if profile else None,
            'is_adventurous': profile.is_adventurous if profile else None,
            'dietary_label': profile.dietary_label if profile else None,
            'allergies': profile.allergies if profile else None
        }
    }
    
    user_schema = User(**user_data)
    print(f'   ✅ 스키마 생성 성공: {user_schema.username}')
    print(f'   데이터 타입: {type(user_schema)}')
    
except Exception as e:
    print(f'   ❌ 스키마 생성 실패: {e}')
    print(f'   에러 타입: {type(e)}')

# 4. API 테스트 시뮬레이션
print(f'\n4. API 테스트 시뮬레이션:')
try:
    # GET /api/users/me 요청 시뮬레이션
    import requests
    
    # 로그인하여 토큰 발급
    login_response = requests.post('http://localhost:8000/api/auth/login', 
                              data={'username': 'aaa', 'password': 'password123'})
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        token = token_data.get('access_token')
        
        # 프로필 조회 요청
        headers = {'Authorization': f'Bearer {token}'}
        profile_response = requests.get('http://localhost:8000/api/users/me', headers=headers)
        
        print(f'   상태 코드: {profile_response.status_code}')
        if profile_response.status_code == 422:
            print(f'   응답 내용: {profile_response.text}')
        else:
            print(f'   응답 데이터: {profile_response.json()}')
    else:
        print(f'   로그인 실패: {login_response.status_code}')
        
except Exception as e:
    print(f'   API 테스트 실패: {e}')

db.close()
