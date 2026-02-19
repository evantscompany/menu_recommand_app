# 메뉴 추천 API 명세서 v2.1.1 (간소화 버전)

## 기본 정보
- **Base URL**: `http://localhost:8000`
- **인증**: JWT Bearer Token
- **Content-Type**: `application/json`

---

## 1. 인증 API

### 로그인
```http
POST /api/auth/login
```

**Request**:
```json
{
  "username": "aaa",
  "password": "password123"
}
```

**Response**:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "username": "aaa",
  "nickname": "매운맛 애호가"
}
```

---

## 2. 사용자 프로필 관리 (v2.1.1 신규)

### 내 프로필 조회
```http
GET /api/users/me
Authorization: Bearer <token>
```

**Response**:
```json
{
  "user_id": 1,
  "username": "aaa",
  "nickname": "매운맛 애호가",
  "email": "aaa@example.com",
  "profile": {
    "spicy_threshold": 5,
    "lunch_budget_max": 15000,
    "is_adventurous": true,
    "dietary_label": "none"
  }
}
```

### 프로필 수정
```http
PUT /api/users/me
Authorization: Bearer <token>
```

**Request**:
```json
{
  "nickname": "새로운 닉네임",
  "spicy_threshold": 4,
  "lunch_budget_max": 12000,
  "is_adventurous": false
}
```

### 비밀번호 변경
```http
PUT /api/users/me/password
Authorization: Bearer <token>
```

**Request**:
```json
{
  "current_password": "password123",
  "new_password": "newpassword456"
}
```

### 회원탈퇴
```http
DELETE /api/users/me
Authorization: Bearer <token>
```

**Response**:
```json
{
  "message": "회원탈퇴가 완료되었습니다."
}
```

---

## 3. 추천 API

### 메뉴 추천 받기
```http
POST /api/recommend/
Authorization: Bearer <token>
```

**Response** (메뉴 3개):
```json
[
  {
    "menu_id": 1,
    "menu_name": "김치찌개",
    "category": "한식",
    "price": 11000,
    "match_rate": 85,
    "description": "매운맛 애호가에게 완벽한 김치찌개!",
    "details": {
      "spicy_level": 4,
      "texture": "쫄깃함",
      "rating": 4.2
    }
  }
]
```

---

## 4. 피드백 API

### 즉시 피드백
```http
POST /api/recommend/feedback/instant
Authorization: Bearer <token>
```

**Request**:
```json
{
  "menu_name": "김치찌개",
  "feedback_type": "excellent",
  "score": 4.9
}
```

**Feedback Type (v2.0)**:
```json
{
  "positive_types": ["excellent", "good", "love", "like"],
  "neutral_types": ["neutral", "okay"],
  "negative_types": ["poor", "bad", "dislike"]
}
```

---

## 5. 에러 처리
- `200`: 성공
- `400`: 요청 데이터 오류
- `401`: 인증 실패
- `404`: 리소스 없음
- `500`: 서버 오류

---

## 6. 사용 예제

### JavaScript
```javascript
// 1. 로그인
const login = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'aaa', password: 'password123' })
});
const { access_token } = await login.json();

// 2. 프로필 조회
const profile = await fetch('/api/users/me', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});

// 3. 프로필 수정
await fetch('/api/users/me', {
  method: 'PUT',
  headers: { 
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    nickname: '새로운 닉네임',
    spicy_threshold: 4
  })
});

// 4. 회원탈퇴
await fetch('/api/users/me', {
  method: 'DELETE',
  headers: { 'Authorization': `Bearer ${access_token}` }
});
```

---

## 7. v2.1.1 특징
- **프로필 관리**: 조회, 수정, 비밀번호 변경, 회원탈퇴
- **422 에러 해결**: 경로 충돌 문제 완전 해결
- **성능 최적화**: 불필요한 DB 쿼리 제거
- **안정성**: 100% API 성공률 달성
- **인증**: JWT 토큰 기반 보안

---

## 8. 테스트 계정
- **aaa**: password123 (매운맛 애호가)
- **bbb**: password123 (건강식 애호가)  
- **ccc**: password123 (중용파)

---

## 9. v2.1.1 개선 사항
- **422 에러 해결**: 프로필 조회 경로 충돌 해결
- **성능 최적화**: DB 재조회 제거
- **안정성 향상**: 에러 처리 개선
- **사용자 경험**: 직관적인 프로필 관리
