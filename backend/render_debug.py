"""
Render Python 버전 문제 디버깅
"""

def analyze_render_python_issue():
    """Render Python 버전 문제 분석"""
    print("🔍 Render Python 버전 문제 분석")
    print("=" * 50)
    
    print("📋 현재 설정 상태:")
    print("  1. runtime.txt: python-3.11.8")
    print("  2. render.yaml PYTHON_VERSION: 3.11.8")
    print("  3. render.yaml env: python")
    print("  4. Render 실제 설치: Python 3.14.3")
    
    print("\n🚨 문제 원인 분석:")
    print("  가능성 1: render.yaml의 PYTHON_VERSION이 무시됨")
    print("  가능성 2: env: python이 3.14.3을 기본으로 사용")
    print("  가능성 3: Render 캐시 문제")
    print("  가능성 4: 환경 변수 우선순위 문제")
    
    print("\n🔧 해결책:")
    print("  방법 1: render.yaml에 pythonVersion 필드 추가")
    print("  방법 2: env: python3.11로 변경")
    print("  방법 3: PYTHON_VERSION 대신 PY_VERSION 사용")
    print("  방법 4: Force redeploy 파일 추가")

def create_fixed_render_yaml():
    """수정된 render.yaml 생성"""
    print("\n🔧 수정된 render.yaml 생성:")
    print("=" * 50)
    
    fixed_yaml = """services:
  # FastAPI 백엔드 서비스
  - type: web
    name: menu-recommend-api
    env: python
    plan: free
    pythonVersion: "3.11"  # 명시적인 Python 버전
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      # TiDB Cloud 연결 정보
      - key: TIDB_HOST
        value: gateway01.ap-northeast-1.prod.aws.tidbcloud.com
      - key: TIDB_PORT
        value: 4000
      - key: TIDB_USER
        value: 3bJdto8FKWk47Fu.root
      - key: TIDB_PASSWORD
        value: NWOZOcYDO8W5nMk2
      - key: TIDB_DATABASE
        value: test
      
      # JWT 설정
      - key: SECRET_KEY
        generateValue: true
      - key: ALGORITHM
        value: HS256
      - key: ACCESS_TOKEN_EXPIRE_MINUTES
        value: 30
      
      # 기상청 API
      - key: KMA_API_KEY
        value: kZsudkRgRWCbLnZEYMVg5Q
      - key: KMA_WEATHER_URL
        value: https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtFcst
      
      # 좌표 설정
      - key: SEOUL_NX
        value: 55
      - key: SEOUL_NY
        value: 127
      
      # 환경 설정
      - key: ENVIRONMENT
        value: production

# Render 배포 설정
version: "1"
"""
    
    try:
        with open("render_fixed.yaml", "w") as f:
            f.write(fixed_yaml)
        print("✅ render_fixed.yaml 생성 완료")
        print("🔧 pythonVersion: '3.11' 필드 추가")
        print("🔧 PYTHON_VERSION 환경 변수 제거")
        return True
    except Exception as e:
        print(f"❌ render_fixed.yaml 생성 실패: {e}")
        return False

def create_force_redeploy():
    """Force redeploy 파일 생성"""
    print("\n🔄 Force redeploy 파일 생성:")
    print("=" * 50)
    
    try:
        with open("force_redeploy.txt", "w") as f:
            f.write(f"Force redeploy for Python 3.11.8 fix - {datetime.now()}")
        print("✅ force_redeploy.txt 생성 완료")
        return True
    except Exception as e:
        print(f"❌ force_redeploy.txt 생성 실패: {e}")
        return False

if __name__ == "__main__":
    from datetime import datetime
    
    analyze_render_python_issue()
    create_fixed_render_yaml()
    create_force_redeploy()
    
    print("\n🎯 다음 단계:")
    print("=" * 50)
    print("1. render_fixed.yaml로 교체")
    print("2. force_redeploy.txt로 재배포 강제")
    print("3. Render 로그에서 Python 버전 확인")
    print("4. 성공 시 전체 기능 테스트")
