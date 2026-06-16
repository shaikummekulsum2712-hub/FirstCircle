from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class FreeSlot(Base):
    __tablename__ = "free_slots"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(Integer, nullable=False) # 0 = Monday, 6 = Sunday
    start_time = Column(String, nullable=False)    # "HH:MM"
    end_time = Column(String, nullable=False)      # "HH:MM"

    profile = relationship("Profile", back_populates="free_slots")
