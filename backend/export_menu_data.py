from app.database import SessionLocal
from app import models
import json

def export_menu_data():
    """DB에 있는 메뉴 데이터를 추출하여 Python 파일로 만들기"""
    
    db = SessionLocal()
    
    try:
        # 1. 메뉴 데이터 조회
        print("1. 메뉴 데이터 조회 중...")
        menus = db.query(models.Menu).all()
        print(f"   ✅ 메뉴 데이터 조회 성공: {len(menus)}개 메뉴")
        
        # 2. 메뉴 데이터 구조화
        menu_data = []
        for menu in menus:
            menu_item = {
                "menu_name": menu.menu_name,
                "category": menu.category,
                "price": menu.price,
                "image_url": menu.image_url,
                "is_lunch_available": menu.is_lunch_available,
                "matching_weather": menu.matching_weather,
                "suitable_ground_size": menu.suitable_ground_size,
                "is_quick_meal": menu.is_quick_meal
            }
            menu_data.append(menu_item)
        
        # 3. Python 파일 생성
        python_content = '''# 메뉴 데이터 삽입 스크립트
# 생성 시간: 2026-02-19
# 메뉴 수: {}

from app.database import SessionLocal
from app import models

def insert_menu_data():
    """메뉴 데이터를 DB에 삽입"""
    db = SessionLocal()
    
    try:
        # 기존 데이터 삭제 (선택사항)
        print("기존 메뉴 데이터 삭제 중...")
        db.query(models.Menu).delete()
        db.commit()
        
        # 메뉴 데이터 삽입
        print("메뉴 데이터 삽입 중...")
        
'''.format(len(menu_data))
        
        # 메뉴 데이터 추가
        for i, menu in enumerate(menu_data):
            image_url = menu.get('image_url', '') or ''
            matching_weather = menu.get('matching_weather', '') or ''
            
            python_content += f'''        # 메뉴 {i+1}: {menu['menu_name']}
        menu_{i+1} = models.Menu(
            menu_name="{menu['menu_name'].replace('"', '\\"')}",
            category="{menu['category'].replace('"', '\\"')}",
            price={menu['price']},
            image_url="{image_url.replace('"', '\\"')}",
            is_lunch_available={menu['is_lunch_available']},
            matching_weather="{matching_weather.replace('"', '\\"')}",
            suitable_ground_size={menu['suitable_ground_size'] if menu['suitable_ground_size'] is not None else 'None'},
            is_quick_meal={menu['is_quick_meal']}
        )
        db.add(menu_{i+1})
        
'''
        
        python_content += '''        db.commit()
        print(f"✅ 메뉴 데이터 삽입 완료: {len(menu_data)}개 메뉴")
        
        # 삽입된 데이터 확인
        inserted_count = db.query(models.Menu).count()
        print(f"📊 DB 내 메뉴 수: {inserted_count}개")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    insert_menu_data()
'''
        
        # 4. 파일 저장
        with open("insert_menu_data.py", "w", encoding="utf-8") as f:
            f.write(python_content)
        
        print(f"   ✅ Python 파일 생성 완료: insert_menu_data.py")
        print(f"   📊 생성된 데이터: {len(menu_data)}개 메뉴")
        print(f"   📄 파일 저장 위치: {os.path.abspath('insert_menu_data.py')}")
        
        # 5. 카테고리별 통계
        print("\n📊 메뉴 통계:")
        categories = {}
        for menu in menu_data:
            cat = menu['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        for category, count in sorted(categories.items()):
            print(f"   {category}: {count}개")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    export_menu_data()
