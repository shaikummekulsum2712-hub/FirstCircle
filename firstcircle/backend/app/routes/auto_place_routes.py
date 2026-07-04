from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.matching.auto_place import find_best_drop
from app.schemas.auto_place_schema import AutoPlaceRequest, AutoPlaceResponse, DropRecommendation, ScoreBreakdown

router = APIRouter(prefix="/auto-place", tags=["Auto-place"])


@router.post("/suggest", response_model=AutoPlaceResponse)
def suggest_drop(
    request: AutoPlaceRequest,
    session: Session = Depends(get_session),
):
    """
    Auto-place API: Suggest the best open drop for a user.
    
    Request parameters:
    - user_id: ID of the user
    - preferred_circle_type: friend/study/build/random/any
    - preferred_day: YYYY-MM-DD
    - preferred_start_time: HH:MM
    - preferred_end_time: HH:MM
    - preferred_vibes: list of vibe tags (optional)
    
    Returns:
    - recommended_drop: the best drop found
    - score: total score (0-100)
    - score_breakdown: breakdown of all scoring components
    - reason: human-readable reason
    """
    # Find best drop
    best_drop, breakdown = find_best_drop(
        request.user_id,
        request.preferred_circle_type,
        request.preferred_day,
        request.preferred_start_time,
        request.preferred_end_time,
        request.preferred_vibes,
        session,
    )

    # Handle no match found
    if best_drop is None:
        if "error" in breakdown:
            return AutoPlaceResponse(
                recommended_drop=None,
                score=None,
                score_breakdown=None,
                reason=breakdown.get("error", "No suitable drops found"),
            )
        return AutoPlaceResponse(
            recommended_drop=None,
            score=None,
            score_breakdown=None,
            reason="Could not find a suitable drop for your preferences",
        )

    # Convert vibe_tags CSV to list
    vibe_tags = best_drop.vibe_tags.split(",") if best_drop.vibe_tags else []

    # Build response
    recommended = DropRecommendation(
        drop_id=best_drop.id,
        title=best_drop.title,
        description=best_drop.description,
        circle_type=best_drop.circle_type,
        scheduled_date=best_drop.scheduled_date,
        start_time=best_drop.start_time,
        end_time=best_drop.end_time,
        location_id=best_drop.location_id,
        current_members=best_drop.current_members,
        max_members=best_drop.max_members,
        creator_user_id=best_drop.creator_user_id,
        vibe_tags=vibe_tags,
    )

    score_breakdown = ScoreBreakdown(
        circle_type_fit=breakdown["circle_type_fit"],
        time_fit=breakdown["time_fit"],
        profile_fit=breakdown["profile_fit"],
        vibe_fit=breakdown["vibe_fit"],
        urgency_boost=breakdown["urgency_boost"],
        fairness_boost=breakdown["fairness_boost"],
        total=breakdown["total"],
    )

    # Build reason
    reason = f"This drop is a great match! {best_drop.current_members}/{best_drop.max_members} spots filled. "
    reason += f"Circle type: {best_drop.circle_type}, Time: {best_drop.start_time}-{best_drop.end_time}"

    return AutoPlaceResponse(
        recommended_drop=recommended,
        score=breakdown["total"],
        score_breakdown=score_breakdown,
        reason=reason,
    )
