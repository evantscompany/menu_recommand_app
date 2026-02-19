import requests
import json
import os

# 메뉴 DB 데이터 생성 스크립트
def create_menu_db_script():
    """메뉴 DB에 데이터를 넣는 스크립트 생성"""
    
    # API 엔드포인트
    base_url = "http://localhost:8000"
    
    # 1. 로그인하여 토큰 발급
    print("1. 로그인 중...")
    login_response = requests.post(f"{base_url}/api/auth/login", 
                              data={"username": "aaa", "password": "password123"})
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        token = token_data.get("access_token")
        print("   ✅ 로그인 성공")
        
        # 2. 메뉴 목록 조회
        print("2. 메뉴 목록 조회 중...")
        menu_response = requests.get(f"{base_url}/api/menus", 
                               headers={"Authorization": f"Bearer {token}"})
        
        if menu_response.status_code == 200:
            menu_data = menu_response.json()
            menus = menu_data if isinstance(menu_data, list) else []
            print(f"   메뉴 목록 조회 성공: {len(menus)}개 메뉴")
            
            # 3. 메뉴 DB에 넣을 데이터 생성
            menu_data = []
            for i, menu in enumerate(menus, 1):
                menu_item = {
                    "menu_name": menu["menu_name"],
                    "category": menu["category"],
                    "price": menu["price"],
                    "image_url": menu.get("image_url", ""),
                    "is_lunch_available": menu.get("is_lunch_available", True),
                    "matching_weather": menu.get("matching_weather", ""),
                    "suitable_ground_size": menu.get("suitable_ground_size", None),
                    "is_quick_meal": menu.get("is_quick_meal", True)
                }
                menu_data.append(menu_item)
            
            # 4. SQL 파일 생성
            sql_content = "-- 메뉴 데이터 삽입 스크립트\n"
            sql_content += "-- 생성 시간: 2026-02-19\n\n"
            sql_content += "-- 메뉴 수: {}\n\n".format(len(menu_data))
            
            for i, menu in enumerate(menu_data):
                sql_content += "-- 메뉴 {}: {}\n".format(i+1, menu["menu_name"])
                sql_content += "INSERT INTO menus (menu_name, category, price, image_url, is_lunch_available, matching_weather, suitable_ground_size, is_quick_meal) VALUES ('{}', '{}', {}, '{}', '{}', '{}', '{}', '{}');\n".format(
                    menu["menu_name"].replace("'", "''"),  # 작은따옴표 처리
                    menu["category"].replace("'", "''"),
                    str(menu["price"]),
                    menu.get("image_url", "").replace("'", "''") if menu.get("image_url") else "''",
                    str(menu.get("is_lunch_available", True)),
                    str(menu.get("matching_weather", "")).replace("'", "''") if menu.get("matching_weather") else "''",
                    str(menu.get("suitable_ground_size", "None")).replace("'", "''") if menu.get("suitable_ground_size") else "''",
                    str(menu.get("is_quick_meal", True))
                )
            
            sql_content += "\n-- 인덱스 생성\n"
            sql_content += "CREATE INDEX idx_menus_category ON menus(category);\n"
            sql_content += "CREATE INDEX idx_menus_name ON menus(menu_name);\n"
            sql_content += "CREATE INDEX idx_menus_price ON menus(price);\n"
            
            # 5. 파일 저장
            with open("insert_menus.sql", "w", encoding="utf-8") as f:
                f.write(sql_content)
            
            print(f"   ✅ SQL 파일 생성 완료: insert_menus.sql")
            print(f"   📊 생성된 SQL: {len(menu_data)}개 메뉴 데이터")
            print(f"   📄 파일 저장 위치: {os.path.abspath('insert_menus.sql')}")
            
        else:
            print(f"   ❌ 메뉴 목록 조회 실패: {menu_response.status_code}")
            print(f"   응답 내용: {menu_response.text}")
            
    else:
        print("   ❌ 로그인 실패")
        print(f"   상태 코드: {login_response.status_code}")
        print(f"   응답 내용: {login_response.text}")

if __name__ == "__main__":
    create_menu_db_script()
