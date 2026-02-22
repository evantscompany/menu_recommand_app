# 🍽️ 메뉴 추천 앱 API 명세서

## 📋 개요
메뉴 추천 앱의 프론트엔드-백엔드 통신을 위한 API 명세서입니다.

**서버 정보**
- **기본 URL**: `http://192.168.0.22:8000`
- **인증 방식**: JWT Bearer Token
- **데이터 형식**: JSON

---

## 🔐 인증 관련 API

### 1. 회원가입
**엔드포인트**: `POST /api/auth/signup`

**요청 데이터**:
```json
{
  "username": "string",           // 계정 ID (필수)
  "email": "string",              // 이메일 주소 (필수)
  "nickname": "string",           // 닉네임 (필수)
  "password": "string",           // 비밀번호 (필수, 8자 이상)
  "dietary_label": "string",      // 식단 제한 (기본값: "none")
  "allergies": "string",          // 알레르기 정보 (선택사항)
  "spicy_threshold": "number",    // 매운맛 선호도 1-5 (기본값: 3)
  "saltiness_preference": "number", // 짠맛 선호도 1-5 (기본값: 3)
  "lunch_budget_max": "number",  // 점심 예산 상한선 (기본값: 12000)
  "is_adventurous": "boolean"    // 새로운 메뉴 도전 여부 (기본값: true)
}
```

**성공 응답** (201):
```json
{
  "user_id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "nickname": "테스트유저",
  "created_at": "2026-02-20T00:00:00",
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

**에러 응답** (400/422):
```json
{
  "detail": "이미 존재하는 아이디입니다."
}
```

---

### 2. 로그인
**엔드포인트**: `POST /api/auth/login`

**요청 데이터**:
```json
{
  "username": "string",  // 계정 ID
  "password": "string"   // 비밀번호
}
```

**성공 응답** (200):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "username": "testuser",
  "nickname": "테스트유저"
}
```

**에러 응답** (401):
```json
{
  "detail": "아이디 또는 비밀번호가 틀렸습니다."
}
```

---

### 3. 현재 사용자 정보 조회
**엔드포인트**: `GET /api/auth/me`

**헤더**:
```
Authorization: Bearer {token}
```

**성공 응답** (200):
```json
{
  "user_id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "nickname": "테스트유저",
  "created_at": "2026-02-20T00:00:00",
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

## 🍱 메뉴 추천 API

### 1. 메뉴 추천 받기
**엔드포인트**: `POST /api/recommend/`

**헤더**:
```
Authorization: Bearer {token}
```

**성공 응답** (200):
```json
[
  {
    "menu_name": "김치찌개",
    "category": "한식",
    "image_url": "https://via.placeholder.com/150",
    "price": 11000,
    "match_rate": 97,
    "description": "오늘 날씨에 어울리는 따끈한 한식 메뉴를 추천해요!",
    "details": {
      "spicy_level": 3,
      "texture": "일반적",
      "rating": 4.2
    },
    "restaurant_info": null
  },
  {
    "menu_name": "돈까스",
    "category": "양식",
    "image_url": "https://via.placeholder.com/150",
    "price": 13000,
    "match_rate": 85,
    "description": "예산에 맞는 만족도 높은 양식 메뉴를 추천해요!",
    "details": {
      "spicy_level": 1,
      "texture": "바삭함",
      "rating": 4.5
    },
    "restaurant_info": null
  },
  {
    "menu_name": "파스타",
    "category": "양식",
    "image_url": "https://via.placeholder.com/150",
    "price": 12000,
    "match_rate": 78,
    "description": "새로운 맛을 찾는 당신을 위한 이탈리안 메뉴를 추천해요!",
    "details": {
      "spicy_level": 2,
      "texture": "쫄깃함",
      "rating": 4.1
    },
    "restaurant_info": null
  }
]
```

---

### 2. 메뉴 선택 (히스토리 기록)
**엔드포인트**: `POST /api/recommend/select/{menu_id}`

**헤더**:
```
Authorization: Bearer {token}
```

**성공 응답** (200):
```json
{
  "message": "김치찌개 선택 완료",
  "history_id": 123
}
```

---

### 3. 피드백 제출
**엔드포인트**: `POST /api/recommend/feedback`

**헤더**:
```
Authorization: Bearer {token}
```

**요청 데이터**:
```json
{
  "menu_name": "김치찌개",
  "feedback_type": "like",
  "category": "한식",
  "score": 5
}
```

**성공 응답** (200):
```json
{
  "message": "피드백이 저장되었습니다",
  "feedback_id": 456
}
```

---

## 📝 프론트엔드 구현 가이드

### 1. 기본 설정
```javascript
const API_BASE_URL = 'http://192.168.0.22:8000';

// API 요청 기본 설정
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 토큰 인증 인터셉터
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### 2. 회원가입 예시
```javascript
const signup = async (userData) => {
  try {
    const response = await apiClient.post('/api/auth/signup', userData);
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || '회원가입 실패';
  }
};
```

### 3. 로그인 예시
```javascript
const login = async (username, password) => {
  try {
    const response = await apiClient.post('/api/auth/login', {
      username,
      password,
    });
    
    const { token } = response.data;
    localStorage.setItem('access_token', token);
    
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || '로그인 실패';
  }
};
```

### 4. 메뉴 추천 예시
```javascript
const getRecommendations = async () => {
  try {
    const response = await apiClient.post('/api/recommend/');
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || '추천 정보 가져오기 실패';
  }
};
```

---

## 🚨 에러 처리

### 공통 에러 코드
- **400**: Bad Request - 요청 데이터 형식 오류
- **401**: Unauthorized - 인증 실패 또는 토큰 만료
- **404**: Not Found - 리소스 없음
- **422**: Unprocessable Entity - 데이터 검증 실패
- **500**: Internal Server Error - 서버 내부 오류

### 에러 응답 형식
```json
{
  "detail": "에러 메시지 상세 설명"
}
```

---

## 🔄 데이터 흐름

### 회원가입 → 로그인 → 추천 순서
1. **회원가입**: `POST /api/auth/signup`
2. **로그인**: `POST /api/auth/login` → 토큰 저장
3. **메뉴 추천**: `POST /api/recommend/` (토큰 필요)
4. **메뉴 선택**: `POST /api/recommend/select/{menu_id}` (선택사항)
5. **피드백 제출**: `POST /api/recommend/feedback` (선택사항)

---

## 📱 테스트 계정
| 아이디 | 비밀번호 | 닉네임 | 특징 |
|--------|----------|--------|------|
| aaa | password123 | 매운맛 애호가 | 맵참이 (spicy_threshold: 5) |
| bbb | password123 | 건강식 애호가 | 다이어터 (dietary_label: "healthy") |
| ccc | password123 | 중용파 | 평균적인 취향 |

---

## 🛠️ 개발 팁

1. **토큰 관리**: 로그인 성공 시 `token` 필드 값을 저장하세요
2. **에러 처리**: 항상 try-catch로 API 호출을 감싸세요
3. **데이터 검증**: 프론트엔드에서 필수 필드를 미리 검증하세요
4. **네트워크 상태**: 오프라인 상태를 고려한 예외 처리를 하세요
5. **로딩 상태**: API 호출 중 로딩 인디케이터를 표시하세요

---

*마지막 업데이트: 2026-02-20*
