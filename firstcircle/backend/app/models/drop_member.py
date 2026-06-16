from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class DropMember(Base):
    __tablename__ = "drop_members"

    id = Column(Integer, primary_key=True, index=True)
    drop_id = Column(Integer, ForeignKey("drops.id", ondelete="CASCADE"), nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    joined_at = Column(DateTime, server_default=func.now())

    drop = relationship("Drop", back_populates="members")
    profile = relationship("Profile")

    __table_args__ = (UniqueConstraint("drop_id", "profile_id", name="_drop_profile_uc"),)
