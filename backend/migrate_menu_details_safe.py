"""
menu_details 테이블 안전한 마이그레이션 스크립트
"""

import sqlite3
import pymysql

def safe_value(value, default=0, value_type=str):
    """안전한 값 변환"""
    if value is None:
        return default
    try:
        if value_type == int:
            return int(value)
        elif value_type == float:
            return float(value)
        elif value_type == str:
            return str(value)
        else:
            return value
    except (ValueError, TypeError):
        return default

def migrate_menu_details_safe():
    """menu_details 테이블 안전한 마이그레이션"""
    
    # 1. SQLite 연결
    try:
        sqlite_conn = sqlite3.connect('restaurant_app.db')
        sqlite_conn.row_factory = sqlite3.Row
        print("✅ SQLite 데이터베이스 연결 성공")
    except Exception as e:
        print(f"❌ SQLite 연결 실패: {e}")
        return False
    
    # 2. MySQL 연결
    try:
        mysql_conn = pymysql.connect(
            host="gateway01.ap-northeast-1.prod.aws.tidbcloud.com",
            port=4000,
            user="3bJdto8FKWk47Fu.root",
            password="NWOZOcYDO8W5nMk2",
            database="test",
            ssl={"ssl": True},
            charset='utf8mb4'
        )
        mysql_cursor = mysql_conn.cursor()
        print("✅ TiDB Cloud MySQL 연결 성공")
    except Exception as e:
        print(f"❌ MySQL 연결 실패: {e}")
        return False
    
    try:
        # 3. menu_details 데이터 조회 및 마이그레이션
        print("\n🍽️ menu_details 테이블 마이그레이션 중...")
        cursor = sqlite_conn.execute("SELECT * FROM menu_details ORDER BY detail_id")
        
        success_count = 0
        error_count = 0
        
        for row in cursor.fetchall():
            try:
                # 안전한 데이터 변환
                detail_id = safe_value(row['detail_id'], 0, int)
                menu_id = safe_value(row['menu_id'], 0, int)
                spicy_level = safe_value(row['spicy_level'], 0, int)
                saltiness_level = safe_value(row['saltiness_level'], 0, int)
                heaviness = safe_value(row['heaviness'], 0.0, float)
                serving_temperature = safe_value(row['serving_temperature'], 'unknown', str)
                texture = safe_value(row['texture'], 'unknown', str)
                revisit_rate = safe_value(row['revisit_rate'], 0.0, float)
                avg_waiting_time = safe_value(row['avg_waiting_time'], 0, int)
                ad_suspicion_index = safe_value(row['ad_suspicion_index'], 0.0, float)
                real_satisfaction_score = safe_value(row['real_satisfaction_score'], 0.0, float)
                
                # 개별 INSERT 문 실행 (문자열 포맷팅 피하기)
                insert_sql = """INSERT INTO menu_details (
                    detail_id, menu_id, spicy_level, saltiness_level, heaviness, 
                    serving_temperature, texture, revisit_rate, avg_waiting_time, 
                    ad_suspicion_index, real_satisfaction_score
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                
                values = (
                    detail_id, menu_id, spicy_level, saltiness_level, heaviness,
                    serving_temperature, texture, revisit_rate, avg_waiting_time,
                    ad_suspicion_index, real_satisfaction_score
                )
                
                mysql_cursor.execute(insert_sql, values)
                success_count += 1
                
                # 진행 상태 표시
                if success_count % 50 == 0:
                    print(f"  진행 중: {success_count}개 레코드 처리 완료...")
                    
            except Exception as e:
                error_count += 1
                detail_id = safe_value(row['detail_id'], 'unknown', str)
                print(f"  ⚠️ 레코드 {detail_id} 삽입 실패: {e}")
                continue
        
        # 변경사항 커밋
        mysql_conn.commit()
        
        print(f"\n✅ menu_details 마이그레이션 완료!")
        print(f"  성공: {success_count}개 레코드")
        print(f"  실패: {error_count}개 레코드")
        
        # 4. 결과 확인
        try:
            mysql_cursor.execute("SELECT COUNT(*) FROM menu_details")
            final_count = mysql_cursor.fetchone()[0]
            print(f"  TiDB Cloud 최종 레코드 수: {final_count}개")
            
            if final_count > 0:
                print("  🎉 menu_details 마이그레이션 성공!")
            else:
                print("  ⚠️ menu_details 마이그레이션 실패")
                
        except Exception as e:
            print(f"  결과 확인 실패: {e}")
        
    except Exception as e:
        print(f"❌ 마이그레이션 중 오류 발생: {e}")
        mysql_conn.rollback()
        return False
    
    finally:
        sqlite_conn.close()
        mysql_conn.close()
    
    return True

if __name__ == "__main__":
    print("🚀 menu_details 테이블 안전한 마이그레이션 시작")
    print("=" * 60)
    
    if migrate_menu_details_safe():
        print("\n🎉 menu_details 마이그레이션 성공 완료!")
    else:
        print("\n💥 menu_details 마이그레이션 실패!")
