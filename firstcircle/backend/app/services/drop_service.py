from datetime import datetime

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.drop import Drop
from app.models.location import Location
from app.models.user import User


def create_drop(drop_data, session: Session) -> Drop:
    """
    Create a new drop.
    
    Business rules:
    - creator_user_id must exist
    - location_id must exist and must be safe
    - status starts as open
    - current_members starts at 1 (creator)
    """
    # Validate creator exists
    creator = session.get(User, drop_data.creator_user_id)
    if not creator:
        raise HTTPException(status_code=404, detail="Creator user not found")

    # Validate location exists and is safe
    location = session.get(Location, drop_data.location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    if not location.is_safe:
        raise HTTPException(status_code=400, detail="Location is not safe")

    # Convert vibe_tags list to CSV string
    vibe_tags_csv = ",".join(drop_data.vibe_tags) if drop_data.vibe_tags else ""

    # Create drop
    drop = Drop(
        creator_user_id=drop_data.creator_user_id,
        title=drop_data.title,
        description=drop_data.description,
        circle_type=drop_data.circle_type,
        location_id=drop_data.location_id,
        scheduled_date=drop_data.scheduled_date,
        start_time=drop_data.start_time,
        end_time=drop_data.end_time,
        max_members=drop_data.max_members,
        current_members=1,
        status="open",
        urgency_level=drop_data.urgency_level,
        vibe_tags=vibe_tags_csv,
        expires_at=drop_data.expires_at,
    )

    session.add(drop)
    session.commit()
    session.refresh(drop)
    return drop


def get_all_drops(session: Session, status: str = None) -> list[Drop]:
    """
    Get all drops, optionally filtered by status.
    """
    statement = select(Drop)
    if status:
        statement = statement.where(Drop.status == status)
    drops = session.exec(statement).all()
    return drops


def get_drop_by_id(drop_id: int, session: Session) -> Drop:
    """
    Get a drop by ID. Raises 404 if not found.
    """
    drop = session.get(Drop, drop_id)
    if not drop:
        raise HTTPException(status_code=404, detail="Drop not found")
    return drop


def get_drops_by_creator(creator_user_id: int, session: Session) -> list[Drop]:
    """
    Get all drops created by a specific user.
    """
    statement = select(Drop).where(Drop.creator_user_id == creator_user_id)
    drops = session.exec(statement).all()
    return drops


def expire_drop(drop_id: int, session: Session) -> Drop:
    """
    Mark a drop as expired.
    """
    drop = get_drop_by_id(drop_id, session)
    drop.status = "expired"
    session.add(drop)
    session.commit()
    session.refresh(drop)
    return drop


def cancel_drop(drop_id: int, session: Session) -> Drop:
    """
    Mark a drop as cancelled.
    """
    drop = get_drop_by_id(drop_id, session)
    drop.status = "cancelled"
    session.add(drop)
    session.commit()
    session.refresh(drop)
    return drop


def update_drop_status_if_full(drop_id: int, session: Session) -> Drop:
    """
    Check if current_members >= max_members and update status to full if so.
    """
    drop = get_drop_by_id(drop_id, session)
    if drop.current_members >= drop.max_members:
        drop.status = "full"
        session.add(drop)
        session.commit()
        session.refresh(drop)
    return drop
