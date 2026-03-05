# API 엔드포인트 변경 (로컬 → 배포)

## Base URL 변경
```
기존 (로컬): http://localhost:8000
배포 (Render): https://menu-recommand-app.onrender.com
```

## API 엔드포인트

### 인증
- **회원가입**: `POST /api/auth/signup`
- **로그인**: `POST /api/auth/login`

### 사용자
- **내 프로필**: `GET /api/users/me` (인증 필요)

### 메뉴
- **메뉴 목록**: `GET /api/menus?skip=0&limit=10`

### 추천 (인증 필요)
- **메뉴 추천**: `POST /api/recommend/`
- **메뉴 추천 (GET)**: `GET /api/recommend/recommendations`

### 피드백 (인증 필요)
- **즉각 피드백**: `POST /api/recommend/feedback/instant`
- **메뉴 선택**: `POST /api/recommend/select/{menu_id}`

### 날씨
- **서울 날씨**: `GET /api/weather/seoul`

## 테스트 계정
```
아이디: produser
비밀번호: prod1234
```
