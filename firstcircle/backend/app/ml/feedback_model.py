from typing import Dict, Tuple

class DynamicFeedbackAffinities:
    """
    Tracks and refines user pair affinity multipliers based on historical rating feedback loops.
    """
    def __init__(self):
        # Maps (reviewer_id, reviewee_id) to affinity multiplier (default 1.0)
        self.affinities: Dict[Tuple[int, int], float] = {}

    def update_affinity(self, reviewer_id: int, reviewee_id: int, rating: int):
        """
        High ratings (> 3) scale up affinity.
        Low ratings (< 3) scale down affinity.
        """
        pair = (reviewer_id, reviewee_id)
        current = self.affinities.get(pair, 1.0)
        
        if rating >= 4:
            # Boost compatibility by 10% (cap at 1.5)
            self.affinities[pair] = min(current * 1.10, 1.5)
        elif rating <= 2:
            # Penalize compatibility by 30%
            self.affinities[pair] = max(current * 0.70, 0.2)
        else:
            # 3-star rating: Slight decay toward neutral
            self.affinities[pair] = current

    def get_affinity(self, reviewer_id: int, reviewee_id: int) -> float:
        return self.affinities.get((reviewer_id, reviewee_id), 1.0)

feedback_affinity_model = DynamicFeedbackAffinities()
