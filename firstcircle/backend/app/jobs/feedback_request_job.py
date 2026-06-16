from sqlalchemy.orm import Session
from datetime import datetime
from ..models.circle import Circle

def run_feedback_request_job(db: Session):
    """
    Checks circles that have concluded and marks their status as completed.
    """
    now = datetime.utcnow()
    finished_circles = db.query(Circle).filter(
        Circle.status.in_(["scheduled", "rescheduled"]),
        Circle.event_time < now
    ).all()

    count = 0
    for circle in finished_circles:
        circle.status = "completed"
        count += 1

    if count > 0:
        db.commit()
        print(f"[JOB] Concluded {count} social meetups; peer review prompts are now active.")
