"""Feedback service."""

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.circle import Circle
from app.models.feedback import Feedback
from app.models.user import User


def submit_feedback(feedback_data: dict, session: Session) -> Feedback:
    """
    Submit feedback for a circle from a user.
    
    Only one feedback per user per circle.
    """
    circle_id = feedback_data["circle_id"]
    user_id = feedback_data["user_id"]

    # Validate circle exists
    circle = session.get(Circle, circle_id)
    if not circle:
        raise HTTPException(status_code=404, detail="Circle not found")

    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if feedback already submitted
    existing = session.exec(
        select(Feedback).where(
            Feedback.circle_id == circle_id,
            Feedback.user_id == user_id,
        )
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Feedback already submitted by this user for this circle")

    # Create feedback
    feedback = Feedback(
        circle_id=circle_id,
        user_id=user_id,
        rating=feedback_data.get("rating"),
        vibe_match=feedback_data.get("vibe_match", False),
        felt_safe=feedback_data.get("felt_safe", False),
        would_meet_again=feedback_data.get("would_meet_again", False),
        comment=feedback_data.get("comment", ""),
    )
    session.add(feedback)
    session.commit()
    session.refresh(feedback)
    return feedback


def get_circle_feedback(circle_id: int, session: Session) -> list[Feedback]:
    """Get all feedback for a circle."""
    feedback_list = session.exec(
        select(Feedback).where(Feedback.circle_id == circle_id)
    ).all()
    return feedback_list


def get_user_feedback_for_circle(circle_id: int, user_id: int, session: Session) -> Feedback:
    """Get feedback submitted by a user for a circle."""
    feedback = session.exec(
        select(Feedback).where(
            Feedback.circle_id == circle_id,
            Feedback.user_id == user_id,
        )
    ).first()

    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    return feedback
