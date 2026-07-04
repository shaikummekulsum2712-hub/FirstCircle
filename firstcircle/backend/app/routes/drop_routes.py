from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.models.drop import Drop
from app.schemas.drop_schema import DropCreate, DropResponse
from app.services.drop_service import (
    cancel_drop,
    create_drop,
    expire_drop,
    get_all_drops,
    get_drop_by_id,
    get_drops_by_creator,
)

router = APIRouter(prefix="/drops", tags=["Drops"])


@router.post("/", response_model=DropResponse)
def create_new_drop(
    drop_data: DropCreate,
    session: Session = Depends(get_session),
):
    """
    Create a new circle drop.
    
    - creator_user_id: ID of the user creating the drop
    - location_id: ID of the safe campus location
    - max_members: between 2 and 8
    - vibe_tags: list of strings describing the vibe
    """
    drop = create_drop(drop_data, session)
    
    # Convert CSV string back to list for response
    vibe_tags = drop.vibe_tags.split(",") if drop.vibe_tags else []
    
    return DropResponse(
        id=drop.id,
        creator_user_id=drop.creator_user_id,
        title=drop.title,
        description=drop.description,
        circle_type=drop.circle_type,
        location_id=drop.location_id,
        scheduled_date=drop.scheduled_date,
        start_time=drop.start_time,
        end_time=drop.end_time,
        max_members=drop.max_members,
        current_members=drop.current_members,
        status=drop.status,
        urgency_level=drop.urgency_level,
        vibe_tags=vibe_tags,
        created_at=drop.created_at,
        expires_at=drop.expires_at,
    )


@router.get("/", response_model=list[DropResponse])
def get_drops(
    status: str = None,
    session: Session = Depends(get_session),
):
    """
    Get all drops, optionally filtered by status (open, full, expired, cancelled).
    """
    drops = get_all_drops(session, status)
    
    result = []
    for drop in drops:
        vibe_tags = drop.vibe_tags.split(",") if drop.vibe_tags else []
        result.append(DropResponse(
            id=drop.id,
            creator_user_id=drop.creator_user_id,
            title=drop.title,
            description=drop.description,
            circle_type=drop.circle_type,
            location_id=drop.location_id,
            scheduled_date=drop.scheduled_date,
            start_time=drop.start_time,
            end_time=drop.end_time,
            max_members=drop.max_members,
            current_members=drop.current_members,
            status=drop.status,
            urgency_level=drop.urgency_level,
            vibe_tags=vibe_tags,
            created_at=drop.created_at,
            expires_at=drop.expires_at,
        ))
    
    return result


@router.get("/{drop_id}", response_model=DropResponse)
def get_single_drop(
    drop_id: int,
    session: Session = Depends(get_session),
):
    """
    Get a single drop by ID.
    """
    drop = get_drop_by_id(drop_id, session)
    
    vibe_tags = drop.vibe_tags.split(",") if drop.vibe_tags else []
    
    return DropResponse(
        id=drop.id,
        creator_user_id=drop.creator_user_id,
        title=drop.title,
        description=drop.description,
        circle_type=drop.circle_type,
        location_id=drop.location_id,
        scheduled_date=drop.scheduled_date,
        start_time=drop.start_time,
        end_time=drop.end_time,
        max_members=drop.max_members,
        current_members=drop.current_members,
        status=drop.status,
        urgency_level=drop.urgency_level,
        vibe_tags=vibe_tags,
        created_at=drop.created_at,
        expires_at=drop.expires_at,
    )


@router.patch("/{drop_id}/expire", response_model=DropResponse)
def expire_drop_endpoint(
    drop_id: int,
    session: Session = Depends(get_session),
):
    """
    Mark a drop as expired.
    """
    drop = expire_drop(drop_id, session)
    
    vibe_tags = drop.vibe_tags.split(",") if drop.vibe_tags else []
    
    return DropResponse(
        id=drop.id,
        creator_user_id=drop.creator_user_id,
        title=drop.title,
        description=drop.description,
        circle_type=drop.circle_type,
        location_id=drop.location_id,
        scheduled_date=drop.scheduled_date,
        start_time=drop.start_time,
        end_time=drop.end_time,
        max_members=drop.max_members,
        current_members=drop.current_members,
        status=drop.status,
        urgency_level=drop.urgency_level,
        vibe_tags=vibe_tags,
        created_at=drop.created_at,
        expires_at=drop.expires_at,
    )


@router.patch("/{drop_id}/cancel", response_model=DropResponse)
def cancel_drop_endpoint(
    drop_id: int,
    session: Session = Depends(get_session),
):
    """
    Mark a drop as cancelled.
    """
    drop = cancel_drop(drop_id, session)
    
    vibe_tags = drop.vibe_tags.split(",") if drop.vibe_tags else []
    
    return DropResponse(
        id=drop.id,
        creator_user_id=drop.creator_user_id,
        title=drop.title,
        description=drop.description,
        circle_type=drop.circle_type,
        location_id=drop.location_id,
        scheduled_date=drop.scheduled_date,
        start_time=drop.start_time,
        end_time=drop.end_time,
        max_members=drop.max_members,
        current_members=drop.current_members,
        status=drop.status,
        urgency_level=drop.urgency_level,
        vibe_tags=vibe_tags,
        created_at=drop.created_at,
        expires_at=drop.expires_at,
    )


@router.get("/user/{user_id}", response_model=list[DropResponse])
def get_user_drops(
    user_id: int,
    session: Session = Depends(get_session),
):
    """
    Get all drops created by a specific user.
    """
    drops = get_drops_by_creator(user_id, session)
    
    result = []
    for drop in drops:
        vibe_tags = drop.vibe_tags.split(",") if drop.vibe_tags else []
        result.append(DropResponse(
            id=drop.id,
            creator_user_id=drop.creator_user_id,
            title=drop.title,
            description=drop.description,
            circle_type=drop.circle_type,
            location_id=drop.location_id,
            scheduled_date=drop.scheduled_date,
            start_time=drop.start_time,
            end_time=drop.end_time,
            max_members=drop.max_members,
            current_members=drop.current_members,
            status=drop.status,
            urgency_level=drop.urgency_level,
            vibe_tags=vibe_tags,
            created_at=drop.created_at,
            expires_at=drop.expires_at,
        ))
    
    return result
