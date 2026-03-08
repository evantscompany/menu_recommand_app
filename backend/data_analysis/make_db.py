import sqlite3
import pandas as pd
import os

# 1. 파일 이름 및 경로 설정
# 현재 폴더(data_analysis)에 있는 엑셀 파일
excel_file = '카테고리_재분류_최종.xlsx'
# 한 단계 위(backend) 폴더에 있는 진짜 DB 파일
db_file = '../restaurant_app.db' 

try:
    # 2. 엑셀 파일 읽기
    print(f"🔄 {excel_file} 파일을 읽어오는 중입니다...")
    df = pd.read_excel(excel_file)

    # 3. DB 연결
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 4. 기존 테이블 삭제 (구조를 새로 잡기 위해 필요합니다)
    print("🧹 기존 restaurants 테이블을 정리하고 새로 생성합니다...")
    cursor.execute("DROP TABLE IF EXISTS restaurants")

    # 5. 새로운 구조로 테이블 생성 (distance, walking_time 포함)
    create_table_query = """
    CREATE TABLE restaurants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        latitude REAL,
        longitude REAL,
        category_1 TEXT,
        category_2 TEXT,
        distance INTEGER,
        walking_time INTEGER
    )
    """
    cursor.execute(create_table_query)

    # 6. 데이터프레임에서 필요한 컬럼만 추출하여 DB에 삽입
    # 엑셀에 있는 컬럼명과 정확히 일치해야 합니다.
    target_columns = [
        'name', 'address', 'latitude', 'longitude', 
        'category_1', 'category_2', 'distance', 'walking_time'
    ]
    
    df_to_db = df[target_columns]
    
    # if_exists='append'를 사용해야 위에서 만든 id(Auto Increment)가 정상 작동합니다.
    df_to_db.to_sql('restaurants', conn, if_exists='append', index=False)

    # 7. 변경사항 저장 및 종료
    conn.commit()
    conn.close()

    # 절대 경로로 어디 저장됐는지 친절하게 알려주기
    abs_path = os.path.abspath(db_file)
    print(f"\n✨ 모든 작업이 성공적으로 완료되었습니다!")
    print(f"📍 위치: {abs_path}")
    print(f"📊 포함된 정보: 이름, 주소, 좌표, 카테고리, 거리, 도보시간")

except FileNotFoundError:
    print(f"❌ 에러: {excel_file} 파일을 찾을 수 없습니다. 파일이 data_analysis 폴더 안에 있는지 확인해주세요.")
except Exception as e:
    print(f"❌ 예기치 못한 에러 발생: {e}")