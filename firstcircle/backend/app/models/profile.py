from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    bio = Column(Text)
    age = Column(Integer)
    gender = Column(String)
    reliability_score = Column(Float, default=100.0)
    interests = Column(Text)  # Comma-separated tags, e.g., "tech,boardgames"
    comforts = Column(Text)   # JSON string for preferences

    user = relationship("User", back_populates="profile")
    free_slots = relationship("FreeSlot", back_populates="profile", cascade="all, delete-orphan")
