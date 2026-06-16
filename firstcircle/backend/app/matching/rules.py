import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.soft_blacklist import SoftBlacklist
from ..models.profile import Profile

def check_hard_rules(db: Session, profile_ids: List[int], profiles: List[Profile]) -> bool:
    """
    Applies hard constraints. Returns True if the proposed group is valid.
    """
    if len(profile_ids) < 3:
        return False

    # 1. Soft Blacklist Exclusion
    # Check if any user in the group has blacklisted another user in the group
    blacklist_count = db.query(SoftBlacklist).filter(
        SoftBlacklist.user_id.in_(profile_ids),
        SoftBlacklist.blacklisted_user_id.in_(profile_ids)
    ).count()
    if blacklist_count > 0:
        return False

    # Create maps for quick access
    profile_map = {p.id: p for p in profiles}

    ages = [profile_map[pid].age for pid in profile_ids if profile_map[pid].age is not None]
    genders = [profile_map[pid].gender for pid in profile_ids if profile_map[pid].gender is not None]

    # 2. Age Gap Verification (Max 12 years gap constraint)
    if ages:
        if max(ages) - min(ages) > 12:
            return False

    # 3. Same Gender Preferences
    for pid in profile_ids:
        prof = profile_map[pid]
        if prof.comforts:
            try:
                comfort_data = json.loads(prof.comforts)
                if comfort_data.get("same_gender_only") is True:
                    # If this user wants same gender, verify all users have the same gender
                    if len(set(genders)) > 1:
                        return False
            except json.JSONDecodeError:
                pass

    return True
