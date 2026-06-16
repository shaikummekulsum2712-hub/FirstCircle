from sqlalchemy.orm import Session
from datetime import datetime
from ..models.circle import Circle

def process_reschedule(db: Session, circle_id: int, new_time: datetime) -> Circle:
    circle = db.query(Circle).filter(Circle.id == circle_id).first()
    if circle:
        circle.event_time = new_time
        circle.status = "rescheduled"
        db.commit()
        db.refresh(circle)
    return circle
