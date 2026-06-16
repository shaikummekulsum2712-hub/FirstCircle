from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict
from ..models.profile import Profile
from ..models.free_slot import FreeSlot
from ..models.drop import Drop
from ..models.drop_member import DropMember
from ..models.proposal import Proposal
from ..ml.embedding_service import embedding_service
from ..ml.clustering import clustering_service
from .group_builder import build_best_matching_group

def run_auto_place_matching(db: Session, target_category: str = "Social", target_date_str: str = "2026-06-20") -> int:
    """
    Finds inactive users with calendar slots on the target day, clusters them by interests,
    and automatically schedules dynamic drops and blind proposals.
    Returns the count of created dynamic drops.
    """
    # 1. Fetch all profiles who are not already in a pending proposal or confirmed circle
    # For simplicity in this local version, we fetch all profiles
    profiles = db.query(Profile).all()
    if len(profiles) < 3:
        return 0

    # 2. Extract profile vectors for clustering
    doc_interests = []
    for p in profiles:
        interests_list = [t.strip().lower() for t in p.interests.split(",") if t.strip()] if p.interests else []
        doc_interests.append(interests_list)
        
    embedding_service.fit(doc_interests)
    
    data_points = []
    for p, doc in zip(profiles, doc_interests):
        vector = embedding_service.transform(doc)
        data_points.append((p.id, vector))

    # Cluster profiles (target 3 groups)
    clusters = clustering_service.fit_predict(data_points)
    drops_created = 0

    # For each cluster, try to find a valid sub-group with schedule overlap
    for c_idx, member_ids in clusters.items():
        if len(member_ids) < 3:
            continue
        
        cluster_profiles = [p for p in profiles if p.id in member_ids]
        
        # Load free slots for these profiles
        slots = db.query(FreeSlot).filter(FreeSlot.profile_id.in_(member_ids)).all()
        slots_by_user: Dict[int, List[FreeSlot]] = {pid: [] for pid in member_ids}
        for s in slots:
            slots_by_user[s.profile_id].append(s)

        # Build best group
        best_group_ids, score = build_best_matching_group(
            db, cluster_profiles, slots_by_user, min_size=3, max_size=5
        )

        if len(best_group_ids) >= 3 and score > 0:
            # We found a group! Let's generate a dynamic Drop
            # Find the overlapping slot day to set target time
            # For simplicity, default to the Saturday evening or the day matching target_date_str
            event_time = datetime.strptime(f"{target_date_str} 18:00:00", "%Y-%m-%d %H:%M:%S")
            
            # Create Drop
            new_drop = Drop(
                host_id=best_group_ids[0],
                title=f"Auto Connect: {target_category} Drop",
                description="This drop was auto-created by the matching engine based on your shared availability and interests.",
                category=target_category,
                event_time=event_time,
                location_name="Centrally Selected Coffee Shop",
                max_members=len(best_group_ids),
                status="matching"
            )
            db.add(new_drop)
            db.commit()
            db.refresh(new_drop)

            # Add members
            for pid in best_group_ids:
                member_join = DropMember(drop_id=new_drop.id, profile_id=pid)
                db.add(member_join)

            # Generate blind Proposal
            votes = {str(pid): "pending" for pid in best_group_ids}
            new_proposal = Proposal(
                drop_id=new_drop.id,
                members_json=str(best_group_ids),
                votes_json=str(votes).replace("'", '"'),
                status="pending",
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            db.add(new_proposal)
            db.commit()
            drops_created += 1

    return drops_created
