# FirstCircle AI & ML Strategy Plan

This document outlines the machine learning logic, NLP vector representations, and clustering processes running locally in FirstCircle.

---

## 1. Interest Representation (NLP)
User interests are represented as a bag of cleaned token chips (e.g., `#tech`, `#indierock`, `#hiking`).
*   **Vectorization**: To keep dependencies lightweight and stable, we build a local Term Frequency-Inverse Document Frequency (TF-IDF) representation over the vocabulary of all interest chips in the system:
    
    $$v_i = \text{TF-IDF}(I_u)$$
    
*   **Similarity Computation**: The similarity between user $A$ and user $B$ is the cosine similarity of their interest vectors:
    
    $$\text{Sim}(A, B) = \frac{v_A \cdot v_B}{\|v_A\| \|v_B\|}$$

---

## 2. Collaborative Clustering Strategy
To run Auto-Place matchings, we apply a partition clustering method (K-Means/hierarchical agglomerative clustering) over profile similarity matrices:
1.  **Feature Construction**: Create feature vectors combining interests (TF-IDF dimensions), preferred event times, and location coordinates.
2.  **Distance Metric**: Compute composite distances where:
    
    $$D(A, B) = w_{interest} (1 - \text{Sim}(A, B)) + w_{time} D_{time}(A, B) + w_{loc} D_{geo}(A, B)$$
    
3.  **Clustering Step**: Place profiles in high-density clusters of 4-6 members to seed potential Drops.

---

## 3. Human-in-the-Loop Feedback Tuning
The feedback model adjusts matching weights based on outcome history:
*   **Success Loops**: Pair matches that lead to high ratings (+4 or +5) receive small positive weight boosts in similarity scoring.
*   **Failure Loops**: If a group is skipped during blind proposal, we decay the matching priority multiplier between those user combinations to prevent future overlapping suggestions.
