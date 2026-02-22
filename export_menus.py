import sqlite3
import pandas as pd
import os

def export_menus_to_excel():
    # 데이터베이스 파일 경로
    db_path = 'restaurant_app.db'
    
    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 모든 테이블 조회
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("데이터베이스의 테이블 목록:")
    for table in tables:
        print(f"- {table[0]}")
    
    all_menus = []
    
    # 각 테이블에서 메뉴 데이터 추출
    for table in tables:
        table_name = table[0]
        try:
            # 테이블 구조 확인
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            print(f"\n{table_name} 테이블의 컬럼: {column_names}")
            
            # 데이터 조회
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            
            if rows:
                # 메뉴 이름이 포함된 컬럼 찾기
                menu_column = None
                for col in column_names:
                    if 'menu' in col.lower() or 'name' in col.lower() or '메뉴' in col:
                        menu_column = col
                        break
                
                if menu_column:
                    menu_index = column_names.index(menu_column)
                    for row in rows:
                        menu_name = row[menu_index]
                        if menu_name and menu_name.strip():
                            all_menus.append({
                                '테이블': table_name,
                                '메뉴명': menu_name.strip(),
                                '전체데이터': str(row)
                            })
                else:
                    # 메뉴 컬럼을 찾지 못한 경우, 첫 번째 컬럼을 메뉴로 가정
                    for row in rows:
                        if row[0] and str(row[0]).strip():
                            all_menus.append({
                                '테이블': table_name,
                                '메뉴명': str(row[0]).strip(),
                                '전체데이터': str(row)
                            })
            else:
                print(f"{table_name} 테이블에 데이터가 없습니다.")
                
        except Exception as e:
            print(f"{table_name} 테이블 조회 중 오류: {e}")
    
    # 중복 메뉴 제거
    unique_menus = []
    seen_menus = set()
    for menu in all_menus:
        menu_key = (menu['메뉴명'], menu['테이블'])
        if menu_key not in seen_menus:
            seen_menus.add(menu_key)
            unique_menus.append(menu)
    
    # DataFrame으로 변환
    if unique_menus:
        df = pd.DataFrame(unique_menus)
        
        # 엑셀 파일로 저장
        excel_filename = 'restaurant_menus.xlsx'
        df.to_excel(excel_filename, index=False, engine='openpyxl')
        print(f"\n총 {len(unique_menus)}개의 메뉴를 {excel_filename} 파일로 저장했습니다.")
        
        # 메뉴 목록 출력
        print("\n메뉴 목록:")
        for i, menu in enumerate(unique_menus, 1):
            print(f"{i}. [{menu['테이블']}] {menu['메뉴명']}")
    else:
        print("데이터베이스에서 메뉴를 찾을 수 없습니다.")
        
        # menu_list.txt 파일에서 메뉴 읽기
        if os.path.exists('backend/menu_list.txt'):
            print("\nmenu_list.txt 파일에서 메뉴를 읽어옵니다...")
            with open('backend/menu_list.txt', 'r', encoding='utf-8') as f:
                menus = [line.strip() for line in f.readlines() if line.strip()]
            
            menu_data = []
            for i, menu in enumerate(menus, 1):
                menu_data.append({
                    '번호': i,
                    '메뉴명': menu,
                    '분류': '미분류',
                    '출처': 'menu_list.txt'
                })
            
            df = pd.DataFrame(menu_data)
            excel_filename = 'restaurant_menus_from_list.xlsx'
            df.to_excel(excel_filename, index=False, engine='openpyxl')
            print(f"총 {len(menus)}개의 메뉴를 {excel_filename} 파일로 저장했습니다.")
    
    conn.close()

if __name__ == "__main__":
    export_menus_to_excel()
