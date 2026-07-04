"""Circle service."""

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.circle import Circle
from app.models.circle_member import CircleMember
from app.models.proposal import Proposal
from app.models.proposal_participant import ProposalParticipant
from app.models.user import User


def create_circle_from_proposal(proposal_id: int, meeting_place: str, meeting_date: str, start_time: str, end_time: str, session: Session) -> Circle:
    """
    Create a confirmed circle from an accepted proposal.
    
    Reveal all members in the circle.
    """
    # Get proposal
    proposal = session.get(Proposal, proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    if proposal.status != "accepted":
        raise HTTPException(status_code=400, detail="Proposal must be accepted first")

    # Create circle
    circle = Circle(
        drop_id=proposal.drop_id,
        proposal_id=proposal_id,
        status="confirmed",
        meeting_place=meeting_place,
        meeting_date=meeting_date,
        start_time=start_time,
        end_time=end_time,
    )
    session.add(circle)
    session.commit()
    session.refresh(circle)

    # Get all accepted participants from proposal
    participants = session.exec(
        select(ProposalParticipant).where(
            ProposalParticipant.proposal_id == proposal_id,
            ProposalParticipant.response_status == "accepted",
        )
    ).all()

    # Create circle members with revealed=True
    for p in participants:
        member = CircleMember(
            circle_id=circle.id,
            user_id=p.user_id,
            attendance_status="unknown",
            revealed=True,
        )
        session.add(member)

    session.commit()
    return circle


def get_circle(circle_id: int, session: Session) -> Circle:
    """Get a circle by ID."""
    circle = session.get(Circle, circle_id)
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")
    return circle


def get_user_circles(user_id: int, session: Session) -> list[Circle]:
    """Get all circles a user is in."""
    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get circles where user is a member
    members = session.exec(
        select(CircleMember).where(CircleMember.user_id == user_id)
    ).all()

    circles = []
    for m in members:
        circle = session.get(Circle, m.circle_id)
        if circle:
            circles.append(circle)

    return circles


def mark_circle_complete(circle_id: int, session: Session) -> Circle:
    """Mark a circle as completed."""
    circle = get_circle(circle_id, session)
    circle.status = "completed"
    session.add(circle)
    session.commit()
    session.refresh(circle)
    return circle


def set_attendance_status(circle_id: int, user_id: int, status: str, session: Session) -> CircleMember:
    """Set attendance status for a circle member."""
    # Get circle member
    member = session.exec(
        select(CircleMember).where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == user_id,
        )
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found in circle")

    member.attendance_status = status
    session.add(member)
    session.commit()
    session.refresh(member)
    return member
