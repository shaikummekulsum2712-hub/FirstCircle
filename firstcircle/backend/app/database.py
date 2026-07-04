from sqlmodel import SQLModel, Session, create_engine

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.APP_ENV == "development",
    connect_args={"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {},
)


def create_db_and_tables():
    from app.models.location import Location  # noqa: F401
    from app.models.user import User  # noqa: F401
    from app.models.profile import Profile  # noqa: F401
    from app.models.free_slot import FreeSlot  # noqa: F401
    from app.models.drop import Drop  # noqa: F401
    from app.models.drop_member import DropMember  # noqa: F401
    from app.models.vibe_vote import VibeVote  # noqa: F401
    from app.models.proposal import Proposal  # noqa: F401
    from app.models.proposal_participant import ProposalParticipant  # noqa: F401
    from app.models.soft_blacklist import SoftBlacklist  # noqa: F401
    from app.models.circle import Circle  # noqa: F401
    from app.models.circle_member import CircleMember  # noqa: F401
    from app.models.feedback import Feedback  # noqa: F401
    from app.models.report import Report  # noqa: F401
    from app.models.reliability import Reliability  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session