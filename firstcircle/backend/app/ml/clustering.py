import random
from typing import List, Dict, Tuple
from .similarity import cosine_similarity

class SimpleKMeans:
    """
    A pure-Python K-Means clustering algorithm.
    """
    def __init__(self, k: int = 3, max_iter: int = 20):
        self.k = k
        self.max_iter = max_iter
        self.centroids: List[List[float]] = []

    def fit_predict(self, data: List[Tuple[int, List[float]]]) -> Dict[int, List[int]]:
        """
        data: List of tuples (profile_id, vector)
        Returns a dictionary mapping cluster index (0 to K-1) to list of profile_id's.
        """
        if not data:
            return {}
        
        # If there are fewer elements than K, group them in a single cluster or separate ones
        n_samples = len(data)
        k = min(self.k, n_samples)
        
        # Randomly choose initial centroids
        selected = random.sample(data, k)
        self.centroids = [list(item[1]) for item in selected]
        
        cluster_assignments = {}
        
        for _ in range(self.max_iter):
            # Assign points to nearest centroid (using cosine similarity -> highest similarity)
            new_assignments: Dict[int, List[int]] = {i: [] for i in range(k)}
            for profile_id, vector in data:
                best_sim = -1.0
                best_centroid_idx = 0
                for c_idx, centroid in enumerate(self.centroids):
                    sim = cosine_similarity(vector, centroid)
                    if sim > best_sim:
                        best_sim = sim
                        best_centroid_idx = c_idx
                new_assignments[best_centroid_idx].append(profile_id)
            
            # Check convergence (if assignments didn't change)
            if new_assignments == cluster_assignments:
                break
            cluster_assignments = new_assignments
            
            # Recompute centroids
            for c_idx in range(k):
                assigned_profile_ids = cluster_assignments[c_idx]
                if not assigned_profile_ids:
                    continue
                
                # Find the profiles' vectors
                assigned_vectors = [vec for pid, vec in data if pid in assigned_profile_ids]
                vector_len = len(assigned_vectors[0])
                
                new_centroid = [0.0] * vector_len
                for vec in assigned_vectors:
                    for d_idx in range(vector_len):
                        new_centroid[d_idx] += vec[d_idx]
                
                self.centroids[c_idx] = [val / len(assigned_vectors) for val in new_centroid]
                
        return cluster_assignments

clustering_service = SimpleKMeans()
