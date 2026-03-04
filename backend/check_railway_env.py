"""
Railway 환경 변수 확인
"""
import os

def check_railway_env():
    """Railway 환경 변수 확인"""
    
    print("🔍 Railway 환경 변수 확인")
    print("=" * 50)
    
    # TiDB 관련 환경 변수
    tidb_vars = [
        "TIDB_HOST",
        "TIDB_PORT", 
        "TIDB_USER",
        "TIDB_PASSWORD",
        "TIDB_DATABASE"
    ]
    
    print("📋 TiDB 관련 환경 변수:")
    for var in tidb_vars:
        value = os.getenv(var)
        if value:
            # 비밀번호는 일부만 표시
            if "PASSWORD" in var:
                display_value = value[:4] + "*" * (len(value) - 4)
            else:
                display_value = value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ❌ {var}: 설정되지 않음")
    
    # 기타 중요 환경 변수
    other_vars = [
        "DATABASE_URL",
        "PYTHONPATH",
        "RAILWAY_ENVIRONMENT",
        "PORT"
    ]
    
    print("\n📋 기타 환경 변수:")
    for var in other_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: 설정되지 않음")
    
    # DATABASE_URL 자동 생성 확인
    if all(os.getenv(var) for var in tidb_vars):
        host = os.getenv("TIDB_HOST")
        port = os.getenv("TIDB_PORT")
        user = os.getenv("TIDB_USER")
        password = os.getenv("TIDB_PASSWORD")
        database = os.getenv("TIDB_DATABASE")
        
        generated_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"
        
        print(f"\n🔗 생성된 DATABASE_URL:")
        print(f"   {generated_url}")
        
        # 현재 DATABASE_URL과 비교
        current_url = os.getenv("DATABASE_URL")
        if current_url:
            print(f"\n📋 현재 DATABASE_URL:")
            print(f"   {current_url}")
            
            if generated_url == current_url:
                print("   ✅ DATABASE_URL 일치")
            else:
                print("   ❌ DATABASE_URL 불일치")
        else:
            print("\n   ❌ DATABASE_URL 설정되지 않음")
    
    print("\n💡 Railway 환경 변수 설정 방법:")
    print("   1. Railway 프로젝트 대시보드 접속")
    print("   2. Variables 탭 클릭")
    print("   3. New Variable 버튼 클릭")
    print("   4. 위 TiDB 환경 변수들 추가")

if __name__ == "__main__":
    check_railway_env()
