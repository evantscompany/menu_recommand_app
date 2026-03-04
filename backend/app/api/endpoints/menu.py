from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database_mysql import get_db # 기존 main이나 database에 정의된 get_db 사용 권장
from ... import crud, schemas

router = APIRouter()

# [수정] response_model을 schemas.Menu로 변경
@router.post("/", response_model=schemas.Menu)
def create_new_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    """새로운 메뉴(식당) 데이터를 등록합니다."""
    return crud.create_menu(db=db, menu=menu)

# [수정] response_model을 list[schemas.Menu]로 변경
@router.get("/", response_model=list[schemas.Menu])
def read_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """등록된 모든 메뉴 리스트를 가져옵니다."""
    # skip=0일 때 문제가 있으므로, skip이 0이면 1로 변경
    actual_skip = skip if skip > 0 else 1
    menus = crud.get_menus(db, skip=actual_skip, limit=limit)
    return menus

# [수정] store_id를 menu_id로 명칭 통일
@router.delete("/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """특정 메뉴를 삭제합니다."""
    success = crud.delete_menu(db, menu_id=menu_id)
    if not success:
        raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다.")
    return {"message": f"Menu {menu_id} 삭제 완료"}