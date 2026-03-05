-- TiDB Cloud 데이터베이스 초기화 스크립트
-- menu_data_for_frontend_20260223_153903.sql 기반
-- 총 메뉴 수: 351, 총 상세 정보 수: 351

-- 기존 데이터 삭제 (초기화)
DELETE FROM menu_details;
DELETE FROM menus;
DELETE FROM recommendation_feedback;
DELETE FROM user_history;
DELETE FROM user_profiles;
DELETE FROM user_accounts;

-- 테이블 생성
CREATE TABLE IF NOT EXISTS menus (
    menu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    image_url VARCHAR(500),
    price INTEGER DEFAULT 8000,
    matching_weather VARCHAR(100),
    suitable_ground_size INTEGER,
    is_quick_meal BOOLEAN DEFAULT 1,
    is_lunch_available BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS menu_details (
    detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_id INTEGER NOT NULL,
    spicy_level INTEGER DEFAULT 1,
    saltiness_level INTEGER DEFAULT 3,
    heaviness REAL DEFAULT 0.5,
    serving_temperature VARCHAR(50) DEFAULT 'hot',
    texture VARCHAR(50) DEFAULT 'normal',
    revisit_rate REAL DEFAULT 0.8,
    avg_waiting_time INTEGER DEFAULT 15,
    ad_suspicion_index REAL DEFAULT 0.1,
    real_satisfaction_score REAL DEFAULT 4.0,
    FOREIGN KEY (menu_id) REFERENCES menus (menu_id)
);

-- 메뉴 데이터 삽입
INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (1, '김치찌개', '한식', '', 11000, 'Cold,Rainy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (2, '된장찌개', '한식', '', 11000, 'Cold,Rainy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (3, '순두부찌개', '한식', '', 11000, 'Cold,Rainy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (4, '부대찌개', '한식', '', 11000, 'Cold,Rainy,Snowy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (5, '청국장', '한식', '', 11000, 'Cold,Rainy,Snowy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (6, '동태찌개', '한식', '', 11000, 'Cold,Rainy,Snowy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (7, '알탕', '한식', '', 11000, 'Cold,Rainy,Snowy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (8, '대구탕', '한식', '', 11000, 'Cold,Rainy,Snowy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (9, '매운탕', '한식', '', 11000, 'Cold,Rainy,Snowy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (10, '해물탕', '한식', '', 11000, 'Cold,Rainy,Snowy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (11, '추어탕', '한식', '', 11000, 'Cold,Rainy,Snowy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (12, '육개장', '한식', '', 11000, 'Cold,Rainy,Snowy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (13, '설렁탕', '한식', '', 11000, 'Cold,Rainy,Snowy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (14, '곰탕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (15, '갈비탕', '한식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (16, '삼계탕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (17, '닭곰탕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (18, '닭개장', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (19, '우거지탕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (20, '감자탕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (21, '뼈해장국', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (22, '선지해장국', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (23, '콩나물국밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (24, '황태국', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (25, '북어국', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (26, '미역국', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (27, '시래기국', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (28, '순대국', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (29, '돼지국밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (30, '소머리국밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (31, '굴국밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (32, '따로국밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (33, '수육국밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (34, '내장탕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (35, '도가니탕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (36, '꼬리곰탕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (37, '양평해장국', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (38, '장터국밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (39, '삼겹살', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (40, '목살', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (41, '항정살', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (42, '갈매기살', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (43, '가브리살', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (44, '돼지갈비', '한식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (45, '소갈비', '한식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (46, 'LA갈비', '한식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (47, '양념갈비', '한식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (48, '불고기', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (49, '언양불고기', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (50, '산더미불고기', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (51, '제육볶음', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (52, '오삼불고기', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (53, '낙지볶음', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (54, '쭈꾸미볶음', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (55, '닭갈비', '한식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (56, '닭볶음탕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (57, '닭강정', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (58, '닭발', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (59, '닭똥집', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (60, '간장치킨', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (61, '양념치킨', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (62, '후라이드치킨', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (63, '마늘치킨', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (64, '순살치킨', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (65, '숯불치킨', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (66, '파닭', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (67, '간장새우', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (68, '양념새우', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (69, '새우튀김', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (70, '대하구이', '구이', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (71, '장어구이', '구이', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (72, '고등어구이', '구이', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (73, '삼치구이', '구이', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (74, '갈치구이', '구이', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (75, '조기구이', '구이', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (76, '꽁치구이', '구이', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (77, '임연수구이', '구이', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (78, '굴비구이', '구이', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (79, '생선조림', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (80, '고등어조림', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (81, '갈치조림', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (82, '코다리조림', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (83, '꽁치조림', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (84, '닭백숙', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (85, '오리백숙', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (86, '오리주물럭', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (87, '오리훈제', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (88, '보쌈', '한식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (89, '족발', '한식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (90, '불족발', '한식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (91, '마늘족발', '한식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (92, '냉채족발', '한식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (93, '막국수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (94, '물막국수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (95, '비빔막국수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (96, '냉면', '면', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (97, '물냉면', '면', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (98, '비빔냉면', '면', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (99, '회냉면', '면', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (100, '밀면', '면', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (101, '칼국수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (102, '들깨칼국수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (103, '바지락칼국수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (104, '손칼국수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (105, '잔치국수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (106, '비빔국수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (107, '열무국수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (108, '콩국수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (109, '쫄면', '면', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (110, '라면', '면', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (111, '해물라면', '면', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (112, '김치라면', '면', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (113, '짜장라면', '면', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (114, '짜장면', '면', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (115, '간짜장', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (116, '삼선짜장', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (117, '짬뽕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (118, '삼선짬뽕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (119, '백짬뽕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (120, '볶음짬뽕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (121, '탕수육', '한식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (122, '깐풍육', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (123, '깐풍기', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (124, '유린기', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (125, '팔보채', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (126, '양장피', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (127, '고추잡채', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (128, '마파두부', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (129, '마라탕', '중식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (130, '마라샹궈', '중식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (131, '마라룽샤', '중식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (132, '훠궈', '한식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (133, '양꼬치', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (134, '양갈비', '한식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (135, '중국식볶음밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (136, '게살볶음밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (137, '새우볶음밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (138, '잡채밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (139, '잡탕밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (140, '짬뽕밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (141, '짜장밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (142, '덮밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (143, '김치볶음밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (144, '낙지덮밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (145, '제육덮밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (146, '오징어덮밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (147, '돈부리', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (148, '규동', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (149, '가츠동', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (150, '텐동', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (151, '사케동', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (152, '에비동', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (153, '카츠카레', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (154, '카레라이스', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (155, '일본식카레', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (156, '수프카레', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (157, '초밥', '일식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (158, '모둠초밥', '일식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (159, '회', '일식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (160, '광어회', '일식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (161, '우럭회', '일식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (162, '연어회', '일식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (163, '참치회', '일식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (164, '방어회', '일식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (165, '농어회', '일식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (166, '도미회', '일식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (167, '물회', '일식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (168, '회덮밥', '일식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (169, '알밥', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (170, '우동', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (171, '냄비우동', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (172, '냉우동', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (173, '어묵우동', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (174, '야키우동', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (175, '소바', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (176, '모밀', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (177, '판모밀', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (178, '냉모밀', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (179, '메밀국수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (180, '라멘', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (181, '돈코츠라멘', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (182, '미소라멘', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (183, '쇼유라멘', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (184, '탄탄멘', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (185, '츠케멘', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (186, '스시롤', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (187, '돈까스', '일식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (188, '치즈돈까스', '일식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (189, '고구마돈까스', '일식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (190, '생선까스', '일식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (191, '치킨까스', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (192, '함박스테이크', '양식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (193, '스테이크', '양식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (194, '토마호크스테이크', '양식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (195, '티본스테이크', '양식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (196, '채끝스테이크', '양식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (197, '안심스테이크', '양식', '', 35000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (198, '립아이', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (199, '파스타', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (200, '크림파스타', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (201, '토마토파스타', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (202, '오일파스타', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (203, '해물파스타', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (204, '봉골레파스타', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (205, '알리오올리오', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (206, '까르보나라', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (207, '라자냐', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (208, '리조또', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (209, '해물리조또', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (210, '버섯리조또', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (211, '트러플리조또', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (212, '피자', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (213, '페퍼로니피자', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (214, '고르곤졸라피자', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (215, '콤비네이션피자', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (216, '불고기피자', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (217, '하와이안피자', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (218, '마르게리타피자', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (219, '치즈피자', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (220, '포카치아', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (221, '브루스케타', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (222, '샌드위치', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (223, '클럽샌드위치', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (224, 'BLT샌드위치', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (225, '치아바타샌드위치', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (226, '파니니', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (227, '햄버거', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (228, '치즈버거', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (229, '불고기버거', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (230, '치킨버거', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (231, '새우버거', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (232, '수제버거', '양식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (233, '핫도그', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (234, '콘도그', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (235, '토스트', '한식', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (236, '계란토스트', '한식', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (237, '프렌치토스트', '한식', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (238, '김밥', '한식', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (239, '참치김밥', '한식', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (240, '치즈김밥', '한식', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (241, '멸치김밥', '한식', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (242, '야채김밥', '한식', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (243, '돈까스김밥', '일식', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (244, '떡볶이', '한식', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (245, '로제떡볶이', '한식', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (246, '짜장떡볶이', '한식', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (247, '국물떡볶이', '한식', '', 6000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (248, '순대', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (249, '찰순대', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (250, '야채순대', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (251, '백순대', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (252, '순대볶음', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (253, '튀김', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (254, '오징어튀김', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (255, '야채튀김', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (256, '고구마튀김', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (257, '만두', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (258, '군만두', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (259, '찐만두', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (260, '물만두', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (261, '왕만두', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (262, '김치만두', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (263, '고기만두', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (264, '딤섬', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (265, '샤오롱바오', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (266, '춘권', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (267, '완탕', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (268, '월남쌈', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (269, '쌀국수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (270, '분짜', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (271, '반미', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (272, '팟타이', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (273, '똠얌꿍', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (274, '카오팟', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (275, '나시고렝', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (276, '미고렝', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (277, '커리', '아시안', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (278, '그린커리', '아시안', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (279, '레드커리', '아시안', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (280, '탄두리치킨', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (281, '버터치킨커리', '양식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (282, '난', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (283, '또띠아', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (284, '타코', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (285, '브리또', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (286, '퀘사디아', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (287, '엔칠라다', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (288, '파히타', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (289, '샐러드', '건강식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (290, '시저샐러드', '건강식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (291, '콥샐러드', '건강식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (292, '그릭샐러드', '건강식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (293, '연어샐러드', '건강식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (294, '치킨샐러드', '건강식', '', 22000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (295, '포케', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (296, '연어포케', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (297, '참치포케', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (298, '하와이안포케', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (299, '스프', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (300, '양송이스프', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (301, '콘스프', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (302, '크림스프', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (303, '클램차우더', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (304, '미네스트로네', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (305, '빵', '베이커리', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (306, '식빵', '베이커리', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (307, '바게트', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (308, '크루아상', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (309, '베이글', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (310, '프레첼', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (311, '치아바타', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (312, '케이크', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (313, '초코케이크', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (314, '치즈케이크', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (315, '티라미수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (316, '롤케이크', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (317, '생크림케이크', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (318, '마카롱', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (319, '쿠키', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (320, '초코칩쿠키', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (321, '브라우니', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (322, '머핀', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (323, '도넛', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (324, '와플', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (325, '팬케이크', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (326, '크레페', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (327, '빙수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (328, '팥빙수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (329, '망고빙수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (330, '초코빙수', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (331, '아이스크림', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (332, '젤라또', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (333, '요거트아이스크림', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (334, '스무디', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (335, '밀크쉐이크', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (336, '프라페', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (337, '버블티', '한식', '', 11000, 'Clear', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (338, '흑당버블티', '한식', '', 11000, 'Clear', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (339, '과일주스', '한식', '', 11000, 'Clear', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (340, '레몬에이드', '한식', '', 11000, 'Clear', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (341, '자몽에이드', '한식', '', 11000, 'Clear', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (342, '커피', '카페', '', 6000, 'Clear,Cloudy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (343, '아메리카노', '한식', '', 11000, 'Clear,Cloudy', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (344, '카페라떼', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (345, '카푸치노', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (346, '바닐라라떼', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (347, '카라멜마끼아또', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (348, '콜드브루', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (349, '에스프레소', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (350, '녹차라떼', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menus (menu_id, menu_name, category, image_url, price, matching_weather, suitable_ground_size, is_quick_meal, is_lunch_available) 
VALUES (351, '초코라떼', '한식', '', 11000, '', NULL, 0, 1);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (1, 3, 4, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (2, 3, 4, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (3, 3, 4, 0.6, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (4, 3, 4, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (5, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (6, 3, 4, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (7, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (8, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (9, 3, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (10, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (11, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (12, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (13, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (14, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (15, 2, 3, 0.8, 'hot', 'soft', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (16, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (17, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (18, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (19, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (20, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (21, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (22, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (23, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (24, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (25, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (26, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (27, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (28, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (29, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (30, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (31, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (32, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (33, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (34, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (35, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (36, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (37, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (38, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (39, 1, 2, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (40, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (41, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (42, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (43, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (44, 1, 2, 0.4, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (45, 1, 2, 0.4, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (46, 1, 2, 0.4, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (47, 1, 3, 0.4, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (48, 3, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (49, 3, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (50, 3, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (51, 3, 3, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (52, 3, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (53, 3, 3, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (54, 3, 3, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (55, 1, 2, 0.4, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (56, 3, 3, 0.6, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (57, 1, 2, 0.4, 'hot', 'crunchy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (58, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (59, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (60, 1, 4, 1.0, 'hot', 'crunchy', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (61, 1, 4, 1.0, 'hot', 'crunchy', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (62, 1, 3, 1.0, 'hot', 'crunchy', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (63, 1, 3, 1.0, 'hot', 'crunchy', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (64, 1, 3, 1.0, 'hot', 'crunchy', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (65, 3, 3, 1.0, 'hot', 'crunchy', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (66, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (67, 1, 3, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (68, 1, 3, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (69, 1, 2, 0.6, 'hot', 'crunchy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (70, 1, 3, 0.8, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (71, 1, 3, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (72, 1, 3, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (73, 1, 3, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (74, 1, 3, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (75, 1, 3, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (76, 1, 3, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (77, 1, 3, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (78, 1, 3, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (79, 3, 4, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (80, 3, 4, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (81, 3, 4, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (82, 3, 4, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (83, 3, 4, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (84, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (85, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (86, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (87, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (88, 1, 2, 0.4, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (89, 1, 2, 0.4, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (90, 3, 2, 0.4, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (91, 1, 2, 0.4, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (92, 1, 2, 0.4, 'cold', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (93, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (94, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (95, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (96, 2, 3, 0.4, 'cold', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (97, 2, 3, 0.4, 'cold', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (98, 2, 3, 0.4, 'cold', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (99, 2, 3, 0.4, 'cold', 'chewy', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (100, 2, 3, 0.6, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (101, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (102, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (103, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (104, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (105, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (106, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (107, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (108, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (109, 2, 3, 0.6, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (110, 2, 3, 0.6, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (111, 2, 3, 0.6, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (112, 2, 3, 0.6, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (113, 2, 3, 0.6, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (114, 2, 3, 0.6, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (115, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (116, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (117, 2, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (118, 2, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (119, 2, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (120, 4, 3, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (121, 2, 3, 0.8, 'hot', 'crunchy', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (122, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (123, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (124, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (125, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (126, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (127, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (128, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (129, 5, 4, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (130, 5, 4, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (131, 5, 4, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (132, 1, 2, 0.4, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (133, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (134, 1, 2, 0.4, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (135, 3, 3, 0.6, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (136, 3, 3, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (137, 3, 3, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (138, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (139, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (140, 2, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (141, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (142, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (143, 3, 3, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (144, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (145, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (146, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (147, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (148, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (149, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (150, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (151, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (152, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (153, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (154, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (155, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (156, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (157, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (158, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (159, 1, 2, 0.4, 'cold', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (160, 1, 2, 0.4, 'cold', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (161, 1, 2, 0.4, 'cold', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (162, 1, 2, 0.4, 'cold', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (163, 1, 2, 0.4, 'cold', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (164, 1, 2, 0.4, 'cold', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (165, 1, 2, 0.4, 'cold', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (166, 1, 2, 0.4, 'cold', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (167, 1, 2, 0.4, 'cold', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (168, 1, 2, 0.4, 'cold', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (169, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (170, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (171, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (172, 1, 2, 0.4, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (173, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (174, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (175, 1, 2, 0.4, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (176, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (177, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (178, 1, 2, 0.4, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (179, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (180, 2, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (181, 2, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (182, 2, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (183, 2, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (184, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (185, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (186, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (187, 1, 3, 0.8, 'hot', 'crunchy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (188, 1, 4, 1.0, 'hot', 'crunchy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (189, 1, 3, 0.8, 'hot', 'crunchy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (190, 1, 3, 0.8, 'hot', 'crunchy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (191, 1, 3, 1.0, 'hot', 'crunchy', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (192, 1, 2, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (193, 1, 2, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (194, 1, 2, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (195, 1, 2, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (196, 1, 2, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (197, 1, 2, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (198, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (199, 1, 3, 0.8, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (200, 1, 3, 0.8, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (201, 1, 3, 0.8, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (202, 1, 3, 0.8, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (203, 1, 3, 0.8, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (204, 1, 3, 0.8, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (205, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (206, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (207, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (208, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (209, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (210, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (211, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (212, 1, 3, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (213, 1, 3, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (214, 1, 3, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (215, 1, 3, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (216, 3, 3, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (217, 1, 3, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (218, 1, 3, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (219, 1, 4, 1.0, 'hot', 'normal', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (220, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (221, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (222, 1, 2, 0.4, 'room', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (223, 1, 2, 0.4, 'room', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (224, 1, 2, 0.4, 'room', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (225, 1, 2, 0.4, 'room', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (226, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (227, 1, 3, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (228, 1, 4, 1.0, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (229, 3, 3, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (230, 1, 3, 1.0, 'hot', 'crunchy', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (231, 1, 3, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (232, 1, 3, 0.8, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (233, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (234, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (235, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (236, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (237, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (238, 1, 2, 0.4, 'room', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (239, 1, 2, 0.4, 'room', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (240, 1, 3, 0.6, 'room', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (241, 1, 2, 0.4, 'room', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (242, 1, 2, 0.4, 'room', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (243, 1, 3, 0.8, 'room', 'crunchy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (244, 2, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (245, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (246, 2, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (247, 2, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (248, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (249, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (250, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (251, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (252, 3, 3, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (253, 1, 2, 0.6, 'hot', 'crunchy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (254, 1, 2, 0.6, 'hot', 'crunchy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (255, 1, 2, 0.6, 'hot', 'crunchy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (256, 1, 2, 0.6, 'hot', 'crunchy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (257, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (258, 1, 2, 0.4, 'hot', 'crunchy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (259, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (260, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (261, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (262, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (263, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (264, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (265, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (266, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (267, 2, 3, 0.8, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (268, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (269, 1, 2, 0.4, 'hot', 'chewy', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (270, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (271, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (272, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (273, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (274, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (275, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (276, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (277, 3, 3, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (278, 3, 3, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (279, 3, 3, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (280, 1, 3, 1.0, 'hot', 'crunchy', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (281, 1, 3, 1.0, 'hot', 'crunchy', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (282, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (283, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (284, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (285, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (286, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (287, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (288, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (289, 1, 2, 0.2, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (290, 1, 2, 0.2, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (291, 1, 2, 0.2, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (292, 1, 2, 0.2, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (293, 1, 2, 0.2, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (294, 1, 2, 0.2, 'cold', 'crunchy', 0.82, 25, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (295, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (296, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (297, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (298, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (299, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (300, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (301, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (302, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (303, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (304, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (305, 1, 2, 0.6, 'room', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (306, 1, 2, 0.6, 'room', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (307, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (308, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (309, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (310, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (311, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (312, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (313, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (314, 1, 3, 0.6, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (315, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (316, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (317, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (318, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (319, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (320, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (321, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (322, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (323, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (324, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (325, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (326, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (327, 1, 2, 0.4, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (328, 1, 2, 0.4, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (329, 1, 2, 0.4, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (330, 1, 2, 0.4, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (331, 1, 2, 0.4, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (332, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (333, 1, 2, 0.4, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (334, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (335, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (336, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (337, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (338, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (339, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (340, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (341, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (342, 1, 1, 0.2, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (343, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (344, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (345, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (346, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (347, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (348, 1, 2, 0.4, 'cold', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (349, 1, 2, 0.4, 'hot', 'soft', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (350, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);

INSERT INTO menu_details (menu_id, spicy_level, saltiness_level, heaviness, serving_temperature, texture, revisit_rate, avg_waiting_time, ad_suspicion_index, real_satisfaction_score) 
VALUES (351, 1, 2, 0.4, 'hot', 'normal', 0.82, 12, 0.05, 4.3);


-- UPDATE statements for matching_weather column
-- Generated from weather-menu mapping data

UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = 'BLT샌드위치';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = 'LA갈비';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '가브리살';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '가츠동';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '간장새우';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '간장치킨';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '간짜장';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '갈매기살';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '갈비탕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '갈치구이';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '갈치조림';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '감자탕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '게살볶음밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '계란토스트';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '고구마돈까스';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '고구마튀김';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '고기만두';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '고등어구이';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '고등어조림';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '고르곤졸라피자';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '고추잡채';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '곰탕';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '과일주스';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '광어회';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '국물떡볶이';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '군만두';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '굴국밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '굴비구이';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '규동';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '그릭샐러드';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '그린커리';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '김밥';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '김치라면';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '김치만두';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '김치볶음밥';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '김치찌개';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '까르보나라';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '깐풍기';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '깐풍육';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '꼬리곰탕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '꽁치구이';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '꽁치조림';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '나시고렝';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '낙지덮밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '낙지볶음';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '난';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '내장탕';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '냄비우동';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '냉면';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '냉모밀';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '냉우동';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '냉채족발';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '녹차라떼';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '농어회';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '닭갈비';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '닭강정';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '닭개장';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '닭곰탕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '닭똥집';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '닭발';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '닭백숙';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '닭볶음탕';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '대구탕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '대하구이';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '덮밥';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '도가니탕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '도넛';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '도미회';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '돈까스';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '돈까스김밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '돈부리';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '돈코츠라멘';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '동태찌개';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '돼지갈비';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '돼지국밥';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '된장찌개';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '들깨칼국수';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '딤섬';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '따로국밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '떡볶이';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '또띠아';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '똠얌꿍';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '라멘';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '라면';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '라자냐';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '레드커리';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '레몬에이드';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '로제떡볶이';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '롤케이크';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '리조또';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '립아이';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '마늘족발';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '마늘치킨';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '마라룽샤';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '마라샹궈';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '마라탕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '마르게리타피자';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '마카롱';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '마파두부';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '막국수';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '만두';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '망고빙수';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '매운탕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '머핀';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '메밀국수';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '멸치김밥';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '모둠초밥';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '모밀';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '목살';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '물냉면';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '물막국수';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '물만두';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '물회';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '미고렝';
UPDATE menus SET matching_weather = 'Mist' WHERE menu_name = '미네스트로네';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '미소라멘';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '미역국';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '밀면';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '밀크쉐이크';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '바게트';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '바닐라라떼';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '바지락칼국수';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '반미';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '방어회';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '백순대';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '백짬뽕';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '버블티';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '버섯리조또';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '버터치킨커리';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '베이글';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '보쌈';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '볶음짬뽕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '봉골레파스타';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '부대찌개';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '북어국';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '분짜';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '불고기';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '불고기버거';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '불고기피자';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '불족발';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '브라우니';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '브루스케타';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '브리또';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '비빔국수';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '비빔냉면';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '비빔막국수';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '빙수';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '빵';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '뼈해장국';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '사케동';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '산더미불고기';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '삼겹살';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '삼계탕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '삼선짜장';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '삼선짬뽕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '삼치구이';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '새우버거';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '새우볶음밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '새우튀김';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '샌드위치';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '샐러드';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '생선까스';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '생선조림';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '생크림케이크';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '샤오롱바오';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '선지해장국';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '설렁탕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '소갈비';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '소머리국밥';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '소바';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '손칼국수';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '쇼유라멘';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '수육국밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '수제버거';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '수프카레';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '순대';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '순대국';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '순대볶음';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '순두부찌개';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '순살치킨';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '숯불치킨';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '스무디';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '스시롤';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '스테이크';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '시래기국';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '시저샐러드';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '식빵';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '쌀국수';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '아메리카노';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '아이스크림';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '안심스테이크';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '알리오올리오';
UPDATE menus SET matching_weather = 'Mist' WHERE menu_name = '알밥';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '알탕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '야채김밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '야채순대';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '야채튀김';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '야키우동';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '양갈비';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '양꼬치';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '양념갈비';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '양념새우';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '양념치킨';
UPDATE menus SET matching_weather = 'Mist' WHERE menu_name = '양송이스프';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '양장피';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '양평해장국';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '어묵우동';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '언양불고기';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '에비동';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '에스프레소';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '엔칠라다';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '연어샐러드';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '연어포케';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '연어회';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '열무국수';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '오리백숙';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '오리주물럭';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '오리훈제';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '오삼불고기';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '오일파스타';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '오징어덮밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '오징어튀김';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '와플';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '왕만두';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '요거트아이스크림';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '우거지탕';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '우동';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '우럭회';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '월남쌈';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '유린기';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '육개장';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '일본식카레';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '임연수구이';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '자몽에이드';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '잔치국수';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '잡채밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '잡탕밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '장어구이';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '장터국밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '제육덮밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '제육볶음';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '젤라또';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '조기구이';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '족발';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '중국식볶음밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '짜장떡볶이';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '짜장라면';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '짜장면';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '짜장밥';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '짬뽕';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '짬뽕밥';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '쫄면';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '쭈꾸미볶음';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '찐만두';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '찰순대';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '참치김밥';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '참치포케';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '참치회';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '채끝스테이크';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '청국장';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '초밥';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '초코라떼';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '초코빙수';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '초코칩쿠키';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '초코케이크';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '추어탕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '춘권';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '츠케멘';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '치아바타';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '치아바타샌드위치';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '치즈김밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '치즈돈까스';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '치즈버거';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '치즈케이크';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '치즈피자';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '치킨까스';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '치킨버거';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '치킨샐러드';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '카라멜마끼아또';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '카레라이스';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '카오팟';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '카츠카레';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '카페라떼';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '카푸치노';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '칼국수';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '커리';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '커피';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '케이크';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '코다리조림';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '콘도그';
UPDATE menus SET matching_weather = 'Mist' WHERE menu_name = '콘스프';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '콜드브루';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '콤비네이션피자';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '콥샐러드';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '콩국수';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '콩나물국밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '쿠키';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '퀘사디아';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '크레페';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '크루아상';
UPDATE menus SET matching_weather = 'Mist' WHERE menu_name = '크림스프';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '크림파스타';
UPDATE menus SET matching_weather = 'Mist' WHERE menu_name = '클램차우더';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '클럽샌드위치';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '타코';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '탄두리치킨';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '탄탄멘';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '탕수육';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '텐동';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '토마토파스타';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '토마호크스테이크';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '토스트';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '튀김';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '트러플리조또';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '티라미수';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '티본스테이크';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '파니니';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '파닭';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '파스타';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '파히타';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '판모밀';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '팔보채';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '팟타이';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '팥빙수';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '팬케이크';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '페퍼로니피자';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '포카치아';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '포케';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '프라페';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '프레첼';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '프렌치토스트';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '피자';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '하와이안포케';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '하와이안피자';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '함박스테이크';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '핫도그';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '항정살';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '해물라면';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '해물리조또';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '해물탕';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '해물파스타';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '햄버거';
UPDATE menus SET matching_weather = 'Rain' WHERE menu_name = '황태국';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '회';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '회냉면';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '회덮밥';
UPDATE menus SET matching_weather = 'Clouds' WHERE menu_name = '후라이드치킨';
UPDATE menus SET matching_weather = 'Snow' WHERE menu_name = '훠궈';
UPDATE menus SET matching_weather = 'Clear' WHERE menu_name = '흑당버블티';

-- 인덱스 생성 (성능 최적화)
CREATE INDEX IF NOT EXISTS idx_menus_category ON menus(category);
CREATE INDEX IF NOT EXISTS idx_menus_name ON menus(menu_name);
CREATE INDEX IF NOT EXISTS idx_menus_price ON menus(price);
CREATE INDEX IF NOT EXISTS idx_menu_details_menu_id ON menu_details(menu_id);

-- 데이터 추출 완료
-- 총 메뉴 수: 351
-- 총 상세 정보 수: 351


