from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserRead
from app.utils.validators import (
    extract_email_domain,
    is_allowed_college_email,
    is_valid_roll_number,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
):
    if not is_allowed_college_email(user_data.email):
        raise HTTPException(
            status_code=400,
            detail="Email domain is not allowed for this MVP",
        )

    if not is_valid_roll_number(user_data.roll_number):
        raise HTTPException(
            status_code=400,
            detail="Invalid roll number format",
        )

    existing_email = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_roll = session.exec(
        select(User).where(User.roll_number == user_data.roll_number)
    ).first()

    if existing_roll:
        raise HTTPException(status_code=400, detail="Roll number already registered")

    user = User(
        name=user_data.name,
        email=user_data.email.lower().strip(),
        roll_number=user_data.roll_number.upper().strip(),
        college_domain=extract_email_domain(user_data.email),
        email_verified=False,
        verification_status="pending",
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get("/", response_model=list[UserRead])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.patch("/{user_id}/verify-email", response_model=UserRead)
def mark_email_verified(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email_verified = True
    user.verification_status = "email_verified"

    session.add(user)
    session.commit()
    session.refresh(user)

    return user