from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas.drop_member_schema import DropMemberJoin, DropMemberLeave, DropMemberResponse
from app.services.drop_member_service import (
    get_drop_members,
    get_user_drops,
    join_drop,
    leave_drop,
)

router = APIRouter(prefix="/drop-members", tags=["Drop Members"])


@router.post("/join", response_model=DropMemberResponse)
def join_drop_endpoint(
    join_data: DropMemberJoin,
    session: Session = Depends(get_session),
):
    """
    Join a drop.
    
    Business rules:
    - Drop must be open
    - User cannot join twice
    - User cannot be drop creator
    - Drop cannot be full
    """
    member = join_drop(join_data.drop_id, join_data.user_id, session)
    
    return DropMemberResponse(
        id=member.id,
        drop_id=member.drop_id,
        user_id=member.user_id,
        role=member.role,
        join_status=member.join_status,
        joined_at=member.joined_at,
    )


@router.patch("/leave", response_model=dict)
def leave_drop_endpoint(
    leave_data: DropMemberLeave,
    session: Session = Depends(get_session),
):
    """
    Leave a drop.
    
    - Creator cannot leave (for MVP)
    - User must be currently joined
    """
    result = leave_drop(leave_data.drop_id, leave_data.user_id, session)
    return result


@router.get("/drop/{drop_id}", response_model=list[DropMemberResponse])
def get_drop_members_endpoint(
    drop_id: int,
    session: Session = Depends(get_session),
):
    """
    Get all members joined to a drop.
    """
    members = get_drop_members(drop_id, session)
    
    result = []
    for member in members:
        result.append(DropMemberResponse(
            id=member.id,
            drop_id=member.drop_id,
            user_id=member.user_id,
            role=member.role,
            join_status=member.join_status,
            joined_at=member.joined_at,
        ))
    
    return result


@router.get("/user/{user_id}", response_model=list[DropMemberResponse])
def get_user_drops_endpoint(
    user_id: int,
    session: Session = Depends(get_session),
):
    """
    Get all drops joined by a user.
    """
    memberships = get_user_drops(user_id, session)
    
    result = []
    for membership in memberships:
        result.append(DropMemberResponse(
            id=membership.id,
            drop_id=membership.drop_id,
            user_id=membership.user_id,
            role=membership.role,
            join_status=membership.join_status,
            joined_at=membership.joined_at,
        ))
    
    return result
