from sqlalchemy.orm import Session
from ..services.cleanup_service import expire_pending_proposals

def run_proposal_expiry_job(db: Session):
    count = expire_pending_proposals(db)
    if count > 0:
        print(f"[JOB] Expired {count} pending matching proposals due to voter timeout.")
