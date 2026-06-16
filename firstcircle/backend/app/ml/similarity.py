import math
from typing import List

def dot_product(v1: List[float], v2: List[float]) -> float:
    return sum(x * y for x, y in zip(v1, v2))

def magnitude(v: List[float]) -> float:
    return math.sqrt(sum(x * x for x in v))

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """
    Computes cosine similarity between two lists of floats.
    Returns 0.0 if vectors are empty or have a magnitude of 0.
    """
    if len(v1) != len(v2) or len(v1) == 0:
        return 0.0
    
    mag1 = magnitude(v1)
    mag2 = magnitude(v2)
    
    if mag1 == 0.0 or mag2 == 0.0:
        return 0.0
        
    return dot_product(v1, v2) / (mag1 * mag2)
