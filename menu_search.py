import requests
import sqlite3
import time
import csv

#######################################
# 🔑 카카오 API 키 입력
#######################################
KAKAO_API_KEY = "480659fb0572b15e98bdf29897126ad7"

HEADERS = {
    "Authorization": f"KakaoAK {KAKAO_API_KEY}"
}

#######################################
# 📂 메뉴 파일 로드 (1000개 확장 가능)
#######################################
def load_menu_list():
    with open("menu_list.txt", encoding="utf-8") as f:
        menus = [line.strip() for line in f if line.strip()]
    return menus


#######################################
# 🗄️ SQLite DB 세팅
#######################################
conn = sqlite3.connect("restaurants.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu TEXT,
    name TEXT,
    address TEXT,
    category TEXT,
    x REAL,
    y REAL,
    UNIQUE(menu, name, address)
)
""")

conn.commit()


#######################################
# 🔍 DB 조회
#######################################
def get_from_db(menu):
    cursor.execute("SELECT * FROM restaurants WHERE menu=?", (menu,))
    return cursor.fetchall()


#######################################
# 💾 DB 저장
#######################################
def save_to_db(menu, places):

    for p in places:
        try:
            cursor.execute("""
            INSERT INTO restaurants
            (menu,name,address,category,x,y)
            VALUES (?,?,?,?,?,?)
            """, (
                menu,
                p["name"],
                p["address"],
                p["category"],
                p["x"],
                p["y"]
            ))
        except:
            pass

    conn.commit()


#######################################
# 🌐 카카오 API 호출
#######################################
def search_restaurants(menu, region="서울 관악구"):

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    query = f"{region} {menu}"

    all_places = []

    for page in range(1, 46):   # 최대 약 675개 (45 * 15)

        params = {
            "query": query,
            "size": 15,
            "page": page
        }

        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code != 200:
            print("API 오류:", response.status_code)
            break

        data = response.json()

        for doc in data["documents"]:

            # ⭐ 음식점(FD6)만 필터
            if doc["category_group_code"] != "FD6":
                continue

            all_places.append({
                "name": doc["place_name"],
                "address": doc["road_address_name"] or doc["address_name"],
                "category": doc["category_name"],
                "x": doc["x"],
                "y": doc["y"]
            })

        if data["meta"]["is_end"]:
            break

        time.sleep(0.3)   # API 쿨다운

    return all_places


#######################################
# 🚀 전체 메뉴 자동 수집
#######################################
def collect_all_menus():

    menus = load_menu_list()

    for idx, menu in enumerate(menus):

        print(f"\n[{idx+1}/{len(menus)}] {menu} 수집 중...")

        cached = get_from_db(menu)

        if cached:
            print(" → DB 존재 스킵")
            continue

        places = search_restaurants(menu)

        if places:
            save_to_db(menu, places)
            print(f" → {len(places)}개 저장")
        else:
            print(" → 결과 없음")


#######################################
# 📄 CSV 저장
#######################################
def export_csv():

    cursor.execute("""
    SELECT menu,name,address,category,x,y
    FROM restaurants
    """)

    rows = cursor.fetchall()

    with open("restaurants.csv", "w", newline="", encoding="utf-8-sig") as f:

        writer = csv.writer(f)
        writer.writerow(["menu","name","address","category","x","y"])
        writer.writerows(rows)

    print(f"\nCSV 저장 완료 → restaurants.csv ({len(rows)}개)")


#######################################
# ▶ 실행
#######################################
if __name__ == "__main__":

    print("===== 음식점 전용 메뉴 수집 시작 =====")

    collect_all_menus()

    print("\n===== CSV 생성 =====")
    export_csv()

    print("\n완료!")
