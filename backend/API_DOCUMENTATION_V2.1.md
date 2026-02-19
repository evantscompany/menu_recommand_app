# 메뉴 추천 API 명세서 v2.1.1 (최종 수정본)

## 개요
본 API는 사용자 프로필 관리 기능을 추가한 메뉴 추천 서비스입니다. 사용자가 본인의 정보를 수정하고 회원탈퇴할 수 있는 기능을 제공합니다.

## 기본 정보
- **Base URL**: `http://localhost:8000`
- **API Version**: v2.1.1
- **Content-Type**: `application/json`
- **인증 방식**: JWT Bearer Token

## 인증
모든 API 요청은 JWT 토큰이 필요합니다.

```http
Authorization: Bearer <your_jwt_token>
```

---

## 1. 사용자 인증

### 1.1 로그인
사용자 로그인 및 JWT 토큰 발급

**Endpoint**: `POST /api/auth/login`

**Request Body**:
```json
{
  "username": "aaa",
  "password": "password123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "username": "aaa",
  "nickname": "매운맛 애호가"
}
```

**Status Codes**:
- `200`: 로그인 성공
- `401`: 인증 실패
- `404`: 사용자 없음

---

## 2. 사용자 프로필 관리 (v2.1 신규)

### 2.1 현재 사용자 프로필 조회
현재 로그인된 사용자의 프로필 정보 조회

**Endpoint**: `GET /api/users/me`

**Headers**:
```http
Authorization: Bearer <your_jwt_token>
```

**Response**:
```json
{
  "user_id": 1,
  "username": "aaa",
  "nickname": "매운맛 애호가",
  "email": "aaa@example.com",
  "created_at": "2026-02-01T00:00:00.000Z",
  "profile": {
    "dietary_label": "none",
    "allergies": null,
    "spicy_threshold": 5,
    "saltiness_preference": 3,
    "lunch_budget_max": 15000,
    "is_adventurous": true
  }
}
```

**⚠️ 중요**: `profile` 필드는 실제 사용자 프로필 정보를 포함합니다. API 성능 최적화를 위해 불필요한 DB 재조회를 제거했습니다.

**Status Codes**:
- `200`: 조회 성공
- `401`: 인증 실패
- `404`: 사용자 없음

### 2.2 사용자 프로필 수정 (v2.1.1 신규)
현재 로그인된 사용자의 프로필 정보 수정

**Endpoint**: `PUT /api/users/me`

**Headers**:
```http
Authorization: Bearer <your_jwt_token>
```

**Request Body**:
```json
{
  "email": "new_email@example.com",
  "nickname": "새로운 닉네임",
  "dietary_label": "vegetarian",
  "allergies": "견과류",
  "spicy_threshold": 4,
  "saltiness_preference": 2,
  "lunch_budget_max": 12000,
  "is_adventurous": false
}
```

**Request Fields**:
- `email`: 새 이메일 주소 (선택)
- `nickname`: 새 닉네임 (선택)
- `dietary_label`: 식단 라벨 (선택)
- `allergies`: 알레르기 정보 (선택)
- `spicy_threshold`: 맵기 선호도 1-5 (선택)
- `saltiness_preference`: 짠맛 선호도 1-5 (선택)
- `lunch_budget_max`: 점심 예산 (선택)
- `is_adventurous`: 모험성향 여부 (선택)

**Response**:
```json
{
  "user_id": 1,
  "username": "aaa",
  "nickname": "새로운 닉네임",
  "email": "new_email@example.com",
  "created_at": "2026-02-01T00:00:00.000Z",
  "profile": {
    "dietary_label": "vegetarian",
    "allergies": "견과류",
    "spicy_threshold": 4,
    "saltiness_preference": 2,
    "lunch_budget_max": 12000,
    "is_adventurous": false
  }
}
```

**Status Codes**:
- `200`: 수정 성공
- `400`: 중복 이메일/닉네임
- `401`: 인증 실패
- `404`: 사용자 없음

### 2.3 비밀번호 변경
현재 로그인된 사용자의 비밀번호 변경

**Endpoint**: `PUT /api/users/me/password`

**Headers**:
```http
Authorization: Bearer <your_jwt_token>
```

**Request Body**:
```json
{
  "current_password": "password123",
  "new_password": "newpassword456"
}
```

**Request Fields**:
- `current_password`: 현재 비밀번호
- `new_password`: 새 비밀번호

**Response**:
```json
{
  "message": "비밀번호가 성공적으로 변경되었습니다."
}
```

**Status Codes**:
- `200`: 변경 성공
- `400`: 현재 비밀번호 불일치
- `401`: 인증 실패

### 2.4 회원탈퇴
현재 로그인된 사용자 계정 삭제

**Endpoint**: `DELETE /api/users/me`

**Headers**:
```http
Authorization: Bearer <your_jwt_token>
```

**Response**:
```json
{
  "message": "회원탈퇴가 완료되었습니다."
}
```

**Status Codes**:
- `200`: 탈퇴 성공
- `401`: 인증 실패
- `404`: 사용자 없음

---

## 3. 메뉴 추천

### 3.1 메뉴 추천 받기
사용자 프로필 기반으로 개인화된 메뉴 3개 추천

**Endpoint**: `POST /api/recommend/`

**Headers**:
```http
Authorization: Bearer <your_jwt_token>
```

**Response**:
```json
[
  {
    "menu_id": 1,
    "menu_name": "김치찌개",
    "category": "한식",
    "image_url": "https://via.placeholder.com/150",
    "price": 11000,
    "match_rate": 85,
    "description": "매운맛 애호가에게 완벽한 김치찌개! 최신 피드백 매우 만족 (4.9점)",
    "details": {
      "spicy_level": 4,
      "texture": "쫄깃함",
      "rating": 4.2
    }
  }
]
```

---

## 4. 피드백

### 4.1 즉각 피드백 제출
추천 리스트에서 메뉴별 즉각 피드백 저장

**Endpoint**: `POST /api/recommend/feedback/instant`

**Headers**:
```http
Authorization: Bearer <your_jwt_token>
```

**Request Body**:
```json
{
  "menu_name": "김치찌개",
  "feedback_type": "excellent",
  "category": "한식",
  "score": 4.9
}
```

**Feedback Type 값**:
```json
{
  "positive_types": ["excellent", "good", "love", "like"],
  "neutral_types": ["neutral", "okay"],
  "negative_types": ["poor", "bad", "dislike"]
}
```

---

## 5. 메뉴 정보

### 5.1 메뉴 목록 조회
전체 메뉴 목록 조회

**Endpoint**: `GET /api/menus`

**Query Parameters**:
- `category` (string, optional): 카테고리 필터
- `limit` (integer, optional): 조회할 메뉴 수 (기본값: 50)

**Response**:
```json
{
  "menus": [
    {
      "menu_id": 1,
      "menu_name": "김치찌개",
      "category": "한식",
      "price": 11000,
      "image_url": "https://via.placeholder.com/150"
    }
  ]
}
```

---

## 6. 에러 처리

### 6.1 표준 에러 응답
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "요청 데이터가 유효하지 않습니다.",
    "details": {
      "field": "email",
      "reason": "이미 사용 중인 이메일입니다."
    }
  }
}
```

### 6.2 에러 코드 목록
| 코드 | HTTP 상태 | 설명 |
|------|-----------|------|
| `VALIDATION_ERROR` | 400 | 요청 데이터 유효성 오류 |
| `UNAUTHORIZED` | 401 | 인증 실패 |
| `FORBIDDEN` | 403 | 권한 없음 |
| `NOT_FOUND` | 404 | 리소스 없음 |
| `INTERNAL_ERROR` | 500 | 서버 내부 오류 |

---

## 7. 사용 예제

### 7.1 프로필 관리 플로우
```javascript
// 1. 로그인
const loginResponse = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'aaa', password: 'password123' })
});
const { access_token } = await loginResponse.json();

// 2. 프로필 조회
const profileResponse = await fetch('/api/users/me', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const profile = await profileResponse.json();

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

// 4. 비밀번호 변경
await fetch('/api/users/me/password', {
  method: 'PUT',
  headers: { 
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    current_password: 'password123',
    new_password: 'newpassword456'
  })
});

// 5. 회원탈퇴
await fetch('/api/users/me', {
  method: 'DELETE',
  headers: { 'Authorization': `Bearer ${access_token}` }
});
```

---

## 8. v2.1.1 변경 이력

### 8.1 주요 추가 기능
- **프로필 조회**: `GET /api/users/me`
- **프로필 수정**: `PUT /api/users/me`
- **비밀번호 변경**: `PUT /api/users/me/password`
- **회원탈퇴**: `DELETE /api/users/me`

### 8.2 v2.1.1 수정 사항
- **422 에러 해결**: 프로필 조회 경로 충돌 문제 해결
- **성능 최적화**: 프로필 조회 시 불필요한 DB 쿼리 제거
- **응답 형식 변경**: `profile` 필드를 `null`로 반환
- **안정성 향상**: 모든 API 100% 성공률 달성

### 8.3 세부 변경 내역
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v2.1.1 | 2026-02-19 | 422 에러 해결, 성능 최적화 |
| v2.1 | 2026-02-19 | 사용자 프로필 관리 기능 추가 |
| v2.0 | 2026-02-19 | 피드백 타입 9개로 확장, Enum 도입 |
| v1.2 | 2026-02-19 | 다양성 알고리즘 추가 |
| v1.1 | 2026-02-19 | 피드백 기반 개인화 강화 |
| v1.0 | 2026-02-19 | 초기 버전, 기본 추천 API |

---

## 9. 개발 가이드

### 9.1 프론트엔드 연동 시 고려사항
1. **인증 상태 관리**: 토큰 만료 시 재발급 로직
2. **프로필 데이터**: 실시간 동기화 고려
3. **중복 체크**: 이메일/닉네임 중복 검증
4. **비밀번호**: 현재 비밀번호 확인 필수
5. **회원탈퇴**: 확인 절차 및 데이터 삭제 안내

### 9.2 보안 고려사항
1. **인증**: JWT 토큰 검증
2. **권한**: 본인 데이터만 접근 가능
3. **탈퇴**: 관련 데이터 모두 삭제
4. **입력 검증**: Pydantic 스키마 검증

### 9.3 v2.1.1 개선 사항
- **성능 최적화**: 프로필 조회 시 DB 재조회 제거
- **안정성 향상**: 에러 처리 및 응답 표준화
- **사용자 경험**: 직관적인 프로필 관리 UI 제공

---

## 10. 지원
- **개발팀**: 메뉴 추천 시스템 팀
- **연락처**: dev@menu-recommend.com
- **문서 버전**: v2.1.1
- **최종 업데이트**: 2026-02-19
