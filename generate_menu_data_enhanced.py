#!/usr/bin/env python3
import sqlite3
import hashlib
import os

def get_food_personality(m: str):
    """
    각 음식의 카테고리별로 '기준 점수(Base)'를 엄격하게 부여합니다.
    이 기준점수 위에서 해시값이 미세한 차이를 만듭니다.
    """
    # 기본값 (맵기, 짜기, 무게, 온도, 식감, 카테고리, 날씨, 기분)
    p = {"sp": 1, "sa": 2, "hv": 2.0, "tp": "Hot", "tx": "Soft", "ct": "기타", "we": "맑음", "mo": "일상"}

    # --- 1. 한국인의 소울푸드 (맵고 짠 국물류) ---
    if any(k in m for k in ["찌개", "매운탕", "육개장", "해장국", "볶음", "떡볶이", "마라"]):
        p.update({"sp": 4, "sa": 4, "hv": 3.5, "ct": "한식", "we": "비", "mo": "스트레스"})
        if "마라" in m: p["sp"] = 5; p["sa"] = 5
    
    # --- 2. 맑은 국물 / 보양식 (짜지만 맵지 않음) ---
    elif any(k in m for k in ["곰탕", "설렁탕", "갈비탕", "미역국", "칼국수", "샤브샤브"]):
        p.update({"sp": 1, "sa": 3, "hv": 4.0, "ct": "한식", "we": "흐림", "mo": "든든함"})

    # --- 3. 육류 구이 (무겁고 쫄깃함) ---
    elif any(k in m for k in ["삼겹살", "구이", "스테이크", "갈비", "족발", "보쌈"]):
        p.update({"sp": 1, "sa": 3, "hv": 4.8, "tx": "Chewy", "ct": "육류", "mo": "기력보충"})
        if "양념" in m or "불" in m: p["sp"] = 3; p["sa"] = 4

    # --- 4. 일식 / 신선식품 (차갑고 가벼움) ---
    elif any(k in m for k in ["회", "초밥", "스시", "물회", "샐러드", "포케"]):
        p.update({"sp": 1, "sa": 2, "hv": 2.0, "tp": "Cold", "ct": "일식", "we": "더움", "mo": "신선함"})
        if "회덮밥" in m or "알밥" in m: p["tp"] = "Hot"

    # --- 5. 양식 / 패스트푸드 (짜고 기름짐) ---
    elif any(k in m for k in ["피자", "버거", "파스타", "리조또", "치킨", "튀김"]):
        p.update({"sp": 1, "sa": 4, "hv": 4.0, "tx": "Crispy", "ct": "양식", "mo": "즐거움"})
        if "치킨" in m or "튀김" in m: p["tx"] = "Crispy"
        else: p["tx"] = "Chewy"

    # --- 6. 카페 / 디저트 (매우 가볍고 달콤함 - 맵기/짜기 최하) ---
    elif any(k in m for k in ["커피", "라떼", "에이드", "케이크", "빙수", "차", "라떼"]):
        p.update({"sp": 1, "sa": 1, "hv": 1.0, "tp": "Cold", "ct": "디저트", "mo": "휴식"})
        if "티" in m or "아메리카노" in m: p["hv"] = 0.5

    # --- 7. 면류 (세부 교정) ---
    if any(k in m for k in ["라면", "짬뽕", "쫄면"]):
        p.update({"sp": 4, "sa": 5, "ct": "면류"})
    elif any(k in m for k in ["짜장", "우동", "소바"]):
        p.update({"sp": 1, "sa": 3, "ct": "면류"})

    return p

def run_sync():
    db_path = "./backend/restaurant_app.db"
    list_path = "./menu_list.txt"

    if not os.path.exists(list_path): return print("파일 없음")

    with open(list_path, 'r', encoding='utf-8') as f:
        menus = [l.strip() for l in f if l.strip()]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 테이블 초기화 (테스트용으로 깔끔하게 다시 넣고 싶을 때 사용)
    # cursor.execute("DELETE FROM menu_details")
    # cursor.execute("DELETE FROM menus")

    for name in menus:
        p = get_food_personality(name)
        
        # 고유 해시로 0.1~0.3 정도의 개성 부여
        h = int(hashlib.md5(name.encode()).hexdigest(), 16)
        
        # 실제 데이터 생성 (기준점 + 미세변동)
        spicy = p["sp"]
        salt = p["sa"]
        heavy = round(p["hv"] + (h % 5) / 10, 1)
        revisit = round(0.7 + (h % 20) / 100, 2)
        wait = 10 + (h % 10)
        if p["hv"] >= 4.0: wait += 10 # 무거운 음식은 오래 걸림

        try:
            cursor.execute("""
                INSERT INTO menus (menu_name, category, is_lunch_available, is_quick_meal, matching_weather, matching_mood)
                VALUES (?, ?, 1, ?, ?, ?)
            """, (name, p["ct"], (1 if wait <= 15 else 0), p["we"], p["mo"]))
            
            m_id = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (m_id, spicy, salt, heavy, p["tp"], p["tx"], revisit, wait, round(0.1 + (h%10)/100, 2), round(3.8 + (h%12)/10, 1)))
        except:
            continue

    conn.commit()
    conn.close()
    print("🚀 초정밀 데이터 삽입 완료!")

if __name__ == "__main__":
    run_sync()