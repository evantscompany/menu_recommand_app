"""
Render 배포된 서버용 데이터 마이그레이션 스크립트
"""
import os
import sqlite3
import pymysql
from datetime import datetime

def migrate_data_for_render():
    """Render 배포 서버용 데이터 마이그레이션"""
    
    print("🚀 Render 배포 서버 데이터 마이그레이션 시작")
    print("=" * 60)
    
    # 1. SQLite 연결 (로컬 데이터)
    try:
        sqlite_conn = sqlite3.connect('restaurant_app.db')
        sqlite_conn.row_factory = sqlite3.Row
        print("✅ SQLite 데이터베이스 연결 성공")
    except Exception as e:
        print(f"❌ SQLite 연결 실패: {e}")
        return False
    
    # 2. TiDB Cloud 연결 (환경변수 사용)
    try:
        mysql_conn = pymysql.connect(
            host=os.getenv("TIDB_HOST", "gateway01.ap-northeast-1.prod.aws.tidbcloud.com"),
            port=int(os.getenv("TIDB_PORT", "4000")),
            user=os.getenv("TIDB_USER", "3bJdto8FKWk47Fu.root"),
            password=os.getenv("TIDB_PASSWORD", "NWOZOcYDO8W5nMk2"),
            database=os.getenv("TIDB_DATABASE", "test"),
            ssl={"ssl": True},
            charset='utf8mb4'
        )
        mysql_cursor = mysql_conn.cursor()
        print("✅ TiDB Cloud MySQL 연결 성공")
    except Exception as e:
        print(f"❌ TiDB Cloud 연결 실패: {e}")
        print("🔍 환경변수 설정 확인 필요")
        return False
    
    try:
        # 3. 데이터 마이그레이션
        tables_data = {
            'user_accounts': [
                'username', 'email', 'nickname', 'hashed_password', 'created_at'
            ],
            'menus': [
                'menu_name', 'category', 'image_url', 'price', 'matching_weather',
                'suitable_ground_size', 'is_quick_meal', 'is_lunch_available'
            ],
            'user_profiles': [
                'user_id', 'dietary_label', 'allergies', 'spicy_threshold',
                'saltiness_preference', 'lunch_budget_max', 'is_adventurous'
            ],
            'menu_details': [
                'detail_id', 'menu_id', 'spicy_level', 'saltiness_level', 'heaviness',
                'serving_temperature', 'texture', 'revisit_rate', 'avg_waiting_time',
                'ad_suspicion_index', 'real_satisfaction_score'
            ]
        }
        
        total_migrated = 0
        
        for table_name, columns in tables_data.items():
            print(f"\n📋 {table_name} 테이블 마이그레이션 중...")
            
            # SQLite 데이터 조회
            cursor = sqlite_conn.execute(f"SELECT {', '.join(columns)} FROM {table_name}")
            rows = cursor.fetchall()
            
            if not rows:
                print(f"   ⚠️ {table_name}에 데이터가 없습니다")
                continue
            
            # MySQL에 데이터 삽입
            success_count = 0
            error_count = 0
            
            for row in rows:
                try:
                    # 데이터 처리
                    values = []
                    for col in columns:
                        value = row[col]
                        if value is None:
                            values.append('NULL')
                        elif isinstance(value, str):
                            values.append(f"'{value}'")
                        elif isinstance(value, bool):
                            values.append('1' if value else '0')
                        else:
                            values.append(str(value))
                    
                    # INSERT 문 생성
                    insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)})"
                    
                    mysql_cursor.execute(insert_sql)
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    continue
            
            print(f"   ✅ 성공: {success_count}개, ❌ 실패: {error_count}개")
            total_migrated += success_count
        
        # 4. 변경사항 커밋
        mysql_conn.commit()
        print(f"\n✅ 데이터 마이그레이션 완료!")
        print(f"   총 {total_migrated}개 레코드 마이그레이션됨")
        
        # 5. 결과 확인
        print(f"\n📊 마이그레이션 결과 확인:")
        for table_name in tables_data.keys():
            try:
                mysql_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = mysql_cursor.fetchone()[0]
                print(f"   {table_name}: {count}개 레코드")
            except Exception as e:
                print(f"   {table_name}: 확인 실패 - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 마이그레이션 중 오류 발생: {e}")
        mysql_conn.rollback()
        return False
    
    finally:
        sqlite_conn.close()
        mysql_conn.close()

if __name__ == "__main__":
    if migrate_data_for_render():
        print("\n🎉 데이터 마이그레이션 성공!")
        print("🌐 Render 서버에서 데이터를 확인하세요.")
    else:
        print("\n💥 데이터 마이그레이션 실패!")
