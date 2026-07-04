"""
Auto-place matching orchestration.

Finds the best open drop for a user based on preferences and scoring rules.
"""

from sqlmodel import Session, select

from app.models.drop import Drop
from app.models.drop_member import DropMember
from app.models.location import Location
from app.models.user import User
from app.matching.fairness import get_fairness_boost
from app.matching.scoring import (
    calculate_total_score,
    score_circle_type_fit,
    score_profile_fit,
    score_time_fit,
    score_urgency_boost,
    score_vibe_fit,
)


def find_best_drop(
    user_id: int,
    preferred_circle_type: str,
    preferred_day: str,
    preferred_start_time: str,
    preferred_end_time: str,
    preferred_vibes: list[str],
    session: Session,
) -> tuple[Drop, dict]:
    """
    Find the best open drop for a user.
    
    Returns: (best_drop, score_breakdown_dict)
    
    Excludes:
    - Drops created by same user
    - Drops already joined by user
    - Full/expired/cancelled drops
    - Unsafe locations
    
    Scores drops and returns the highest scoring one.
    """
    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        return None, {"error": "User not found"}

    # Get all open drops
    statement = select(Drop).where(Drop.status == "open")
    all_drops = session.exec(statement).all()

    if not all_drops:
        return None, {"error": "No open drops available"}

    # Filter drops
    candidate_drops = []
    for drop in all_drops:
        # Exclude creator's own drops
        if drop.creator_user_id == user_id:
            continue

        # Exclude already joined
        already_joined = session.exec(
            select(DropMember).where(
                DropMember.drop_id == drop.id,
                DropMember.user_id == user_id,
                DropMember.join_status == "joined",
            )
        ).first()
        if already_joined:
            continue

        # Exclude if location is unsafe
        location = session.get(Location, drop.location_id)
        if not location or not location.is_safe:
            continue

        candidate_drops.append(drop)

    if not candidate_drops:
        return None, {"error": "No suitable drops found after filtering"}

    # Score each drop
    best_drop = None
    best_score = -1.0
    best_breakdown = None

    # Get user profile interests (optional, for profile fit scoring)
    user_interests = []
    # For MVP, we'll use an empty list if profile/interests not available

    for drop in candidate_drops:
        # Calculate scores
        circle_type_fit = score_circle_type_fit(drop, preferred_circle_type)
        time_fit = score_time_fit(drop, preferred_day, preferred_start_time, preferred_end_time)
        profile_fit = score_profile_fit(drop, user_interests)
        vibe_fit = score_vibe_fit(drop, preferred_vibes)
        urgency_boost = score_urgency_boost(drop)
        fairness_boost = get_fairness_boost(user_id, session)

        total_score = calculate_total_score(
            circle_type_fit,
            time_fit,
            profile_fit,
            vibe_fit,
            urgency_boost,
            fairness_boost,
        )

        # Track best drop
        if total_score > best_score:
            best_score = total_score
            best_drop = drop
            best_breakdown = {
                "circle_type_fit": round(circle_type_fit, 2),
                "time_fit": round(time_fit, 2),
                "profile_fit": round(profile_fit, 2),
                "vibe_fit": round(vibe_fit, 2),
                "urgency_boost": round(urgency_boost, 2),
                "fairness_boost": round(fairness_boost, 2),
                "total": round(total_score, 2),
            }

    if best_drop is None:
        return None, {"error": "Could not score any drops"}

    return best_drop, best_breakdown
