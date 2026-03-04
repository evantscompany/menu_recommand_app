"""
menu_details 테이블 작동하는 마이그레이션 스크립트
"""

import sqlite3
import pymysql

def migrate_menu_details_working():
    """menu_details 테이블 작동하는 마이그레이션"""
    
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
        
        # 데이터를 리스트로 수집
        all_data = []
        for row in cursor.fetchall():
            try:
                # 데이터를 개별적으로 처리하고 타입 변환
                data_row = {
                    'detail_id': int(row[0]) if row[0] is not None else 0,
                    'menu_id': int(row[1]) if row[1] is not None else 0,
                    'spicy_level': int(row[2]) if row[2] is not None else 0,
                    'saltiness_level': int(row[3]) if row[3] is not None else 0,
                    'heaviness': float(row[4]) if row[4] is not None else 0.0,
                    'serving_temperature': str(row[5]) if row[5] is not None else 'unknown',
                    'texture': str(row[6]) if row[6] is not None else 'unknown',
                    'revisit_rate': float(row[7]) if row[7] is not None else 0.0,
                    'avg_waiting_time': int(row[8]) if row[8] is not None else 0,
                    'ad_suspicion_index': float(row[9]) if row[9] is not None else 0.0,
                    'real_satisfaction_score': float(row[10]) if row[10] is not None else 0.0
                }
                all_data.append(data_row)
                
            except Exception as e:
                error_count += 1
                print(f"  ⚠️ 데이터 처리 실패: {e}")
                continue
        
        # executemany로 한 번에 삽입
        if all_data:
            try:
                insert_sql = """INSERT INTO menu_details (
                    detail_id, menu_id, spicy_level, saltiness_level, heaviness, 
                    serving_temperature, texture, revisit_rate, avg_waiting_time, 
                    ad_suspicion_index, real_satisfaction_score
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                
                # 데이터를 튜플 리스트로 변환
                values_list = [
                    (
                        data['detail_id'], data['menu_id'], data['spicy_level'], data['saltiness_level'], 
                        data['heaviness'], data['serving_temperature'], data['texture'], 
                        data['revisit_rate'], data['avg_waiting_time'], data['ad_suspicion_index'], 
                        data['real_satisfaction_score']
                    ) for data in all_data
                ]
                
                mysql_cursor.executemany(insert_sql, values_list)
                success_count = len(all_data)
                print(f"  executemany로 {success_count}개 레코드 삽입 시도...")
                
            except Exception as e:
                print(f"  ❌ executemany 실패: {type(e).__name__}: {e}")
                
                # 개별 삽입으로 fallback
                print("  🔄 개별 삽입으로 fallback...")
                for data in all_data:
                    try:
                        insert_sql = """INSERT INTO menu_details (
                            detail_id, menu_id, spicy_level, saltiness_level, heaviness, 
                            serving_temperature, texture, revisit_rate, avg_waiting_time, 
                            ad_suspicion_index, real_satisfaction_score
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                        
                        values = (
                            data['detail_id'], data['menu_id'], data['spicy_level'], data['saltiness_level'], 
                            data['heaviness'], data['serving_temperature'], data['texture'], 
                            data['revisit_rate'], data['avg_waiting_time'], data['ad_suspicion_index'], 
                            data['real_satisfaction_score']
                        )
                        
                        mysql_cursor.execute(insert_sql, values)
                        success_count += 1
                        
                        # 진행 상태 표시
                        if success_count % 50 == 0:
                            print(f"    진행 중: {success_count}개 레코드 처리 완료...")
                            
                    except Exception as e:
                        error_count += 1
                        print(f"    ⚠️ 개별 삽입 실패: {e}")
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
    print("🚀 menu_details 테이블 작동 마이그레이션 시작")
    print("=" * 60)
    
    if migrate_menu_details_working():
        print("\n🎉 menu_details 마이그레이션 성공 완료!")
    else:
        print("\n💥 menu_details 마이그레이션 실패!")
