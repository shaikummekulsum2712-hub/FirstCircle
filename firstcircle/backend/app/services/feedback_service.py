from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from ..models.feedback import Feedback
from ..models.report import Report
from ..models.circle import Circle
from ..schemas.feedback_schema import FeedbackCreate, ReportCreate
from ..ml.feedback_model import feedback_affinity_model
from .reliability_service import update_user_reliability

def submit_circle_feedback(db: Session, reviewer_id: int, feedback_data: FeedbackCreate) -> bool:
    circle = db.query(Circle).filter(Circle.id == feedback_data.circle_id).first()
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    # 1. Process Attendance Ratings (and adjust reliability score accordingly)
    for att in feedback_data.attendance:
        # Determine score delta
        delta = 0.0
        if att.status == "on-time":
            delta = 2.0
        elif att.status == "late":
            delta = -5.0
        elif att.status == "no-show":
            delta = -15.0
        
        # Apply score update to database
        update_user_reliability(db, att.profile_id, att.status, delta)

    # 2. Process Peer Vibe Ratings
    for r in feedback_data.ratings:
        # Save feedback row in database
        db_fb = Feedback(
            circle_id=feedback_data.circle_id,
            reviewer_id=reviewer_id,
            reviewee_id=r.profile_id,
            rating=r.rating,
            tags=r.tags
        )
        db.add(db_fb)
        
        # Feed back into local ML model
        feedback_affinity_model.update_affinity(reviewer_id, r.profile_id, r.rating)

    db.commit()
    return True

def submit_safety_report(db: Session, reporter_id: int, report_data: ReportCreate) -> Report:
    new_report = Report(
        circle_id=report_data.circle_id,
        reporter_id=reporter_id,
        reportee_id=report_data.reportee_id,
        reason=report_data.reason,
        status="pending"
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report
