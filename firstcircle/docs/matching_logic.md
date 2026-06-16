# FirstCircle Matching Logic Specifications

The matching engine matches users into groups of 3-6 (default 4) for a given Drop activity or creates new groups via Auto-Place.

---

## 1. Score Calculation Formula

The aggregate matching score $S(G)$ for a candidate group $G = \{u_1, u_2, ..., u_n\}$ is defined as:

$$S(G) = w_i \cdot S_{interest}(G) + w_t \cdot S_{time}(G) - w_d \cdot P_{distance}(G) + w_r \cdot S_{reliability}(G)$$

Where:
*   $w_i, w_t, w_d, w_r$ are weighting coefficients.

### Interest Similarity Score $S_{interest}(G)$
Calculated by computing the pairwise cosine similarity of the TF-IDF representation of user interest chips:

$$S_{interest}(G) = \frac{2}{n(n-1)} \sum_{j < k} \text{CosineSimilarity}(v_{u_j}, v_{u_k})$$

### Time Slot Overlap Score $S_{time}(G)$
Checks the total number of hours of overlapping free slots across all members in the group:

$$S_{time}(G) = \text{OverlapHours}(\bigcap_{u \in G} \text{FreeSlots}(u))$$

If there is no overlapping slot of at least 2 hours, the group score is set to $-\infty$ (hard filter).

### Distance Penalty $P_{distance}(G)$
Calculated as the average physical distance (in kilometers) between members' default/current locations:

$$P_{distance}(G) = \frac{2}{n(n-1)} \sum_{j < k} \text{Distance}(L_{u_j}, L_{u_k})$$

### Reliability Score $S_{reliability}(G)$
Ensures high-reliability users are matched together, while flakers are grouped or quarantined:

$$S_{reliability}(G) = 1.0 - \text{StandardDeviation}(\{\text{Reliability}(u) \mid u \in G\})$$

---

## 2. Hard Exclusion Constraints

The following rules will filter out group candidates before scoring:
1.  **Soft Blacklist**: If user $A$ has user $B$ on their blacklist (or vice versa), the group is invalid.
2.  **Age Gaps**: If the maximum age minus the minimum age in the group exceeds 12 years (unless a "cross-generation" flag is checked).
3.  **Gender Configurations**: Matches gender preferences if a user has selected "Same Gender Only".
4.  **Reliability Quarantine**: Any user with a reliability score under 70 is blocked from standard matching and matched only in secondary pools.
