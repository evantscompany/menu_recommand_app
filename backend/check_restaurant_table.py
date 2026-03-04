"""
Restaurant 테이블 확인
"""
import os
import sys
sys.path.append('.')

from app.database_mysql import engine, SessionLocal
from app import models
from sqlalchemy import text

def check_restaurant_table():
    """Restaurant 테이블 확인"""
    
    print("🏪 Restaurant 테이블 확인")
    print("=" * 40)
    
    try:
        # 1. 테이블 존재 확인
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES LIKE 'restaurants'"))
            tables = result.fetchall()
            
            if len(tables) > 0:
                print("✅ restaurants 테이블 존재")
                
                # 테이블 구조 확인
                result = conn.execute(text("DESCRIBE restaurants"))
                columns = result.fetchall()
                print(f"   컬럼 수: {len(columns)}")
                for col in columns:
                    print(f"   - {col[0]}: {col[1]}")
                
                # 데이터 개수 확인
                result = conn.execute(text("SELECT COUNT(*) FROM restaurants"))
                count = result.fetchone()[0]
                print(f"   데이터 개수: {count}개")
                
                if count > 0:
                    # 샘플 데이터 확인
                    result = conn.execute(text("SELECT * FROM restaurants LIMIT 3"))
                    rows = result.fetchall()
                    print("   샘플 데이터:")
                    for row in rows:
                        print(f"   - {row}")
                        
            else:
                print("❌ restaurants 테이블 없음")
                
                # 모든 테이블 목록 확인
                result = conn.execute(text("SHOW TABLES"))
                all_tables = result.fetchall()
                print(f"   전체 테이블: {[t[0] for t in all_tables]}")
        
        # 2. 모델 확인
        print(f"\n🔍 모델 확인:")
        if hasattr(models, 'Restaurant'):
            print("✅ Restaurant 모델 존재")
            
            # 모델 속성 확인
            restaurant_model = models.Restaurant
            print(f"   테이블명: {restaurant_model.__tablename__}")
            print(f"   컬럼: {[col.name for col in restaurant_model.__table__.columns]}")
            
        else:
            print("❌ Restaurant 모델 없음")
            
            # 모든 모델 확인
            all_models = [name for name in dir(models) if not name.startswith('_')]
            print(f"   전체 모델: {all_models}")
        
        # 3. DB 세션 테스트
        print(f"\n🗄️ DB 세션 테스트:")
        db = SessionLocal()
        
        try:
            # Restaurant 조회 시도
            restaurants = db.query(models.Restaurant).all()
            print(f"✅ Restaurant 조회 성공: {len(restaurants)}개")
            
        except Exception as e:
            print(f"❌ Restaurant 조회 실패: {e}")
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ 전체 확인 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_restaurant_table()
