"""
Fairness boost module for auto-place matching.

Simple MVP fairness: users with fewer joined drops get a small boost.
"""

from sqlmodel import Session, select

from app.models.drop_member import DropMember


def get_fairness_boost(user_id: int, session: Session) -> float:
    """
    Fairness boost.
    
    Users with fewer joined drops get a small boost (0-5 points).
    
    - 0 drops joined: 5.0 bonus
    - 1-2 drops joined: 3.0 bonus
    - 3+ drops joined: 1.0 bonus
    """
    # Count drops joined by user
    joined_count = session.exec(
        select(DropMember).where(
            DropMember.user_id == user_id,
            DropMember.join_status == "joined",
        )
    ).all()
    
    drops_joined = len(joined_count)
    
    if drops_joined == 0:
        return 5.0
    elif drops_joined <= 2:
        return 3.0
    else:
        return 1.0
