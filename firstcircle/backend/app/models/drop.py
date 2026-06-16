from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from ..database import Base

class Drop(Base):
    __tablename__ = "drops"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, nullable=False)
    event_time = Column(DateTime, nullable=False)
    location_name = Column(String, nullable=False)
    max_members = Column(Integer, default=5)
    status = Column(String, default="open") # 'open', 'matching', 'completed', 'cancelled'
    created_at = Column(DateTime, server_default=func.now())

    members = relationship("DropMember", back_populates="drop", cascade="all, delete-orphan")
    vibe_votes = relationship("VibeVote", back_populates="drop", cascade="all, delete-orphan")
    proposal = relationship("Proposal", back_populates="drop", uselist=False, cascade="all, delete-orphan")
    circle = relationship("Circle", back_populates="drop", uselist=False, cascade="all, delete-orphan")
