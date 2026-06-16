from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.security import get_current_user
from ..models.user import User
from ..schemas.feedback_schema import FeedbackCreate
from ..services.profile_service import get_profile_by_user_id
from ..services.feedback_service import submit_circle_feedback

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("", status_code=status.HTTP_200_OK)
def post_feedback(payload: FeedbackCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = get_profile_by_user_id(db, current_user.id)
    submit_circle_feedback(db, profile.id, payload)
    return {"message": "Feedback submitted successfully"}
