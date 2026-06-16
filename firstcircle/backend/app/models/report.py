from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from ..database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    circle_id = Column(Integer, ForeignKey("circles.id", ondelete="CASCADE"), nullable=False)
    reporter_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    reportee_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String, default="pending") # 'pending', 'resolved', 'dismissed'
    created_at = Column(DateTime, server_default=func.now())

    circle = relationship("Circle")
    reporter = relationship("Profile", foreign_keys=[reporter_id])
    reportee = relationship("Profile", foreign_keys=[reportee_id])
