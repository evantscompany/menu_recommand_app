# Railway 환경에서 TiDB Cloud 연결 가이드

## 🚨 문제 원인

### 1. IP 화이트리스트 문제
- **현재 상황**: Railway 서버 IP가 TiDB 허용 목록에 없음
- **해결책**: TiDB Cloud 콘솔에서 IP Access List에 `0.0.0.0/0` 추가

### 2. TLS/SSL 인증서 문제
- **현재 상황**: Railway 환경에서 CA 인증서 파일을 찾지 못함
- **해결책**: SSL 설정을 딕셔너리로 명시

## 🔧 해결 방안

### 1. TiDB Cloud IP 허용 설정

1. [TiDB Cloud 콘솔](https://tidbcloud.com/) 접속
2. `Clusters` → 해당 클러스터 선택
3. `Security` → `IP Access List` 메뉴 이동
4. `Add IP Access` 클릭
5. **CIDR 블록**: `0.0.0.0/0` 입력 (모든 IP 허용)
6. `Save` 클릭

### 2. Railway 환경 변수 설정

Railway 프로젝트 설정에서 다음 환경 변수 추가:

```bash
# TiDB Cloud 연결 정보
TIDB_HOST=gateway01.ap-northeast-1.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USER=3bJdto8FKWk47Fu.root
TIDB_PASSWORD=NWOZOcYDO8W5nMk2
TIDB_DATABASE=test
```

### 3. 데이터베이스 연결 코드 수정

기존 `database_mysql.py` 대신 `database_railway.py` 사용:

```python
# main.py에서 import 변경
from app.database_railway import engine, SessionLocal
```

## 🎯 예상 결과

- IP 화이트리스트 문제 해결
- SSL 인증서 문제 해결
- Railway에서 TiDB Cloud 안정적 연결
- 타임아웃 현상 해결

## 📋 확인 방법

1. Railway 로그 확인
2. TiDB Cloud 연결 테스트
3. API 엔드포인트 정상 작동 확인
