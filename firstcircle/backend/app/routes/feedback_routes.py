"""Feedback routes."""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas.feedback_schema import FeedbackCreate, FeedbackResponse
from app.services.feedback_service import (
    submit_feedback,
    get_circle_feedback,
    get_user_feedback_for_circle,
)

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.post("/", response_model=FeedbackResponse)
def submit_feedback_endpoint(
    feedback_data: FeedbackCreate,
    session: Session = Depends(get_session),
):
    """Submit feedback for a circle."""
    feedback = submit_feedback(feedback_data.model_dump(), session)
    return feedback


@router.get("/circle/{circle_id}", response_model=list[FeedbackResponse])
def get_circle_feedback_endpoint(
    circle_id: int, session: Session = Depends(get_session)
):
    """Get all feedback for a circle."""
    feedback_list = get_circle_feedback(circle_id, session)
    return feedback_list


@router.get("/circle/{circle_id}/user/{user_id}", response_model=FeedbackResponse)
def get_user_feedback_endpoint(
    circle_id: int,
    user_id: int,
    session: Session = Depends(get_session),
):
    """Get feedback from a user for a circle."""
    feedback = get_user_feedback_for_circle(circle_id, user_id, session)
    return feedback
