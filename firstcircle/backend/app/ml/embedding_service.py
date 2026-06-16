import math
from typing import List, Dict

class SimpleTFIDF:
    """
    A lightweight, pure-Python TF-IDF encoder for user interests.
    This avoids compiled sklearn/numpy dependencies, ensuring portability on Windows.
    """
    def __init__(self):
        self.vocab: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.doc_count = 0

    def fit(self, documents: List[List[str]]):
        self.doc_count = len(documents)
        if self.doc_count == 0:
            return

        # Count document frequency (DF) for each interest term
        df: Dict[str, int] = {}
        for doc in documents:
            unique_terms = set(doc)
            for term in unique_terms:
                df[term] = df.get(term, 0) + 1

        # Build vocabulary indices and compute IDF
        self.vocab = {term: idx for idx, term in enumerate(df.keys())}
        for term, count in df.items():
            # Standard smooth IDF formula
            self.idf[term] = math.log((1 + self.doc_count) / (1 + count)) + 1.0

    def transform(self, doc: List[str]) -> List[float]:
        vector = [0.0] * len(self.vocab)
        if not doc or not self.vocab:
            return vector

        # Term frequency (TF) count
        tf: Dict[str, int] = {}
        for term in doc:
            if term in self.vocab:
                tf[term] = tf.get(term, 0) + 1

        # Apply TF-IDF
        for term, count in tf.items():
            idx = self.vocab[term]
            vector[idx] = count * self.idf[term]

        return vector

embedding_service = SimpleTFIDF()
