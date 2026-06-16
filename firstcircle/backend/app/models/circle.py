from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base

class Circle(Base):
    __tablename__ = "circles"

    id = Column(Integer, primary_key=True, index=True)
    drop_id = Column(Integer, ForeignKey("drops.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    event_time = Column(DateTime, nullable=False)
    location_name = Column(String, nullable=False)
    status = Column(String, default="scheduled") # 'scheduled', 'completed', 'rescheduled'
    created_at = Column(DateTime, server_default=func.now())

    drop = relationship("Drop", back_populates="circle")
    feedbacks = relationship("Feedback", back_populates="circle", cascade="all, delete-orphan")
