import itertools
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from ..models.profile import Profile
from ..models.free_slot import FreeSlot
from .rules import check_hard_rules
from .scoring import score_candidate_group

def build_best_matching_group(
    db: Session,
    joined_profiles: List[Profile],
    slots_by_user: Dict[int, List[FreeSlot]],
    min_size: int = 3,
    max_size: int = 5
) -> Tuple[List[int], float]:
    """
    Finds the highest-scoring combination of members of size [min_size, max_size].
    Returns (list_of_profile_ids, group_score).
    """
    if len(joined_profiles) < min_size:
        return [], 0.0

    best_group: List[int] = []
    best_score = -999999.0

    # Test combinations of sizes from min_size to max_size
    for size in range(min_size, min(len(joined_profiles) + 1, max_size + 1)):
        for combo in itertools.combinations(joined_profiles, size):
            combo_list = list(combo)
            combo_ids = [p.id for p in combo_list]

            # 1. Apply Hard Rules
            if not check_hard_rules(db, combo_ids, joined_profiles):
                continue

            # 2. Score Group
            combo_slots = {pid: slots_by_user[pid] for pid in combo_ids}
            score = score_candidate_group(combo_list, combo_slots)

            if score > best_score:
                best_score = score
                best_group = combo_ids

    return best_group, best_score
