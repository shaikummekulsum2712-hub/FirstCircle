from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..models.circle import Circle

def run_reminder_job(db: Session):
    """
    Finds circles occurring in the next 2 hours and issues attendance logs.
    """
    now = datetime.utcnow()
    two_hours_later = now + timedelta(hours=2)
    
    upcoming_circles = db.query(Circle).filter(
        Circle.status.in_(["scheduled", "rescheduled"]),
        Circle.event_time >= now,
        Circle.event_time <= two_hours_later
    ).all()

    for circle in upcoming_circles:
        # Simulate pushing reminders
        print(f"[REMINDER JOB] Circle '{circle.title}' is starting soon at {circle.event_time} (Location: {circle.location_name})")
