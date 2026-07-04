from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.free_slot import FreeSlot
from app.models.user import User
from app.schemas.free_slot_schema import FreeSlotCreate, FreeSlotRead

router = APIRouter(prefix="/free-slots", tags=["Free Slots"])


@router.post("/", response_model=FreeSlotRead)
def create_free_slot(
    slot_data: FreeSlotCreate,
    session: Session = Depends(get_session),
):
    user = session.get(User, slot_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    slot = FreeSlot(**slot_data.model_dump())

    session.add(slot)
    session.commit()
    session.refresh(slot)

    return slot


@router.get("/user/{user_id}", response_model=list[FreeSlotRead])
def get_user_free_slots(
    user_id: int,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    statement = select(FreeSlot).where(FreeSlot.user_id == user_id)
    slots = session.exec(statement).all()

    return slots


@router.delete("/{slot_id}")
def delete_free_slot(
    slot_id: int,
    session: Session = Depends(get_session),
):
    slot = session.get(FreeSlot, slot_id)

    if not slot:
        raise HTTPException(status_code=404, detail="Free slot not found")

    session.delete(slot)
    session.commit()

    return {"message": "Free slot deleted successfully"}