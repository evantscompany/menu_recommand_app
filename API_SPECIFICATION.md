# 메추리 API 명세서 (Render 배포 환경)

## 기본 정보

### Base URL
```
https://menu-recommand-app.onrender.com
```

### 인증 방식
- JWT Bearer Token 인증
- 로그인 후 받은 `access_token`을 Authorization 헤더에 포함

### 공통 헤더
```http
Content-Type: application/json
Authorization: Bearer {access_token}
```

---

## 1. 인증 API

### 1.1 회원가입
**POST** `/api/auth/signup`

#### Request Body
```json
{
  "username": "testuser",
  "password": "test1234",
  "email": "test@example.com",
  "nickname": "테스트유저",
  "dietary_label": "none",
  "allergies": null,
  "spicy_threshold": 3,
  "saltiness_preference": 3,
  "lunch_budget_max": 12000,
  "is_adventurous": true
}
```

#### Response (201 Created)
```json
{
  "user_id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "nickname": "테스트유저",
  "profile": {
    "dietary_label": "none",
    "spicy_threshold": 3,
    "saltiness_preference": 3,
    "lunch_budget_max": 12000,
    "is_adventurous": true
  }
}
```

#### Error Response (400)
```json
{
  "detail": "이미 존재하는 아이디입니다."
}
```

---

### 1.2 로그인
**POST** `/api/auth/login`

#### Request Body (Form Data)
```
username=testuser&password=test1234
```

또는 JSON:
```json
{
  "username": "testuser",
  "password": "test1234"
}
```

#### Response (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Error Response (401)
```json
{
  "detail": "아이디 또는 비밀번호가 일치하지 않습니다."
}
```

---

## 2. 사용자 API

### 2.1 내 프로필 조회
**GET** `/api/users/me`

#### Headers
```http
Authorization: Bearer {access_token}
```

#### Response (200 OK)
```json
{
  "user_id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "nickname": "테스트유저",
  "profile": {
    "dietary_label": "none",
    "allergies": null,
    "spicy_threshold": 3,
    "saltiness_preference": 3,
    "lunch_budget_max": 12000,
    "is_adventurous": true
  }
}
```

---

## 3. 메뉴 API

### 3.1 메뉴 목록 조회
**GET** `/api/menus?skip=0&limit=10`

#### Query Parameters
- `skip` (optional): 건너뛸 개수 (기본값: 0)
- `limit` (optional): 조회할 개수 (기본값: 100, 최대: 100)

#### Response (200 OK)
```json
[
  {
    "menu_id": 1,
    "menu_name": "김치찌개",
    "category": "한식",
    "price": 11000,
    "image_url": "https://example.com/image.jpg",
    "matching_weather": "Rain",
    "is_lunch_available": true,
    "details": {
      "spicy_level": 3,
      "saltiness_level": 3,
      "heaviness": 4.0,
      "serving_temperature": "Hot",
      "texture": "Soft",
      "real_satisfaction_score": 4.5
    }
  }
]
```

---

## 4. 메뉴 추천 API ⭐

### 4.1 메뉴 추천 (POST)
**POST** `/api/recommend/`

#### Headers
```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

#### Request Body (Optional)
```json
{
  "weather": "Rain",
  "mood": "Comfortable",
  "group_size": 2,
  "budget": 15000
}
```

> **Note:** Request Body는 선택사항입니다. 비어있어도 사용자 프로필 기반으로 추천합니다.

#### Response (200 OK)
```json
[
  {
    "menu_name": "김치찌개",
    "category": "한식",
    "price": 11000,
    "match_rate": 95,
    "description": "비/눈 오는 날(Rain)엔 따끈하고 든든한 김치찌개 어떠세요?",
    "image_url": "https://example.com/image.jpg",
    "details": {
      "spicy_level": 3,
      "texture": "Soft",
      "rating": 4.5
    },
    "restaurant_info": {
      "restaurant_id": 1,
      "restaurant_name": "맛있는 한식당",
      "address": "서울시 강남구",
      "category_1": "한식"
    }
  },
  {
    "menu_name": "된장찌개",
    "category": "한식",
    "price": 10000,
    "match_rate": 92,
    "description": "오늘 날씨(Rain)에 어울리는 한식 메뉴를 추천해요!",
    "image_url": "https://example.com/image2.jpg",
    "details": {
      "spicy_level": 2,
      "texture": "Soft",
      "rating": 4.3
    },
    "restaurant_info": null
  },
  {
    "menu_name": "순두부찌개",
    "category": "한식",
    "price": 9000,
    "match_rate": 88,
    "description": "추운 날(Rain)엔 따뜻한 순두부찌개으로 몸을 녹여보세요!",
    "image_url": "https://example.com/image3.jpg",
    "details": {
      "spicy_level": 4,
      "texture": "Soft",
      "rating": 4.6
    },
    "restaurant_info": null
  }
]
```

#### Error Response (401)
```json
{
  "detail": "Not authenticated"
}
```

---

### 4.2 메뉴 추천 (GET)
**GET** `/api/recommend/recommendations`

#### Headers
```http
Authorization: Bearer {access_token}
```

#### Response (200 OK)
동일한 형식으로 3개 메뉴 추천 반환

---

## 5. 피드백 API

### 5.1 즉각 피드백 제출
**POST** `/api/recommend/feedback/instant`

#### Headers
```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

#### Request Body
```json
{
  "menu_name": "김치찌개",
  "feedback_type": "excellent",
  "category": "한식",
  "score": 5.0
}
```

#### Feedback Types
- `excellent`: 매우 만족
- `good`: 만족
- `neutral`: 보통
- `bad`: 불만족
- `terrible`: 매우 불만족

#### Response (200 OK)
```json
{
  "feedback_id": 1,
  "user_id": 1,
  "menu_name": "김치찌개",
  "feedback_type": "excellent",
  "category": "한식",
  "score": 5.0,
  "created_at": "2026-03-05T09:00:00"
}
```

---

### 5.2 메뉴 선택 완료
**POST** `/api/recommend/select/{menu_id}`

#### Headers
```http
Authorization: Bearer {access_token}
```

#### Path Parameters
- `menu_id`: 선택한 메뉴 ID (integer)

#### Response (200 OK)
```json
{
  "message": "김치찌개 선택 완료",
  "history_id": 1
}
```

---

## 6. 날씨 API

### 6.1 서울 날씨 조회
**GET** `/api/weather/seoul`

#### Response (200 OK)
```json
{
  "weather": "Rain",
  "temperature": 15.5,
  "humidity": 75,
  "description": "비가 내리고 있습니다"
}
```

---

## 테스트 계정

### 프로덕션 환경 테스트 계정
```
아이디: produser
비밀번호: prod1234
이메일: prod@example.com
```

---

## 에러 코드

| 상태 코드 | 설명 |
|----------|------|
| 200 | 성공 |
| 201 | 생성 성공 |
| 400 | 잘못된 요청 |
| 401 | 인증 실패 |
| 404 | 리소스 없음 |
| 500 | 서버 에러 |

---

## CORS 설정

모든 Origin에서 접근 가능:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: *
```

---

## 사용 예시 (JavaScript)

### 로그인 및 메뉴 추천
```javascript
// 1. 로그인
const loginResponse = await fetch('https://menu-recommand-app.onrender.com/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: 'username=produser&password=prod1234'
});

const { access_token } = await loginResponse.json();

// 2. 메뉴 추천 받기
const recommendResponse = await fetch('https://menu-recommand-app.onrender.com/api/recommend/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({})  // 빈 객체 또는 조건 추가
});

const recommendations = await recommendResponse.json();
console.log(recommendations);
```

---

## 주요 변경사항 (develop_ver_04 → develop_ver_04_server)

### 1. 데이터베이스
- **이전**: SQLite (로컬)
- **현재**: TiDB Cloud MySQL (클라우드)
  - Host: `gateway01.ap-northeast-1.prod.aws.tidbcloud.com`
  - Port: `4000`
  - Database: `test`

### 2. 배포 환경
- **이전**: 로컬 개발 환경
- **현재**: Render (https://menu-recommand-app.onrender.com)

### 3. 메뉴 데이터
- **추가**: 349개 메뉴에 `matching_weather` 필드 추가
  - Rain, Clear, Clouds, Snow, Mist 날씨 조건별 매핑

### 4. 성능 최적화
- DB 쿼리 최적화 (N+1 문제 해결)
- 피드백 캐싱 추가
- 복잡한 알고리즘 전략 간소화 (Free tier 성능 개선)

---

## 문의사항

API 사용 중 문제가 발생하면 다음을 확인하세요:

1. **인증 토큰**: 로그인 후 받은 토큰을 올바르게 사용하고 있는지
2. **Content-Type**: JSON 요청 시 `application/json` 헤더 포함
3. **CORS**: 브라우저에서 요청 시 CORS 에러 확인
4. **응답 시간**: Render Free tier는 첫 요청 시 콜드 스타트로 인해 느릴 수 있음 (최대 30초)

---

## 버전 정보
- **API 버전**: v1
- **배포 환경**: Render Free Tier
- **데이터베이스**: TiDB Cloud Serverless
- **마지막 업데이트**: 2026-03-05
