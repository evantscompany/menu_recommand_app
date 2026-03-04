"""
menu_details 테이블 전용 마이그레이션 스크립트
"""

import sqlite3
import pymysql

def migrate_menu_details_only():
    """menu_details 테이블만 마이그레이션"""
    
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
        cursor = sqlite_conn.execute("SELECT * FROM menu_details")
        
        success_count = 0
        error_count = 0
        
        for row in cursor.fetchall():
            try:
                # 데이터 처리 및 NULL 값 확인
                detail_id = row['detail_id'] if row['detail_id'] is not None else 0
                menu_id = row['menu_id'] if row['menu_id'] is not None else 0
                spicy_level = row['spicy_level'] if row['spicy_level'] is not None else 0
                saltiness_level = row['saltiness_level'] if row['saltiness_level'] is not None else 0
                heaviness = float(row['heaviness']) if row['heaviness'] is not None else 0.0
                serving_temperature = row['serving_temperature'] if row['serving_temperature'] is not None else 'unknown'
                texture = row['texture'] if row['texture'] is not None else 'unknown'
                revisit_rate = float(row['revisit_rate']) if row['revisit_rate'] is not None else 0.0
                avg_waiting_time = row['avg_waiting_time'] if row['avg_waiting_time'] is not None else 0
                ad_suspicion_index = float(row['ad_suspicion_index']) if row['ad_suspicion_index'] is not None else 0.0
                real_satisfaction_score = float(row['real_satisfaction_score']) if row['real_satisfaction_score'] is not None else 0.0
                
                # INSERT 문 실행
                insert_sql = """
                    INSERT INTO menu_details (
                        detail_id, menu_id, spicy_level, saltiness_level, heaviness, 
                        serving_temperature, texture, revisit_rate, avg_waiting_time, 
                        ad_suspicion_index, real_satisfaction_score
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                mysql_cursor.execute(insert_sql, (
                    detail_id, menu_id, spicy_level, saltiness_level, heaviness,
                    serving_temperature, texture, revisit_rate, avg_waiting_time,
                    ad_suspicion_index, real_satisfaction_score
                ))
                
                success_count += 1
                
                # 진행 상태 표시
                if success_count % 50 == 0:
                    print(f"  진행 중: {success_count}개 레코드 처리 완료...")
                    
            except Exception as e:
                error_count += 1
                detail_id = row['detail_id'] if 'detail_id' in row.keys() else 'unknown'
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
    print("🚀 menu_details 테이블 마이그레이션 시작")
    print("=" * 50)
    
    if migrate_menu_details_only():
        print("\n🎉 menu_details 마이그레이션 성공 완료!")
    else:
        print("\n💥 menu_details 마이그레이션 실패!")
