from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas.vibe_vote_schema import VibeVoteCreate, VibeVoteResponse, VibeVoteSummary, VibeSummaryItem
from app.services.vibe_vote_service import (
    get_vibe_summary,
    get_vibe_votes_for_drop,
    vote_on_vibe,
)

router = APIRouter(prefix="/vibe-votes", tags=["Vibe Votes"])


@router.post("/", response_model=VibeVoteResponse)
def create_vibe_vote(
    vote_data: VibeVoteCreate,
    session: Session = Depends(get_session),
):
    """
    Vote on a vibe tag.
    
    Business rules:
    - One user can vote once per vibe_tag per drop
    - Voting again on same tag updates the vote_type
    """
    vote = vote_on_vibe(
        vote_data.drop_id,
        vote_data.user_id,
        vote_data.vibe_tag,
        vote_data.vote_type,
        session,
    )
    
    return VibeVoteResponse(
        id=vote.id,
        drop_id=vote.drop_id,
        user_id=vote.user_id,
        vibe_tag=vote.vibe_tag,
        vote_type=vote.vote_type,
        created_at=vote.created_at,
    )


@router.get("/drop/{drop_id}", response_model=list[VibeVoteResponse])
def get_drop_vibe_votes(
    drop_id: int,
    session: Session = Depends(get_session),
):
    """
    Get all vibe votes for a drop.
    """
    votes = get_vibe_votes_for_drop(drop_id, session)
    
    result = []
    for vote in votes:
        result.append(VibeVoteResponse(
            id=vote.id,
            drop_id=vote.drop_id,
            user_id=vote.user_id,
            vibe_tag=vote.vibe_tag,
            vote_type=vote.vote_type,
            created_at=vote.created_at,
        ))
    
    return result


@router.get("/drop/{drop_id}/summary", response_model=VibeVoteSummary)
def get_vibe_votes_summary(
    drop_id: int,
    session: Session = Depends(get_session),
):
    """
    Get a summary of vibe votes for a drop.
    
    Returns vibe tags with upvote/downvote counts and net votes.
    Sorted by net_votes descending.
    """
    summary = get_vibe_summary(drop_id, session)
    
    summary_items = [VibeSummaryItem(**item) for item in summary["summary"]]
    
    return VibeVoteSummary(
        drop_id=drop_id,
        summary=summary_items,
    )
