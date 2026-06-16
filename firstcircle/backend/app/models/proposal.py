from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from ..database import Base

class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    drop_id = Column(Integer, ForeignKey("drops.id", ondelete="CASCADE"), nullable=False)
    members_json = Column(Text, nullable=False) # JSON array: [1, 2, 3]
    votes_json = Column(Text, nullable=False)   # JSON object: {"1": "accept", "2": "pending"}
    status = Column(String, default="pending")  # 'pending', 'accepted', 'expired', 'skipped'
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    drop = relationship("Drop", back_populates="proposal")
