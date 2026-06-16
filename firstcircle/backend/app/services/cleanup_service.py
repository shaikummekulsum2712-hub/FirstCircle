import json
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.proposal import Proposal
from ..models.drop import Drop
from .reliability_service import update_user_reliability

def expire_pending_proposals(db: Session) -> int:
    """
    Finds pending proposals that have passed their expires_at time limit.
    Sets them to 'expired' and penalizes users who failed to vote ('pending' voters)
    by deducting reliability points (-10 points for failing to respond).
    """
    now = datetime.utcnow()
    expired_proposals = db.query(Proposal).filter(
        Proposal.status == "pending",
        Proposal.expires_at < now
    ).all()
    
    count = 0
    for p in expired_proposals:
        p.status = "expired"
        
        # Penalize non-responsive users
        try:
            votes = json.loads(p.votes_json)
            for profile_str, vote_val in votes.items():
                if vote_val == "pending":
                    # Deduct 10 points for holding up matching
                    update_user_reliability(db, int(profile_str), "expired-timeout", -10.0)
        except json.JSONDecodeError:
            pass

        # Revert the drop status so matching can restart
        drop = db.query(Drop).filter(Drop.id == p.drop_id).first()
        if drop:
            drop.status = "open"
            
        count += 1
        
    if count > 0:
        db.commit()
        
    return count
