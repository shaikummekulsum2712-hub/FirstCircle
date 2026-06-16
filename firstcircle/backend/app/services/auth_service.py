from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.user import User
from ..models.profile import Profile
from ..schemas.user_schema import UserCreate
from ..utils.security import get_password_hash, verify_password, create_access_token

def register_user(db: Session, user_data: UserCreate) -> User:
    # Check if user already exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Initialize blank profile
    display_name = user_data.email.split("@")[0].capitalize()
    new_profile = Profile(
        user_id=new_user.id,
        display_name=display_name,
        bio="Hello! I am new here.",
        age=25,
        gender="Other",
        reliability_score=100.0,
        interests="social,coffee",
        comforts='{"group_size_pref": 4, "same_gender_only": false}'
    )
    db.add(new_profile)
    db.commit()

    return new_user

def authenticate_user(db: Session, user_data: UserCreate) -> str:
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Generate token
    token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return token
