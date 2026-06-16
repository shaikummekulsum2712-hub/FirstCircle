from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.auto_place_schema import AutoPlaceRequest, AutoPlaceResponse
from ..matching.auto_place import run_auto_place_matching

router = APIRouter(prefix="/autoplace", tags=["matching"])

@router.post("/run", response_model=AutoPlaceResponse)
def trigger_autoplace(payload: AutoPlaceRequest, db: Session = Depends(get_db)):
    drops_count = run_auto_place_matching(db, target_category=payload.category, target_date_str=payload.target_date)
    return {
        "success": True,
        "matched_groups_count": drops_count,
        "message": f"Successfully created {drops_count} matching proposals from inactive calendar blocks."
    }
