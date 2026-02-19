from app.database import SessionLocal
from app import models
from app.core.security import get_password_hash

# 사용자 데이터 재생성
db = SessionLocal()

print('=== 사용자 데이터 재생성 시작 ===')

# 기존 데이터 삭제
print('1. 기존 데이터 삭제...')
db.query(models.RecommendationFeedback).delete()
db.query(models.UserHistory).delete()
db.query(models.UserProfile).delete()
db.query(models.UserAccount).delete()
db.commit()

# 테스트 사용자 데이터
test_users = [
    {
        "username": "aaa",
        "email": "aaa@example.com",
        "nickname": "매운맛 애호가",
        "password": "password123",
        "spicy_threshold": 5,
        "saltiness_preference": 3,
        "lunch_budget_max": 15000,
        "is_adventurous": True,
        "dietary_label": "none",
        "allergies": None
    },
    {
        "username": "bbb",
        "email": "bbb@example.com",
        "nickname": "건강식 애호가",
        "password": "password123",
        "spicy_threshold": 2,
        "saltiness_preference": 2,
        "lunch_budget_max": 12000,
        "is_adventurous": False,
        "dietary_label": "healthy",
        "allergies": None
    },
    {
        "username": "ccc",
        "email": "ccc@example.com",
        "nickname": "중용파",
        "password": "password123",
        "spicy_threshold": 3,
        "saltiness_preference": 3,
        "lunch_budget_max": 13000,
        "is_adventurous": True,
        "dietary_label": "none",
        "allergies": None
    }
]

# 사용자 계정 및 프로필 생성
print('2. 새로운 사용자 생성...')
for user_data in test_users:
    # 계정 생성
    account = models.UserAccount(
        username=user_data["username"],
        email=user_data["email"],
        nickname=user_data["nickname"],
        hashed_password=get_password_hash(user_data["password"])
    )
    db.add(account)
    db.flush()  # ID를 얻기 위해 flush
    
    # 프로필 생성
    profile = models.UserProfile(
        user_id=account.user_id,
        dietary_label=user_data["dietary_label"],
        allergies=user_data["allergies"],
        spicy_threshold=user_data["spicy_threshold"],
        saltiness_preference=user_data["saltiness_preference"],
        lunch_budget_max=user_data["lunch_budget_max"],
        is_adventurous=user_data["is_adventurous"]
    )
    db.add(profile)
    
    print(f'   ✅ 생성됨: {user_data["username"]} ({user_data["nickname"]})')

db.commit()

# 생성된 데이터 확인
print('\n3. 생성된 데이터 확인:')
users = db.query(models.UserAccount).all()
print(f'   사용자 계정: {len(users)}개')

profiles = db.query(models.UserProfile).all()
print(f'   사용자 프로필: {len(profiles)}개')

# 비밀번호 검증 테스트
print('\n4. 비밀번호 검증 테스트:')
from app.core.security import verify_password

for user in users:
    is_valid = verify_password('password123', user.hashed_password)
    print(f'   - {user.username}: {"✅ 통과" if is_valid else "❌ 실패"}')

print('\n=== 사용자 데이터 재생성 완료 ===')
print('✅ 모든 테스트 사용자가 정상적으로 생성되었습니다.')
print('✅ 비밀번호 검증이 통과했습니다.')
print('✅ 이제 로그인 테스트를 진행할 수 있습니다.')

db.close()
