"""
전체 프로젝트 검증 스크립트
"""

import os
import sys
import importlib.util

def validate_project_structure():
    """프로젝트 구조 검증"""
    print("🔍 전체 프로젝트 검증")
    print("=" * 50)
    
    # 1. 핵심 파일 존재 확인
    print("\n📁 핵심 파일 확인:")
    core_files = [
        "app/main.py",
        "app/database_railway.py", 
        "app/models.py",
        "app/schemas.py",
        "app/crud.py",
        "requirements.txt"
    ]
    
    for file_path in core_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - 파일 없음!")
    
    # 2. API 엔드포인트 확인
    print("\n🔗 API 엔드포인트 확인:")
    api_files = [
        "app/api/endpoints/auth.py",
        "app/api/endpoints/user.py", 
        "app/api/endpoints/menu.py",
        "app/api/endpoints/recommendation.py",
        "app/api/endpoints/weather.py"
    ]
    
    for file_path in api_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - 파일 없음!")
    
    # 3. 코어 모듈 확인
    print("\n⚙️ 코어 모듈 확인:")
    core_modules = [
        "app/core/security.py",
        "app/core/weather_service.py",
        "app/core/algorithm.py"
    ]
    
    for file_path in core_modules:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - 파일 없음!")

def validate_imports():
    """임포트 문제 검증"""
    print("\n🔍 임포트 문제 검증:")
    print("=" * 50)
    
    try:
        # main.py 임포트 테스트
        print("\n📦 main.py 임포트 테스트:")
        spec = importlib.util.spec_from_file_location("main", "app/main.py")
        main_module = importlib.util.module_from_spec(spec)
        
        # 데이터베이스 임포트 테스트
        print("  🔧 데이터베이스 임포트...")
        from app.database_railway import engine, Base
        print("  ✅ database_railway 임포트 성공")
        
        # 모델 임포트 테스트  
        print("  📋 모델 임포트...")
        import app.models as models
        print("  ✅ models 임포트 성공")
        
        # 스키마 임포트 테스트
        print("  📝 스키마 임포트...")
        import app.schemas as schemas
        print("  ✅ schemas 임포트 성공")
        
    except ImportError as e:
        print(f"  ❌ 임포트 오류: {e}")
    except Exception as e:
        print(f"  ❌ 기타 오류: {e}")

def validate_database_config():
    """데이터베이스 설정 검증"""
    print("\n🗄️ 데이터베이스 설정 검증:")
    print("=" * 50)
    
    try:
        from app.database_railway import TIDB_HOST, TIDB_PORT, TIDB_USER, TIDB_PASSWORD, TIDB_DATABASE
        
        print(f"  🏠 호스트: {TIDB_HOST}")
        print(f"  🔌 포트: {TIDB_PORT}")
        print(f"  👤 사용자: {TIDB_USER}")
        print(f"  🗄️ 데이터베이스: {TIDB_DATABASE}")
        print(f"  🔐 비밀번호: {'*' * len(TIDB_PASSWORD) if TIDB_PASSWORD else 'None'}")
        
        if all([TIDB_HOST, TIDB_PORT, TIDB_USER, TIDB_DATABASE]):
            print("  ✅ 데이터베이스 설정 완료")
        else:
            print("  ❌ 데이터베이스 설정 불완료")
            
    except Exception as e:
        print(f"  ❌ 데이터베이스 설정 오류: {e}")

def validate_requirements():
    """requirements.txt 검증"""
    print("\n📦 requirements.txt 검증:")
    print("=" * 50)
    
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read().strip().split("\n")
        
        print(f"  📋 총 {len(requirements)}개 패키지:")
        
        critical_packages = ["fastapi", "uvicorn", "sqlalchemy", "pydantic", "python-jose"]
        
        for req in requirements:
            if req.startswith("#") or not req.strip():
                continue
                
            package = req.split("==")[0]
            version = req.split("==")[1] if "==" in req else "latest"
            
            status = "🔑" if package in critical_packages else "📦"
            print(f"  {status} {package}=={version}")
        
        print("  ✅ requirements.txt 검증 완료")
        
    except Exception as e:
        print(f"  ❌ requirements.txt 오류: {e}")

def check_potential_issues():
    """잠재적 문제 확인"""
    print("\n⚠️ 잠재적 문제 확인:")
    print("=" * 50)
    
    issues = []
    
    # 1. Python 버전 호환성
    if os.path.exists("runtime.txt"):
        with open("runtime.txt", "r") as f:
            python_version = f.read().strip()
        print(f"  🐍 Python 버전: {python_version}")
        issues.append("runtime.txt가 존재하지만 Render가 무시할 수 있음")
    else:
        print("  🐍 Python 버전: Render 기본 (3.14.3)")
        issues.append("Python 3.14.3 호환성 확인 필요")
    
    # 2. 환경 변수
    env_files = [".env", ".env.example"]
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"  🔧 환경 변수 파일: {env_file}")
    
    # 3. 데이터베이스 연결 문자열
    try:
        from app.database_railway import SQLALCHEMY_DATABASE_URL
        if "password" in SQLALCHEMY_DATABASE_URL.lower():
            issues.append("데이터베이스 연결 문자열에 비밀번호 포함")
    except:
        pass
    
    if issues:
        print("\n  🚨 발견된 문제:")
        for i, issue in enumerate(issues, 1):
            print(f"    {i}. {issue}")
    else:
        print("  ✅ 잠재적 문제 없음")

if __name__ == "__main__":
    validate_project_structure()
    validate_imports()
    validate_database_config()
    validate_requirements()
    check_potential_issues()
    
    print("\n🎯 전체 검증 완료!")
    print("=" * 50)
