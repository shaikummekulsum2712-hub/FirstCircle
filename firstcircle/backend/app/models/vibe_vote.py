from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class VibeVote(Base):
    __tablename__ = "vibe_votes"

    id = Column(Integer, primary_key=True, index=True)
    drop_id = Column(Integer, ForeignKey("drops.id", ondelete="CASCADE"), nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    vibe_value = Column(String, nullable=False) # e.g. 'chill', 'active', 'party', 'intellectual'

    drop = relationship("Drop", back_populates="vibe_votes")
    profile = relationship("Profile")

    __table_args__ = (UniqueConstraint("drop_id", "profile_id", name="_vibe_vote_uc"),)
