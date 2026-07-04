from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.drop import Drop
from app.models.user import User
from app.models.vibe_vote import VibeVote


def vote_on_vibe(drop_id: int, user_id: int, vibe_tag: str, vote_type: str, session: Session) -> VibeVote:
    """
    Vote up or down on a vibe tag for a drop.
    
    Business rules:
    - User and Drop must exist
    - One user can vote once per vibe_tag per drop
    - If same user votes again on same tag, update vote_type
    """
    # Validate user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate drop exists
    drop = session.get(Drop, drop_id)
    if not drop:
        raise HTTPException(status_code=404, detail="Drop not found")

    # Check for existing vote by this user on this tag
    existing_vote = session.exec(
        select(VibeVote).where(
            VibeVote.drop_id == drop_id,
            VibeVote.user_id == user_id,
            VibeVote.vibe_tag == vibe_tag,
        )
    ).first()

    if existing_vote:
        # Update existing vote
        existing_vote.vote_type = vote_type
        session.add(existing_vote)
        session.commit()
        session.refresh(existing_vote)
        return existing_vote

    # Create new vote
    vote = VibeVote(
        drop_id=drop_id,
        user_id=user_id,
        vibe_tag=vibe_tag,
        vote_type=vote_type,
    )
    session.add(vote)
    session.commit()
    session.refresh(vote)
    return vote


def get_vibe_votes_for_drop(drop_id: int, session: Session) -> list[VibeVote]:
    """
    Get all vibe votes for a drop.
    """
    drop = session.get(Drop, drop_id)
    if not drop:
        raise HTTPException(status_code=404, detail="Drop not found")

    votes = session.exec(
        select(VibeVote).where(VibeVote.drop_id == drop_id)
    ).all()

    return votes


def get_vibe_summary(drop_id: int, session: Session) -> dict:
    """
    Get a summary of vibe votes for a drop.
    
    Returns:
    {
        "drop_id": int,
        "summary": [
            {
                "vibe_tag": str,
                "upvotes": int,
                "downvotes": int,
                "net_votes": int
            },
            ...
        ]
    }
    """
    drop = session.get(Drop, drop_id)
    if not drop:
        raise HTTPException(status_code=404, detail="Drop not found")

    votes = session.exec(
        select(VibeVote).where(VibeVote.drop_id == drop_id)
    ).all()

    # Aggregate by vibe_tag
    vibe_summary = {}
    for vote in votes:
        if vote.vibe_tag not in vibe_summary:
            vibe_summary[vote.vibe_tag] = {"upvotes": 0, "downvotes": 0}

        if vote.vote_type == "up":
            vibe_summary[vote.vibe_tag]["upvotes"] += 1
        elif vote.vote_type == "down":
            vibe_summary[vote.vibe_tag]["downvotes"] += 1

    # Build result
    summary_items = []
    for vibe_tag, counts in vibe_summary.items():
        upvotes = counts["upvotes"]
        downvotes = counts["downvotes"]
        net_votes = upvotes - downvotes

        summary_items.append(
            {
                "vibe_tag": vibe_tag,
                "upvotes": upvotes,
                "downvotes": downvotes,
                "net_votes": net_votes,
            }
        )

    # Sort by net_votes descending
    summary_items.sort(key=lambda x: x["net_votes"], reverse=True)

    return {
        "drop_id": drop_id,
        "summary": summary_items,
    }
