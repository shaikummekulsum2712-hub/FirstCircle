from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    circle_id = Column(Integer, ForeignKey("circles.id", ondelete="CASCADE"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    reviewee_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    tags = Column(String) # Comma-separated descriptors, e.g. "punctual,quiet"
    created_at = Column(DateTime, server_default=func.now())

    circle = relationship("Circle", back_populates="feedbacks")
    reviewer = relationship("Profile", foreign_keys=[reviewer_id])
    reviewee = relationship("Profile", foreign_keys=[reviewee_id])
