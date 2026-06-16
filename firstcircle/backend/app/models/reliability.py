from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..database import Base

class ReliabilityHistory(Base):
    __tablename__ = "reliability_history"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String, nullable=False) # 'on-time', 'late', 'no-show'
    delta = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    profile = relationship("Profile")
