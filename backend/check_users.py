from app.database import SessionLocal
from app import models

# 사용자 데이터 확인
db = SessionLocal()

print('=== 사용자 데이터 확인 ===')

# 사용자 계정 확인
users = db.query(models.UserAccount).all()
print(f'1. 사용자 계정: {len(users)}개')
for user in users:
    print(f'   - {user.username} ({user.nickname})')

# 사용자 프로필 확인
profiles = db.query(models.UserProfile).all()
print(f'2. 사용자 프로필: {len(profiles)}개')
for profile in profiles:
    print(f'   - User {profile.user_id}: 맵기 {profile.spicy_threshold}')

# 로그인 테스트
print(f'3. 로그인 테스트:')
from app.core.security import verify_password

for user in users:
    is_valid = verify_password('password123', user.hashed_password)
    print(f'   - {user.username}: 비밀번호 검증 {is_valid}')

db.close()
