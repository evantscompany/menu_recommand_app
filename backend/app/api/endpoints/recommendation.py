from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random
from datetime import datetime
import math

from ...database_mysql import get_db
from ... import models, schemas, crud
from ...core.algorithm import calculate_recommendation_score, generate_recommendation_reason
# 인증 Dependency 가져오기
from ..deps import get_current_user 

router = APIRouter()

# 실시간 날씨 서비스 가져오기
from ...core.weather_service import weather_service

def add_recommendation_randomness(scored_items):
    """
    추천 결과에 랜덤성 추가하여 동일 메뉴 추천 방지
    """
    random.seed(datetime.now().microsecond)  # 현재 시간의 마이크로초로 시드 설정
    
    randomized_items = []
    for item in scored_items:
        if len(item) == 3:  # (score, menu, reason) 형태
            score, menu, reason = item
        else:  # (score, menu) 형태
            score, menu = item
            reason = None
        
        # 점수의 15%만큼 랜덤 변동 추가 (다양성 강화)
        random_variation = score * 0.15 * (random.random() - 0.5) * 2
        new_score = max(0, min(100, score + random_variation))
        
        if reason:
            randomized_items.append((new_score, menu, reason))
        else:
            randomized_items.append((new_score, menu))
    
    # 다시 정렬
    randomized_items.sort(key=lambda x: x[0], reverse=True)
    
    # 다양성 메커니즘 추가
    randomized_items = apply_diversity_mechanism(randomized_items)
    
    return randomized_items

def select_diverse_third_menu(scored_items, user_id, db):
    """
    3번째 추천을 위한 다양성 메뉴 선택 (기존 버전 - 호환성 유지)
    """
    if len(scored_items) < 3:
        return None
    
    latest_history = db.query(models.UserHistory)\
        .filter(models.UserHistory.user_id == user_id)\
        .order_by(models.UserHistory.last_visit_date.desc())\
        .first()
    
    return select_diverse_third_menu_optimized(scored_items, latest_history)

def select_diverse_third_menu_optimized(scored_items, latest_history):
    """
    3번째 추천을 위한 다양성 메뉴 선택 (최적화 버전 - DB 쿼리 제거)
    - 상위 2개와 유사하지만 추천되지 않았던 메뉴 선택
    - 카테고리 다양성 확보 (강화)
    """
    if len(scored_items) < 3:
        return None
    
    # 상위 2개 메뉴 정보
    top_2_menus = [item[1] for item in scored_items[:2]]
    top_2_categories = {menu.category for menu in top_2_menus}
    
    # 최근 추천 기록 확인 (이미 조회된 히스토리 사용)
    recent_menu_names = set()
    if latest_history and latest_history.recent_menus:
        recent_menu_names = set(latest_history.recent_menus[:5])  # 최근 5개만 확인
    
    # 후보 메뉴 필터링 (상위 2개 제외, 최근 추천 제외)
    diverse_candidates = []
    for score, menu in scored_items[2:]:  # 상위 2개 제외
        # 최근 추천된 메뉴 제외
        if menu.menu_name in recent_menu_names:
            continue
            
        # 카테고리 다양성 강력 고려
        if menu.category not in top_2_categories:
            # 새로운 카테고리는 강력 우선 후보
            diverse_candidates.append((score + 20, menu))
        else:
            # 같은 카테고리라도 점수가 높은 것은 후보
            if score >= 70:
                diverse_candidates.append((score, menu))
    
    # 후보가 없으면 기존 방식으로 fallback
    if not diverse_candidates:
        return None
    
    # 후보 중에서 점수가 가장 높은 메뉴 선택
    diverse_candidates.sort(key=lambda x: x[0], reverse=True)
    selected_menu = diverse_candidates[0][1]
    
    return (diverse_candidates[0][0], selected_menu)

def apply_diversity_mechanism(scored_items):
    """
    강화된 다양성 메커니즘 적용 - 카테고리 최대 1개 제한 및 상위 5개 셔플
    """
    # 1. 카테고리 최대 1개 제한 (강화)
    category_limited_items = []
    used_categories = set()
    
    for item in scored_items:
        if len(item) == 3:  # (score, menu, reason) 형태
            score, menu, reason = item
        else:  # (score, menu) 형태
            score, menu = item
            reason = None
        
        if menu.category not in used_categories:
            if reason:
                category_limited_items.append((score, menu, reason))
            else:
                category_limited_items.append((score, menu))
            used_categories.add(menu.category)
        else:
            # 이미 사용된 카테고리는 강력 페널티
            penalty = 50  # 카테고리 중복 강력 페널티
            if reason:
                category_limited_items.append((max(0, score - penalty), menu, reason))
            else:
                category_limited_items.append((max(0, score - penalty), menu))
            print(f" 🔄 {menu.menu_name}: 카테고리 중복 강력 페널티 (-50) - {menu.category}")
    
    # 다시 정렬
    category_limited_items.sort(key=lambda x: x[0], reverse=True)
    
    # 2. 상위 5개 메뉴 셔플 (다양성 극대화)
    top_5_items = category_limited_items[:5]
    
    # 상위 5개 메뉴 랜덤 셔플
    random.shuffle(top_5_items)
    
    # 셔플된 상위 5개와 나머지 합치기
    remaining_items = category_limited_items[5:]
    final_items = top_5_items + remaining_items
    
    # 3. 최상위 메뉴 추가 페널티 (연속 독점 방지)
    if len(final_items) > 0:
        top_menu = final_items[0][1]
        for i, item in enumerate(final_items):
            if len(item) == 3:
                score, menu, reason = item
            else:
                score, menu = item
                reason = None
                
            if menu.menu_name == top_menu.menu_name:
                if reason:
                    final_items[i] = (max(0, score - 15), menu, reason)
                else:
                    final_items[i] = (max(0, score - 15), menu)
                print(f" 🔄 {menu.menu_name}: 최상위 메뉴 페널티 (-15)")
                break
    
    # 최종 정렬
    final_items.sort(key=lambda x: x[0], reverse=True)
    return final_items

@router.get("/recommendations", response_model=List[schemas.MenuRecommendation])
def get_recommendations_get(
    current_user: models.UserAccount = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    GET 방식 추천 API - 프론트엔드 호환용
    """
    # 인증된 사용자만 추천 가능
    user_id = current_user.user_id
    user_profile = current_user.profile

    if not user_profile:
        raise HTTPException(status_code=404, detail="사용자 성향 프로필을 찾을 수 없습니다.")

    # 메뉴 조회
    menus = db.query(models.Menu)\
        .filter(models.Menu.is_lunch_available == True)\
        .all()
    
    # 실시간 날씨 데이터
    weather_data = weather_service.get_current_weather("Seoul")
    
    # 추천 점수 계산
    scored_items = []
    for menu in menus:
        score = calculate_recommendation_score(
            menu=menu,
            user=user_profile,
            daily_inquiry=None,
            weather_data=weather_data,
            history=None,
            db=db
        )
        if score > 0:
            reason = generate_recommendation_reason(menu, weather_data, user_profile, db)
            scored_items.append((score, menu, reason))
    
    # 랜덤성 추가
    scored_items = add_recommendation_randomness(scored_items)
    
    # 상위 3개 선택
    final_items = []
    for score, menu, reason in scored_items[:3]:
        # [추가] 메뉴 카테고리와 똑같은 식당 정보를 DB에서 찾아옵니다.
        restaurant = db.query(models.Restaurant).filter(
            models.Restaurant.category_1 == menu.category
        ).first()

        description = reason or f"오늘 날씨에 어울리는 {menu.category} 메뉴를 추천해요!"
        
        final_items.append(schemas.MenuRecommendation(
            menu_name=menu.menu_name,
            category=menu.category,
            price=menu.price,
            match_rate=min(int(score * 100), 100),
            description=description,
            image_url=menu.image_url,
            details=schemas.MenuRecommendationDetail(
                spicy_level=menu.details.spicy_level if menu.details else 0,
                texture=menu.details.texture if menu.details else "일반적",
                rating=menu.details.real_satisfaction_score if menu.details else 0.0
            ),
            # [수정] None을 빼고, 위에서 찾은 restaurant 변수를 넣어줍니다!
            restaurant_info=restaurant
        ))
    
    return final_items

@router.post("/", response_model=List[schemas.MenuRecommendation])
def get_recommendations(
    # [변경] inquiry 파라미터 제거 - 사용자 프로필만 사용
    current_user: models.UserAccount = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    사용자 프로필 기반으로 최적의 메뉴 3곳을 추천합니다.
    """
    # 1. 유저 확인 (current_user에 이미 유저 성향 profile이 포함되어 있음)
    user_id = current_user.user_id
    user_profile = current_user.profile # 알고리즘에 전달할 유저 성향 데이터

    
    
    if not user_profile:
        raise HTTPException(status_code=404, detail="사용자 성향 프로필을 찾을 수 없습니다.")

    # 2. 기초 데이터 준비 - 메뉴와 상세정보를 한 번에 조회 (JOIN 최적화)
    menus = db.query(models.Menu)\
        .filter(models.Menu.is_lunch_available == True)\
        .options(
            # 메뉴 상세정보를 미리 로드하여 N+1 쿼리 문제 방지
            # joinedload는 사용하지 않고 필요시에만 조회
        )\
        .all()
    
    # 실시간 날씨 데이터 가져오기 (서울 기준)
    weather_data = weather_service.get_current_weather("Seoul")

    # 사용자의 최신 히스토리 한 번만 조회
    latest_history = db.query(models.UserHistory)\
        .filter(models.UserHistory.user_id == user_id)\
        .order_by(models.UserHistory.last_visit_date.desc())\
        .first()
    
    # 모든 메뉴에 대한 히스토리를 한 번에 조회 (N+1 문제 해결)
    all_histories = db.query(models.UserHistory)\
        .filter(models.UserHistory.user_id == user_id)\
        .all()
    
    # 메뉴 ID를 키로 하는 히스토리 딕셔너리 생성
    history_map = {h.menu_id: h for h in all_histories if h.menu_id}
    
    scored_items = []
    for menu in menus:
        # 딕셔너리에서 히스토리 조회 (DB 쿼리 없음)
        history = history_map.get(menu.menu_id, latest_history)
        
        # 개선된 알고리즘 함수 호출 (실시간 피드백 반영)
        score = calculate_recommendation_score(
            menu=menu,
            user=user_profile,
            daily_inquiry=None,  # None으로 전달
            weather_data=weather_data,
            history=history,
            db=db  # DB 세션 전달
        )
        
        if score >= 0:
            scored_items.append((score, menu))

    # 3. 점수 순 정렬 및 상위 10개 (로그 및 결과용)
    scored_items.sort(key=lambda x: x[0], reverse=True)
    
    # 랜덤성 추가를 간소화 (성능 개선)
    if len(scored_items) > 3:
        # 상위 10개만 랜덤성 적용 (전체 처리 불필요)
        top_candidates = scored_items[:10]
        top_candidates = add_recommendation_randomness(top_candidates)
        scored_items = top_candidates + scored_items[10:]
    
    # 🎯 3번째 추천: 유사하지만 추천되지 않았던 메뉴 포함
    top_2 = scored_items[:2]
    
    # 3번째 메뉴 선택 로직 (latest_history 재사용)
    third_menu = select_diverse_third_menu_optimized(scored_items, latest_history)
    if third_menu:
        top_3 = top_2 + [third_menu]
    else:
        top_3 = scored_items[:3]  # 기존 방식으로 fallback
    
    top_10_for_log = scored_items[:10]

    # --- [VS Code 콘솔 출력 로그 시작] (로직 유지) ---
    print("\n" + " " + "="*65)
    print(f" [알고리즘 분석 리포트] 유저 ID: {user_id} ({current_user.username})")
    print(f" 조건: 예산({user_profile.lunch_budget_max}원), 맵기({user_profile.spicy_threshold})")
    print("-" * 67)
    
    if not scored_items:
        print(" 추천 가능한 메뉴가 없습니다.")
    else:
        for i, (score, menu) in enumerate(top_10_for_log, 1):
            display_match = min(99, int(score)) if score < 100 else 99
            rank_label = f" {i}위" if i <= 3 else f"   {i}위"
            print(f"{rank_label} | {display_match}% | {score:6.2f}점 | [{menu.category}] {menu.menu_name[:12]:<12}")
            
    print("="*67 + "\n")
    # --- [VS Code 콘솔 출력 로그 끝] ---

    if not top_3:
        raise HTTPException(status_code=404, detail="조건에 맞는 추천 결과가 없습니다.")

    # 🔥 최근 추천된 메뉴 업데이트 로직
    current_recommendations = [menu.menu_name for score, menu in top_3]
    
    # 사용자 히스토리 가져오기 (최신순)
    user_history = db.query(models.UserHistory)\
        .filter(models.UserHistory.user_id == user_id)\
        .order_by(models.UserHistory.last_visit_date.desc())\
        .first()
    
    if user_history:
        # 기존 recent_menus 가져오기
        recent_menus = user_history.recent_menus or []
        
        # 새로운 추천 메뉴 추가 (최대 10개 유지)
        for menu_name in current_recommendations:
            if menu_name not in recent_menus:
                recent_menus.insert(0, menu_name)
        
        # 최근 10개만 유지
        user_history.recent_menus = recent_menus[:10]
        db.commit()
        
        print(f"📝 최근 추천 메뉴 업데이트: {user_history.recent_menus}")
    else:
        # 히스토리가 없는 경우 새로 생성
        print("⚠️ 사용자 히스토리 없음 - 새로 생성")

    # 4. 프론트엔드 규격 변환 (메뉴 정보만 포함)
    # 4. 프론트엔드 규격 변환 (여기를 찾으세요!)
    results = []
    for score, menu in top_3:
        # [여기서부터 추가되는 핵심 코드]
        # 메뉴 카테고리와 일치하는 식당을 사장님 DB에서 하나 가져옵니다.
        restaurant = db.query(models.Restaurant).filter(
            models.Restaurant.category_1 == menu.category
        ).first()

        match_rate = min(99, int(score)) if score < 100 else 99
        spicy = menu.details.spicy_level if menu.details else 0
        texture = menu.details.texture if menu.details else "일반적"
        rating = menu.details.real_satisfaction_score if menu.details else 0.0

        results.append(
            schemas.MenuRecommendation(
                menu_name=menu.menu_name,
                category=menu.category,
                image_url=menu.image_url or "https://via.placeholder.com/150",
                price=menu.price,
                match_rate=match_rate,
                description=generate_recommendation_reason(menu, weather_data, user=current_user, db=db) or f"오늘 날씨에 어울리는 {menu.category} 메뉴를 추천해요!",
                details=schemas.MenuRecommendationDetail(
                    spicy_level=spicy,
                    texture=texture,
                    rating=rating
                ),
                # [수정] None 대신 위에서 찾은 restaurant 변수를 넣어줍니다.
                restaurant_info=restaurant
            )
        )
    return results
   

@router.post("/select/{menu_id}")
def select_menu(
    menu_id: int, 
    current_user: models.UserAccount = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """메뉴 최종 선택 시 히스토리 생성 (인증 적용)"""
    menu = db.query(models.Menu).filter(models.Menu.menu_id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="메뉴 정보를 찾을 수 없습니다.")
    
    # 🔥 사용자의 최신 히스토리 가져오기
    latest_history = db.query(models.UserHistory)\
        .filter(models.UserHistory.user_id == current_user.user_id)\
        .order_by(models.UserHistory.last_visit_date.desc())\
        .first()
    
    if latest_history:
        # 기존 히스토리 업데이트
        latest_history.menu_id = menu_id
        latest_history.last_eaten_menu = menu.menu_name
        latest_history.last_eaten_category = menu.category
        latest_history.last_visit_date = datetime.utcnow()
        latest_history.visit_count = (latest_history.visit_count or 0) + 1
        db.commit()
        
        print(f"📝 기존 히스토리 업데이트: {menu.menu_name}")
        return {"message": f"{menu.menu_name} 선택 완료", "history_id": latest_history.history_id}
    else:
        # 새 히스토리 생성
        history = crud.create_user_history(db, user_id=current_user.user_id, menu_id=menu_id, category=menu.category)
        history.last_eaten_menu = menu.menu_name
        history.last_eaten_category = menu.category
        db.commit()
        
        print(f"📝 새 히스토리 생성: {menu.menu_name}")
        return {"message": f"{menu.menu_name} 선택 완료", "history_id": history.history_id}

@router.post("/feedback", response_model=dict)
def submit_feedback_get(
    feedback: dict,
    current_user: models.UserAccount = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    피드백 API - 프론트엔드 호환용 (인증 필수)
    """
    try:
        user_id = current_user.user_id
        menu_name = feedback.get("menu_name")
        feedback_type = feedback.get("feedback_type")
        category = feedback.get("category")
        score = feedback.get("score", 0)
        
        # 피드백 저장
        db_feedback = models.RecommendationFeedback(
            user_id=user_id,
            menu_name=menu_name,
            feedback_type=feedback_type,
            category=category,
            score=score
        )
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        
        return {"message": "피드백이 저장되었습니다", "feedback_id": db_feedback.feedback_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"피드백 저장 실패: {str(e)}")

@router.post("/feedback/instant", response_model=schemas.FeedbackResponse)
def submit_instant_feedback(
    feedback: schemas.FeedbackCreate, 
    current_user: models.UserAccount = Depends(get_current_user), # 추가 보안용
    db: Session = Depends(get_db)
):
    """추천 리스트에서 메뉴별 즉각 피드백 저장"""
    # 요청 바디의 user_id보다 인증된 유저의 id를 우선시하여 보안 강화
    db_feedback = models.RecommendationFeedback(
        user_id=current_user.user_id,
        menu_name=feedback.menu_name,
        feedback_type=feedback.feedback_type,
        category=feedback.category,
        score=feedback.score
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.patch("/feedback/{history_id}")
def submit_feedback(
    history_id: int, 
    feedback: schemas.FeedbackUpdate, 
    current_user: models.UserAccount = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """식사 후 방문 기록에 대한 상세 피드백 업데이트"""
    # 내 기록인지 확인하는 로직을 추가하면 더 안전합니다.
    updated_history = crud.update_user_feedback(db, history_id=history_id, feedback=feedback)
    if not updated_history:
         raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다.")
    return {"message": "피드백이 반영되었습니다."}

def get_distance(lat1, lon1, lat2, lon2):
    R = 6371e3 # 지구 반지름 (미터)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c # 미터(m) 단위 결과

#2026-03-03 추가
# 중복 없이 상위 5개만 골라냅니다.
# 📍 주변 5곳 조회 API (실시간 거리 계산 포함)
@router.get("/nearby", response_model=List[schemas.RestaurantBase])
def get_nearby_restaurants(
    lat: float, 
    lon: float, 
    db: Session = Depends(get_db)
):
    # 1. DB에서 모든 식당 데이터를 가져옵니다.
    all_restaurants = db.query(models.Restaurant).all()
    
    # 2. 각 식당별로 실시간 거리를 계산해서 리스트에 담습니다.
    restaurant_with_distance = []
    for res in all_restaurants:
        dist = get_distance(lat, lon, res.latitude, res.longitude)
        restaurant_with_distance.append((dist, res))

    # 3. 거리순(가까운 순)으로 정렬합니다.
    restaurant_with_distance.sort(key=lambda x: x[0])

    # 4. 중복 없이 상위 5개만 골라내며 데이터를 가공합니다.
    unique_5 = []
    seen_names = set()
    
    for dist, res in restaurant_with_distance:
        if res.name not in seen_names:
            # 실시간 거리(m)와 도보 시간(분) 계산
            calculated_dist = int(dist)
            calculated_time = max(1, int(dist / 80))
            
            # 딕셔너리 형태로 만들어 안전하게 반환합니다.
            restaurant_data = {
                "name": res.name,
                "category_1": res.category_1,
                "address": res.address,
                "latitude": res.latitude,
                "longitude": res.longitude,
                "distance": calculated_dist,
                "walking_time": calculated_time
            }
            
            unique_5.append(restaurant_data)
            seen_names.add(res.name)
            
        if len(unique_5) == 5:
            break
            
    return unique_5