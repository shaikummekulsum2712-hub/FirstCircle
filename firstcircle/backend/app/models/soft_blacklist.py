from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class SoftBlacklist(Base):
    __tablename__ = "soft_blacklists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    blacklisted_user_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("Profile", foreign_keys=[user_id])
    blacklisted_user = relationship("Profile", foreign_keys=[blacklisted_user_id])

    __table_args__ = (UniqueConstraint("user_id", "blacklisted_user_id", name="_blacklist_uc"),)
