"""
Scoring module for auto-place matching.

Scoring rules (total: 100 points):
1. Circle type fit: 25 points
2. Time fit: 25 points
3. Profile fit: 20 points
4. Vibe fit: 15 points
5. Urgency/fill boost: 10 points
6. Fairness boost: 5 points
"""

from app.models.drop import Drop


def score_circle_type_fit(drop: Drop, preferred_circle_type: str) -> float:
    """
    Score circle type match.
    
    - exact match: 25 points
    - preferred is "any": 15 points
    - mismatch: 0 points
    """
    if preferred_circle_type == "any":
        return 15.0
    
    if drop.circle_type == preferred_circle_type:
        return 25.0
    
    return 0.0


def score_time_fit(drop: Drop, preferred_day: str, preferred_start_time: str, preferred_end_time: str) -> float:
    """
    Score time match.
    
    - exact day match and time overlap: 25 points
    - partial overlap or same day: 12 points
    - no overlap: 0 points
    
    Time overlap logic:
    - drop_start <= user_end AND drop_end >= user_start (overlap check)
    """
    if drop.scheduled_date != preferred_day:
        # Different day, no time fit
        return 0.0
    
    # Same day, check time overlap
    try:
        drop_start = drop.start_time
        drop_end = drop.end_time
        user_start = preferred_start_time
        user_end = preferred_end_time
        
        # Simple string comparison works for HH:MM format
        if drop_start <= user_end and drop_end >= user_start:
            # Exact match (both requested and drop on same day with overlap)
            return 25.0
        else:
            # Same day but no time overlap
            return 12.0
    except Exception:
        # Time parsing issue, give partial credit
        return 12.0


def score_profile_fit(drop: Drop, user_interests: list[str]) -> float:
    """
    Score profile fit using keyword matching.
    
    Compare user's interests/skills with drop vibe_tags, title, description.
    More shared terms = higher score (0-20 points).
    """
    if not user_interests:
        # No user interests, give neutral score
        return 10.0
    
    # Extract keywords from drop
    drop_keywords = set()
    
    # Add vibe tags
    if drop.vibe_tags:
        vibe_list = drop.vibe_tags.split(",")
        drop_keywords.update([v.strip().lower() for v in vibe_list])
    
    # Add title words (lowercase, skip short words)
    if drop.title:
        title_words = drop.title.lower().split()
        drop_keywords.update([w for w in title_words if len(w) > 3])
    
    # Add description words (lowercase, skip short words)
    if drop.description:
        desc_words = drop.description.lower().split()
        drop_keywords.update([w for w in desc_words if len(w) > 3])
    
    # Convert user interests to lowercase
    user_interests_lower = [i.lower() for i in user_interests]
    
    # Count matches
    matches = 0
    for interest in user_interests_lower:
        if interest in drop_keywords:
            matches += 1
    
    # Score: 0-20 based on match ratio
    if len(user_interests_lower) == 0:
        return 10.0
    
    match_ratio = matches / len(user_interests_lower)
    score = match_ratio * 20.0
    
    return min(score, 20.0)


def score_vibe_fit(drop: Drop, preferred_vibes: list[str]) -> float:
    """
    Score vibe overlap.
    
    Check overlap between preferred_vibes and drop vibe_tags (0-15 points).
    """
    if not preferred_vibes:
        # No vibe preference, neutral score
        return 7.5
    
    if not drop.vibe_tags:
        # Drop has no vibes, lower score
        return 0.0
    
    # Parse drop vibe tags
    drop_vibes = set([v.strip().lower() for v in drop.vibe_tags.split(",")])
    preferred_vibes_lower = set([v.lower() for v in preferred_vibes])
    
    # Count overlaps
    overlaps = len(drop_vibes.intersection(preferred_vibes_lower))
    
    if len(preferred_vibes_lower) == 0:
        return 0.0
    
    # Score: ratio of overlap * 15
    overlap_ratio = overlaps / len(preferred_vibes_lower)
    score = overlap_ratio * 15.0
    
    return min(score, 15.0)


def score_urgency_boost(drop: Drop) -> float:
    """
    Urgency/fill boost.
    
    Drops closer to full get more points, but full drops are excluded.
    Scale: 0-10 points based on current_members / max_members ratio.
    """
    if drop.max_members == 0:
        return 0.0
    
    fill_ratio = drop.current_members / drop.max_members
    
    # Score higher as drop fills up (but not at 100%)
    # Scale to 0-10
    if fill_ratio < 0.2:
        return 1.0
    elif fill_ratio < 0.4:
        return 3.0
    elif fill_ratio < 0.6:
        return 5.0
    elif fill_ratio < 0.8:
        return 7.0
    else:  # 0.8 - 0.99 (not full)
        return 10.0


def calculate_total_score(
    circle_type_fit: float,
    time_fit: float,
    profile_fit: float,
    vibe_fit: float,
    urgency_boost: float,
    fairness_boost: float,
) -> float:
    """
    Calculate total score (0-100).
    """
    total = (
        circle_type_fit +
        time_fit +
        profile_fit +
        vibe_fit +
        urgency_boost +
        fairness_boost
    )
    return min(total, 100.0)
