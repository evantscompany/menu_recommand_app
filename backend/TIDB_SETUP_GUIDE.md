# 🔗 TiDB Cloud 연결 정보 확인 방법

## 📋 TiDB Cloud 대시보드 접속

### 1. **TiDB Cloud 로그인**
1. [TiDB Cloud](https://tidbcloud.com/) 접속
2. Google 계정 또는 이메일로 로그인

### 2. **클러스터 선택**
1. 대시보드에서 생성된 클러스터 선택
2. 클러스터 이름 클릭 → 상세 정보 페이지 이동

### 3. **연결 정보 확인**
클러스터 상세 페이지에서 다음 정보를 확인:

#### 🏷️ **Host (호스트)**
```
Endpoint: gateway01.ap-southeast-1.prod.aws.tidbcloud.com
```

#### 🔌 **Port (포트)**
```
Port: 4000
```

#### 👤 **User (사용자)**
```
Username: 3bJdto8FKWk47Fu.root
```
- `root`는 기본 관리자 계정
- 실제 사용자명은 클러스터 생성 시 설정한 값

#### 🔐 **Password (비밀번호)**
```
Password: NWOZOcYDO8W5nMk2
```
- 클러스터 생성 시 설정한 비밀번호
- 보안을 위해 대시보드에서 일부만 표시될 수 있음

## 🛠️ **연결 테스트 방법**

### 방법 1: Python 스크립트로 테스트
```python
import os
from sqlalchemy import create_engine, text

# 환경 변수 설정
os.environ["TIDB_HOST"] = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
os.environ["TIDB_PORT"] = "4000"
os.environ["TIDB_USER"] = "3bJdto8FKWk47Fu.root"
os.environ["TIDB_PASSWORD"] = "NWOZOcYDO8W5nMk2"
os.environ["TIDB_DATABASE"] = "menu_recommendation"

# 연결 테스트
engine = create_engine(
    f"mysql+pymysql://{os.environ['TIDB_USER']}:{os.environ['TIDB_PASSWORD']}@{os.environ['TIDB_HOST']}:{os.environ['TIDB_PORT']}/{os.environ['TIDB_DATABASE']}"
)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT VERSION()"))
        print(f"✅ 연결 성공: {result.fetchone()[0]}")
except Exception as e:
    print(f"❌ 연결 실패: {e}")
```

### 방법 2: MySQL 클라이언트로 테스트
```bash
# MySQL Workbench 또는 DBeaver 사용
Host: gateway01.ap-southeast-1.prod.aws.tidbcloud.com
Port: 4000
Username: 3bJdto8FKWk47Fu.root
Password: NWOZOcYDO8W5nMk2
Database: menu_recommendation
```

## 🔍 **정보가 없을 경우**

### 1. **새 사용자 생성**
```sql
-- TiDB Cloud에서 SQL 콘솔 사용
CREATE USER 'newuser'@'%' IDENTIFIED BY 'newpassword';
GRANT ALL PRIVILEGES ON menu_recommendation.* TO 'newuser'@'%';
FLUSH PRIVILEGES;
```

### 2. **비밀번호 재설정**
1. TiDB Cloud 대시보드 → 클러스터 선택
2. "Security" 또는 "Users" 탭
3. 사용자 선택 → "Reset Password"

### 3. **연결 문자열 복사**
대시보드에서 "Connect" 버튼 클릭 → 연결 문자열 복사 가능

## 📱 **TiDB Cloud 모바일 앱**
1. 스마트폰에서 TiDB Cloud 접속
2. 클러스터 관리 가능
3. 연결 정보 실시간 확인

## ⚠️ **보안 주의사항**
- 비밀번호는 절대 GitHub에 커밋하지 마세요
- 환경 변수로 안전하게 관리하세요
- 필요시 최소 권한 사용자를 생성하세요

---

📞 **문제 발생 시:**
1. TiDB Cloud 공식 문서 확인
2. 클러스터 상태 확인
3. 네트워크 방화벽 확인
