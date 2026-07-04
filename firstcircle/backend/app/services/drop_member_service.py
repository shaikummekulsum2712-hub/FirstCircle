from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.drop import Drop
from app.models.drop_member import DropMember
from app.models.user import User


def join_drop(drop_id: int, user_id: int, session: Session) -> DropMember:
    """
    Join a drop.
    
    Business rules:
    - User must exist
    - Drop must exist
    - Drop status must be open
    - User cannot join same drop twice
    - User cannot join their own created drop again (creator is already member)
    - If drop is full, reject join
    - When user joins, increment current_members
    - If current_members reaches max_members, status becomes full
    """
    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate drop exists
    drop = session.get(Drop, drop_id)
    if not drop:
        raise HTTPException(status_code=404, detail="Drop not found")

    # Check drop status is open
    if drop.status != "open":
        raise HTTPException(status_code=400, detail="Drop is not open for joining")

    # Check if drop is full
    if drop.current_members >= drop.max_members:
        raise HTTPException(status_code=400, detail="Drop is full")

    # Check if user is creator
    if drop.creator_user_id == user_id:
        raise HTTPException(status_code=400, detail="Creator is already member of their drop")

    # Check if already joined
    existing = session.exec(
        select(DropMember).where(
            DropMember.drop_id == drop_id,
            DropMember.user_id == user_id,
            DropMember.join_status == "joined",
        )
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already joined this drop")

    # Create member entry
    member = DropMember(
        drop_id=drop_id,
        user_id=user_id,
        role="member",
        join_status="joined",
    )
    session.add(member)

    # Increment current_members
    drop.current_members += 1

    # Check if now full
    if drop.current_members >= drop.max_members:
        drop.status = "full"

    session.add(drop)
    session.commit()
    session.refresh(member)
    return member


def leave_drop(drop_id: int, user_id: int, session: Session) -> dict:
    """
    Leave a drop.
    
    Business rules:
    - User must exist
    - Drop must exist
    - User must have been joined
    - Creator should not be allowed to leave (for MVP)
    - Decrement current_members only if user was joined
    """
    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate drop exists
    drop = session.get(Drop, drop_id)
    if not drop:
        raise HTTPException(status_code=404, detail="Drop not found")

    # Check if creator (should not allow)
    if drop.creator_user_id == user_id:
        raise HTTPException(status_code=400, detail="Creator cannot leave their drop")

    # Check if joined
    member = session.exec(
        select(DropMember).where(
            DropMember.drop_id == drop_id,
            DropMember.user_id == user_id,
            DropMember.join_status == "joined",
        )
    ).first()

    if not member:
        raise HTTPException(status_code=400, detail="User is not joined to this drop")

    # Mark as left
    member.join_status = "left"
    session.add(member)

    # Decrement current_members
    drop.current_members -= 1

    # If was full, now it's open
    if drop.status == "full":
        drop.status = "open"

    session.add(drop)
    session.commit()

    return {"message": "Successfully left drop"}


def get_drop_members(drop_id: int, session: Session) -> list[DropMember]:
    """
    Get all members joined to a drop.
    """
    drop = session.get(Drop, drop_id)
    if not drop:
        raise HTTPException(status_code=404, detail="Drop not found")

    members = session.exec(
        select(DropMember).where(
            DropMember.drop_id == drop_id,
            DropMember.join_status == "joined",
        )
    ).all()

    return members


def get_user_drops(user_id: int, session: Session) -> list[DropMember]:
    """
    Get all drops joined by a user.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    memberships = session.exec(
        select(DropMember).where(
            DropMember.user_id == user_id,
            DropMember.join_status == "joined",
        )
    ).all()

    return memberships
