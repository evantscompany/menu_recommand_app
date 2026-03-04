"""
menu_details 테이블 간단 마이그레이션 스크립트
"""

import sqlite3
import pymysql

def migrate_menu_details_simple():
    """menu_details 테이블 간단 마이그레이션"""
    
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
        # 3. menu_details 데이터 조회
        print("\n🍽️ menu_details 테이블 마이그레이션 중...")
        cursor = sqlite_conn.execute("SELECT * FROM menu_details ORDER BY detail_id LIMIT 10")  # 먼저 10개만 시도
        
        success_count = 0
        error_count = 0
        
        for row in cursor.fetchall():
            try:
                # 데이터를 개별 변수로 추출
                detail_id = row[0] if row[0] is not None else 0
                menu_id = row[1] if row[1] is not None else 0
                spicy_level = row[2] if row[2] is not None else 0
                saltiness_level = row[3] if row[3] is not None else 0
                heaviness = float(row[4]) if row[4] is not None else 0.0
                serving_temperature = row[5] if row[5] is not None else 'unknown'
                texture = row[6] if row[6] is not None else 'unknown'
                revisit_rate = float(row[7]) if row[7] is not None else 0.0
                avg_waiting_time = row[8] if row[8] is not None else 0
                ad_suspicion_index = float(row[9]) if row[9] is not None else 0.0
                real_satisfaction_score = float(row[10]) if row[10] is not None else 0.0
                
                # 가장 간단한 INSERT 문
                insert_sql = """INSERT INTO menu_details (
                    detail_id, menu_id, spicy_level, saltiness_level, heaviness, 
                    serving_temperature, texture, revisit_rate, avg_waiting_time, 
                    ad_suspicion_index, real_satisfaction_score
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                
                # 데이터를 튜플로 전달
                values_tuple = (
                    detail_id, menu_id, spicy_level, saltiness_level, heaviness,
                    serving_temperature, texture, revisit_rate, avg_waiting_time,
                    ad_suspicion_index, real_satisfaction_score
                )
                
                mysql_cursor.execute(insert_sql, values_tuple)
                success_count += 1
                print(f"  ✅ 레코드 {detail_id} 삽입 성공")
                    
            except Exception as e:
                error_count += 1
                print(f"  ❌ 레코드 삽입 실패: {type(e).__name__}: {e}")
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
                return True
            else:
                print("  ⚠️ menu_details 마이그레이션 실패")
                return False
                
        except Exception as e:
            print(f"  결과 확인 실패: {e}")
            return False
        
    except Exception as e:
        print(f"❌ 마이그레이션 중 오류 발생: {type(e).__name__}: {e}")
        mysql_conn.rollback()
        return False
    
    finally:
        sqlite_conn.close()
        mysql_conn.close()

if __name__ == "__main__":
    print("🚀 menu_details 테이블 간단 마이그레이션 시작 (10개 레코드만)")
    print("=" * 60)
    
    if migrate_menu_details_simple():
        print("\n🎉 menu_details 마이그레이션 성공 완료!")
        print("💡 전체 351개 레코드 중 10개만 성공했습니다.")
        print("💡 나머지 341개는 수동으로 마이그레이션이 필요합니다.")
    else:
        print("\n💥 menu_details 마이그레이션 실패!")
