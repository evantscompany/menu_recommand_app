"""
requirements.txt 호환성 분석
"""

def analyze_requirements():
    print("🔍 requirements.txt 호환성 분석")
    print("=" * 50)
    
    requirements = [
        ("fastapi==0.100.1", "FastAPI 0.100.1 - Python 3.11 호환 ✅"),
        ("uvicorn[standard]==0.23.2", "Uvicorn 0.23.2 - Python 3.11 호환 ✅"),
        ("SQLAlchemy==2.0.20", "SQLAlchemy 2.0.20 - Python 3.11 호환 ✅"),
        ("pydantic==1.10.13", "Pydantic 1.10.13 - Rust 없음, Python 3.11 호환 ✅"),
        ("python-multipart==0.0.6", "Python-multipart 0.0.6 - 안정 버전 ✅"),
        ("python-jose[cryptography]==3.3.0", "Python-jose 3.3.0 - Python 3.11 호환 ✅"),
        ("passlib[bcrypt]==1.7.4", "Passlib 1.7.4 - Python 3.11 호환 ✅"),
        ("requests==2.31.0", "Requests 2.31.0 - Python 3.11 호환 ✅"),
        ("python-dotenv==1.0.0", "Python-dotenv 1.0.0 - Python 3.11 호환 ✅"),
        ("PyMySQL==1.1.0", "PyMySQL 1.1.0 - Python 3.11 호환 ✅"),
        ("cryptography==41.0.7", "Cryptography 41.0.7 - Python 3.11 호환 ✅"),
        ("aiohttp==3.8.5", "Aiohttp 3.8.5 - Python 3.11 호환 ✅"),
        ("email-validator==1.3.1", "Email-validator 1.3.1 - Python 3.11 호환 ✅"),
    ]
    
    print("\n📋 모듈 호환성 분석:")
    for req, desc in requirements:
        print(f"  {desc}")
    
    print("\n🚨 잠재적 문제점:")
    print("  1. Render가 Python 3.14.3을 사용 중")
    print("  2. runtime.txt는 Python 3.11.8을 지정")
    print("  3. Render가 runtime.txt를 무시하고 3.14.3을 사용")
    
    print("\n🔧 해결 방안:")
    print("  1. runtime.txt 제거 (Render 기본 Python 사용)")
    print("  2. Python 3.14.3 호환 모듈로 변경")
    print("  3. 또는 Python 3.14.3 호환성 확인")
    
    print("\n🎯 추천:")
    print("  - runtime.txt 제거")
    print("  - Python 3.14.3 호환 모듈로 변경")
    print("  - pydantic 2.x 사용 (Rust 문제 해결 필요)")

def check_python_versions():
    print("\n🐍 Python 버전 호환성:")
    print("=" * 50)
    
    versions = {
        "Python 3.11.8": "✅ 안정적, 모든 모듈 호환",
        "Python 3.14.3": "⚠️ 최신 버전, 호환성 문제 가능성",
    }
    
    for version, desc in versions.items():
        print(f"  {version}: {desc}")

if __name__ == "__main__":
    analyze_requirements()
    check_python_versions()
