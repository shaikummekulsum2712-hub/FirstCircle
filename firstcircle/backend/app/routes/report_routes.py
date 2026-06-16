from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.security import get_current_user
from ..models.user import User
from ..schemas.feedback_schema import ReportCreate
from ..services.profile_service import get_profile_by_user_id
from ..services.feedback_service import submit_safety_report

router = APIRouter(prefix="/reports", tags=["moderation"])

@router.post("", status_code=status.HTTP_201_CREATED)
def post_report(payload: ReportCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    report = submit_safety_report(db, profile.id, payload)
    return {"message": "Report received", "report_id": report.id}
