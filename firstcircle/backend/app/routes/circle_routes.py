"""Circle routes for confirmed circles."""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas.circle_schema import CircleCreate, CircleResponse
from app.services.circle_service import (
    create_circle_from_proposal,
    get_circle,
    get_user_circles,
    mark_circle_complete,
    set_attendance_status,
)

router = APIRouter(prefix="/api/circles", tags=["circles"])


@router.post("/from-proposal/{proposal_id}", response_model=CircleResponse)
def create_circle_endpoint(
    proposal_id: int,
    circle_data: CircleCreate,
    session: Session = Depends(get_session),
):
    """Create a confirmed circle from an accepted proposal."""
    circle = create_circle_from_proposal(
        proposal_id,
        circle_data.meeting_place,
        circle_data.meeting_date,
        circle_data.start_time,
        circle_data.end_time,
        session,
    )
    return circle


@router.get("/{circle_id}", response_model=CircleResponse)
def get_circle_endpoint(circle_id: int, session: Session = Depends(get_session)):
    """Get circle details."""
    circle = get_circle(circle_id, session)
    return circle


@router.get("/user/{user_id}", response_model=list[CircleResponse])
def get_user_circles_endpoint(user_id: int, session: Session = Depends(get_session)):
    """Get all circles for a user."""
    circles = get_user_circles(user_id, session)
    return circles


@router.patch("/{circle_id}/complete", response_model=CircleResponse)
def mark_complete_endpoint(circle_id: int, session: Session = Depends(get_session)):
    """Mark circle as completed."""
    circle = mark_circle_complete(circle_id, session)
    return circle


@router.patch("/{circle_id}/member/{user_id}/attendance", response_model=dict)
def set_attendance_endpoint(
    circle_id: int,
    user_id: int,
    attendance_status: str,
    session: Session = Depends(get_session),
):
    """Set attendance status for a circle member."""
    member = set_attendance_status(circle_id, user_id, attendance_status, session)
    return {"status": "success", "member_id": member.id}
