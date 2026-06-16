from sqlalchemy.orm import Session
from ..models.proposal import Proposal
import json

def get_fairness_boost(db: Session, profile_id: int) -> float:
    """
    Looks at past proposals. If the user was in proposals that ended up 'skipped'
    or 'expired', we boost their matching score to prevent them from being left out.
    """
    # Query proposals containing this user's profile ID
    proposals = db.query(Proposal).all()
    
    unsuccessful_count = 0
    
    for p in proposals:
        try:
            members = json.loads(p.members_json)
            if profile_id in members:
                # If the proposal was skipped or expired, count it
                if p.status in ["skipped", "expired"]:
                    unsuccessful_count += 1
        except (json.JSONDecodeError, TypeError):
            pass

    # Each failed match gives a small +3.0 score boost
    boost = float(unsuccessful_count * 3.0)
    # Cap boost at 15.0 to maintain matching sanity
    return min(boost, 15.0)
