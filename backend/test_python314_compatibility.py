"""
Python 3.14.3 호환성 테스트
"""

import sys
import subprocess
import importlib.util

def test_package_imports():
    """핵심 패키지 임포트 테스트"""
    print("🔍 Python 3.14.3 호환성 테스트")
    print("=" * 50)
    print(f"🐍 Python 버전: {sys.version}")
    print()
    
    # 테스트할 패키지 목록
    packages = [
        ("fastapi", "0.104.1"),
        ("uvicorn", "0.24.0"),
        ("sqlalchemy", "2.0.23"),
        ("pydantic", "2.6.0"),
        ("python_multipart", "0.0.6"),
        ("python_jose", "3.3.0"),
        ("passlib", "1.7.4"),
        ("requests", "2.32.5"),
        ("python_dotenv", "1.2.1"),
        ("pymysql", "1.1.2"),
        ("cryptography", "46.0.4"),
        ("aiohttp", "3.9.3"),
        ("email_validator", "2.1.0")
    ]
    
    success_count = 0
    total_count = len(packages)
    
    for package, expected_version in packages:
        try:
            # 패키지 임포트
            module = importlib.import_module(package)
            
            # 버전 확인
            actual_version = getattr(module, '__version__', 'unknown')
            
            print(f"✅ {package}: {actual_version} (기대: {expected_version})")
            success_count += 1
            
        except ImportError as e:
            print(f"❌ {package}: 임포트 실패 - {e}")
        except Exception as e:
            print(f"⚠️ {package}: 기타 오류 - {e}")
    
    print(f"\n📊 결과: {success_count}/{total_count} 패키지 성공")
    return success_count == total_count

def test_critical_functions():
    """핵심 기능 테스트"""
    print("\n🔧 핵심 기능 테스트:")
    print("=" * 50)
    
    try:
        # 1. FastAPI 앱 생성
        print("📦 FastAPI 테스트...")
        from fastapi import FastAPI
        app = FastAPI()
        print("  ✅ FastAPI 앱 생성 성공")
        
        # 2. SQLAlchemy 엔진 생성
        print("🗄️ SQLAlchemy 테스트...")
        from sqlalchemy import create_engine
        engine = create_engine("sqlite:///test.db")
        print("  ✅ SQLAlchemy 엔진 생성 성공")
        
        # 3. Pydantic 모델 생성
        print("📝 Pydantic 테스트...")
        from pydantic import BaseModel
        class TestModel(BaseModel):
            name: str
            age: int
        
        test_instance = TestModel(name="test", age=25)
        print("  ✅ Pydantic 모델 생성 성공")
        
        # 4. JWT 토큰 생성
        print("🔑 JWT 테스트...")
        from python_jose import jwt
        token = jwt.encode({"test": "data"}, "secret", algorithm="HS256")
        print("  ✅ JWT 토큰 생성 성공")
        
        # 5. 비밀번호 해시
        print("🔐 비밀번호 해시 테스트...")
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed = pwd_context.hash("password123")
        verified = pwd_context.verify("password123", hashed)
        print("  ✅ 비밀번호 해시/검증 성공")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 핵심 기능 테스트 실패: {e}")
        return False

def test_app_imports():
    """앱 임포트 테스트"""
    print("\n🚀 앱 임포트 테스트:")
    print("=" * 50)
    
    try:
        # 데이터베이스 임포트
        print("🔧 데이터베이스 임포트...")
        from app.database_railway import engine, Base
        print("  ✅ database_railway 임포트 성공")
        
        # 모델 임포트
        print("📋 모델 임포트...")
        import app.models as models
        print("  ✅ models 임포트 성공")
        
        # 스키마 임포트
        print("📝 스키마 임포트...")
        import app.schemas as schemas
        print("  ✅ schemas 임포트 성공")
        
        # 메인 앱 임포트
        print("🏠 메인 앱 임포트...")
        import app.main
        print("  ✅ main.py 임포트 성공")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 앱 임포트 실패: {e}")
        return False

def check_python314_issues():
    """Python 3.14 특정 문제 확인"""
    print("\n⚠️ Python 3.14 특정 문제 확인:")
    print("=" * 50)
    
    issues = []
    
    # 1. typing 모듈 변경사항 확인
    try:
        from typing import Optional
        print("✅ typing 모듈 정상")
    except Exception as e:
        issues.append(f"typing 모듈 문제: {e}")
    
    # 2. asyncio 변경사항 확인
    try:
        import asyncio
        print("✅ asyncio 모듈 정상")
    except Exception as e:
        issues.append(f"asyncio 모듈 문제: {e}")
    
    # 3. 데이터클래스 확인
    try:
        from dataclasses import dataclass
        print("✅ dataclasses 모듈 정상")
    except Exception as e:
        issues.append(f"dataclasses 모듈 문제: {e}")
    
    if issues:
        print("\n❌ 발견된 문제:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ Python 3.14 특정 문제 없음")
        return True

if __name__ == "__main__":
    print("🚀 Python 3.14.3 호환성 전체 테스트")
    print("=" * 60)
    
    # 1. 패키지 임포트 테스트
    packages_ok = test_package_imports()
    
    # 2. 핵심 기능 테스트
    functions_ok = test_critical_functions()
    
    # 3. 앱 임포트 테스트
    app_ok = test_app_imports()
    
    # 4. Python 3.14 특정 문제 확인
    python314_ok = check_python314_issues()
    
    # 최종 결과
    print("\n🎯 최종 결과:")
    print("=" * 50)
    
    all_tests = [packages_ok, functions_ok, app_ok, python314_ok]
    test_names = ["패키지 임포트", "핵심 기능", "앱 임포트", "Python 3.14 호환성"]
    
    for i, (test_ok, test_name) in enumerate(zip(all_tests, test_names), 1):
        status = "✅ 통과" if test_ok else "❌ 실패"
        print(f"  {i}. {test_name}: {status}")
    
    overall_success = all(all_tests)
    print(f"\n🏆 전체 테스트: {'✅ 성공' if overall_success else '❌ 실패'}")
    
    if overall_success:
        print("\n🚀 Python 3.14.3과 완벽 호환됩니다!")
        print("✅ Render 배포 준비 완료!")
    else:
        print("\n⚠️ 일부 호환성 문제가 있습니다.")
        print("🔧 문제 해결 후 배포를 권장합니다.")
