import json
from typing import List, Dict, Any
from datetime import datetime, time
from ..models.profile import Profile
from ..models.free_slot import FreeSlot
from ..ml.embedding_service import embedding_service
from ..ml.similarity import cosine_similarity

def calculate_time_overlap(slots_by_user: Dict[int, List[FreeSlot]]) -> int:
    """
    Returns the maximum overlap in minutes across all users on any single day of the week.
    If no overlap of >= 120 minutes (2 hours) exists, returns 0.
    """
    user_ids = list(slots_by_user.keys())
    if len(user_ids) < 2:
        return 0

    max_overlap_minutes = 0

    # Check each day of the week
    for day in range(7):
        # Find overlapping range for this day across all users
        overlap_start = None
        overlap_end = None
        has_overlap = True

        for uid in user_ids:
            user_slots = [s for s in slots_by_user[uid] if s.day_of_week == day]
            if not user_slots:
                has_overlap = False
                break
            
            # Find the slot with max coverage
            # For simplicity, intersect the union of slots
            # If multiple slots exist, we take the widest
            slot_start = min(s.start_time for s in user_slots)
            slot_end = max(s.end_time for s in user_slots)

            if overlap_start is None:
                overlap_start = slot_start
                overlap_end = slot_end
            else:
                overlap_start = max(overlap_start, slot_start)
                overlap_end = min(overlap_end, slot_end)

            if overlap_start >= overlap_end:
                has_overlap = False
                break

        if has_overlap and overlap_start is not None and overlap_end is not None:
            # Calculate overlap duration in minutes
            try:
                sh, sm = map(int, overlap_start.split(":"))
                eh, em = map(int, overlap_end.split(":"))
                duration = (eh * 60 + em) - (sh * 60 + sm)
                if duration >= 120:  # 2 hours threshold
                    max_overlap_minutes = max(max_overlap_minutes, duration)
            except ValueError:
                pass

    return max_overlap_minutes

def score_candidate_group(profiles: List[Profile], slots_by_user: Dict[int, List[FreeSlot]]) -> float:
    """
    Scores a group of users.
    Formula: S = w_i * InterestSimilarity + w_t * TimeOverlapMinutes/60 + w_r * AverageReliability
    """
    n = len(profiles)
    if n < 3:
        return -1000.0

    # 1. Interests Cosine Similarity
    # Build vocabulary of all profile interests
    doc_interests = []
    for p in profiles:
        interests_list = [t.strip().lower() for t in p.interests.split(",") if t.strip()] if p.interests else []
        doc_interests.append(interests_list)
    
    embedding_service.fit(doc_interests)
    vectors = [embedding_service.transform(doc) for doc in doc_interests]
    
    # Calculate average pairwise cosine similarity
    sim_sum = 0.0
    pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            sim_sum += cosine_similarity(vectors[i], vectors[j])
            pairs += 1
            
    avg_interest_sim = sim_sum / pairs if pairs > 0 else 0.0

    # 2. Time Overlap (in hours)
    overlap_minutes = calculate_time_overlap(slots_by_user)
    if overlap_minutes == 0:
        return -99999.0  # Hard rejection for no schedule match
    overlap_hours = overlap_minutes / 60.0

    # 3. Reliability Score
    reliability_scores = [p.reliability_score for p in profiles]
    avg_reliability = sum(reliability_scores) / len(reliability_scores)
    # Penalize extreme deviation in reliability (so high and low scorers aren't grouped randomly)
    dev_penalty = 0.0
    if len(reliability_scores) > 1:
        mean = sum(reliability_scores) / len(reliability_scores)
        variance = sum((x - mean) ** 2 for x in reliability_scores) / len(reliability_scores)
        std_dev = variance ** 0.5
        dev_penalty = std_dev / 10.0  # Subtle penalty for high deviation

    # Coefficients
    w_i = 40.0   # Interest weighting
    w_t = 10.0   # Time weighting (per hour)
    w_r = 0.5    # Reliability average weighting
    
    total_score = (w_i * avg_interest_sim) + (w_t * overlap_hours) + (w_r * avg_reliability) - dev_penalty
    return total_score
