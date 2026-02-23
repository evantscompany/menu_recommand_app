# 메뉴 추천 앱 백엔드

## 환경 설정

### 1. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 API 키를 설정하세요:

```bash
cp .env.example .env
```

`.env` 파일에 실제 API 키를 입력:
```env
# 기상청 API 설정
KMA_API_KEY=your_actual_kma_api_key
KMA_WEATHER_URL=https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtFcst

# 서울 좌표 설정
SEOUL_NX=55
SEOUL_NY=127
```

### 4. 데이터베이스 초기화
```bash
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

### 5. 서버 실행
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API 문서
서버 실행 후 http://localhost:8000/docs 에서 API 문서를 확인할 수 있습니다.

## 주요 기능
- 🍽️ 개인화된 메뉴 추천
- 🌤️ 실시간 날씨 데이터 반영
- 💬 사용자 피드백 기반 학습
- 🎯 사용자 성향 기반 추천

## 보안 주의사항
- `.env` 파일은 절대 Git에 커밋하지 마세요
- API 키는 안전하게 보관하세요
- `.gitignore`에 환경 변수 파일이 포함되어 있는지 확인하세요
