import re
from fastapi import HTTPException, status

def validate_interests_string(interests: str):
    """
    Ensures interest lists contain alphanumeric and comma characters only.
    """
    if not interests:
        return
    
    if not re.match(r"^[a-zA-Z0-9,\s#-]+$", interests):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interests must contain only letters, numbers, spaces, hash tags, and commas."
        )

def validate_bio_length(bio: str):
    if bio and len(bio) > 300:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bio must be 300 characters or less."
        )
