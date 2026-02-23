from app.database import SessionLocal
from app import models

# 기존 유저 데이터 모두 삭제
db = SessionLocal()

print('=== 기존 유저 데이터 삭제 시작 ===')

# 1. 추천 피드백 삭제
feedback_count = db.query(models.RecommendationFeedback).count()
print(f'1. 추천 피드백: {feedback_count}건 삭제')
db.query(models.RecommendationFeedback).delete()

# 2. 사용자 히스토리 삭제
history_count = db.query(models.UserHistory).count()
print(f'2. 사용자 히스토리: {history_count}건 삭제')
db.query(models.UserHistory).delete()

# 3. 사용자 프로필 삭제
profile_count = db.query(models.UserProfile).count()
print(f'3. 사용자 프로필: {profile_count}건 삭제')
db.query(models.UserProfile).delete()

# 4. 사용자 계정 삭제
user_count = db.query(models.UserAccount).count()
print(f'4. 사용자 계정: {user_count}건 삭제')
db.query(models.UserAccount).delete()

# 변경사항 저장
db.commit()

print('=== 기존 유저 데이터 삭제 완료 ===')
print(f'삭제된 데이터:')
print(f'- 추천 피드백: {feedback_count}건')
print(f'- 사용자 히스토리: {history_count}건')
print(f'- 사용자 프로필: {profile_count}건')
print(f'- 사용자 계정: {user_count}건')

db.close()
