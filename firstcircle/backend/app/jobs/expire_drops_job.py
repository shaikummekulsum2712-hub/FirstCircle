from sqlalchemy.orm import Session
from datetime import datetime
from ..models.drop import Drop

def run_expire_drops_job(db: Session):
    """
    Cancels open/matching drops that have passed their event target time without forming a Circle.
    """
    now = datetime.utcnow()
    stale_drops = db.query(Drop).filter(
        Drop.status.in_(["open", "matching"]),
        Drop.event_time < now
    ).all()

    count = 0
    for drop in stale_drops:
        drop.status = "cancelled"
        count += 1
        
    if count > 0:
        db.commit()
        print(f"[JOB] Cancelled {count} unfilled drops because their schedule target has passed.")
