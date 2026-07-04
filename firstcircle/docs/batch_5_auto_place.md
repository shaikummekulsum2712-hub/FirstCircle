# Auto-place API Testing

## Endpoint

**POST /api/auto-place/suggest**

Suggests the best open drop for a user based on preferences and scoring engine.

---

## Quick Start

1. **Start backend:**
   ```powershell
   cd firstcircle/backend
   uvicorn main:app --reload
   ```

2. **Open Swagger UI:** http://localhost:8000/docs

3. **Follow test sequence below**

---

## Test Sequence

### Step 1: Setup Test Data

#### Create 3 Users
**POST /api/users/**

User 1 (Alice):
```json
{
  "name": "Alice",
  "email": "alice@nitk.ac.in",
  "roll_number": "CS001"
}
```

Response: `id: 1`

User 2 (Bob):
```json
{
  "name": "Bob",
  "email": "bob@nitk.ac.in",
  "roll_number": "CS002"
}
```

Response: `id: 2`

User 3 (Charlie):
```json
{
  "name": "Charlie",
  "email": "charlie@nitk.ac.in",
  "roll_number": "CS003"
}
```

Response: `id: 3`

---

#### Create 2 Safe Locations
**POST /api/locations/**

Location 1 (Café):
```json
{
  "name": "Campus Café",
  "location_type": "café",
  "is_safe": true,
  "allowed_circle_types": "friend,study,build,random"
}
```

Response: `id: 1`

Location 2 (Library):
```json
{
  "name": "Central Library",
  "location_type": "library",
  "is_safe": true,
  "allowed_circle_types": "friend,study,build,random"
}
```

Response: `id: 2`

---

#### Create Drops (by Bob - User 2)

**Drop 1: Study Group**

**POST /api/drops/**
```json
{
  "creator_user_id": 2,
  "title": "DBMS Study Group",
  "description": "Preparing for the database exam together",
  "circle_type": "study",
  "location_id": 1,
  "scheduled_date": "2026-06-25",
  "start_time": "14:00",
  "end_time": "16:00",
  "max_members": 4,
  "urgency_level": "high",
  "vibe_tags": ["focused", "productive", "academic"],
  "expires_at": "2026-06-24T20:00:00"
}
```

Response: `id: 1, current_members: 1, status: "open"`

---

**Drop 2: Friend Hangout**

**POST /api/drops/**
```json
{
  "creator_user_id": 2,
  "title": "Casual Coffee Hangout",
  "description": "Just hang out and chill with friends",
  "circle_type": "friend",
  "location_id": 2,
  "scheduled_date": "2026-06-25",
  "start_time": "18:00",
  "end_time": "19:30",
  "max_members": 5,
  "urgency_level": "low",
  "vibe_tags": ["chill", "friendly", "casual"],
  "expires_at": "2026-06-24T20:00:00"
}
```

Response: `id: 2, current_members: 1, status: "open"`

---

#### Join Bob's Drops with Charlie (User 3)

**POST /api/drop-members/join**
```json
{
  "drop_id": 1,
  "user_id": 3
}
```

Response: success (Charlie now in drop 1)

**GET /api/drops/1** → current_members: 2

---

### Step 2: Auto-place Suggestion

#### Test Case 1: Perfect Match (Circle Type + Time + Vibes)

**Request:** Alice wants a study drop on same day/time with focus vibes

**POST /api/auto-place/suggest**

```json
{
  "user_id": 1,
  "preferred_circle_type": "study",
  "preferred_day": "2026-06-25",
  "preferred_start_time": "14:00",
  "preferred_end_time": "16:00",
  "preferred_vibes": ["focused", "academic"]
}
```

**Expected Response:**

```json
{
  "recommended_drop": {
    "drop_id": 1,
    "title": "DBMS Study Group",
    "description": "Preparing for the database exam together",
    "circle_type": "study",
    "scheduled_date": "2026-06-25",
    "start_time": "14:00",
    "end_time": "16:00",
    "location_id": 1,
    "current_members": 2,
    "max_members": 4,
    "creator_user_id": 2,
    "vibe_tags": ["focused", "productive", "academic"]
  },
  "score": 90.0,
  "score_breakdown": {
    "circle_type_fit": 25.0,
    "time_fit": 25.0,
    "profile_fit": 10.0,
    "vibe_fit": 15.0,
    "urgency_boost": 5.0,
    "fairness_boost": 5.0,
    "total": 85.0
  },
  "reason": "This drop is a great match! 2/4 spots filled. Circle type: study, Time: 14:00-16:00"
}
```

✅ **Explanation:**
- Circle type match: 25 (study = study)
- Time fit: 25 (same day, same time)
- Vibe fit: 15 (2 matches: focused, academic)
- Urgency: 5 (2/4 = 50% full)
- Fairness: 5 (user has 0 joined drops)
- Total: 85

---

#### Test Case 2: Partial Match (Wrong Time)

**Request:** Alice wants same circle type but different time

**POST /api/auto-place/suggest**

```json
{
  "user_id": 1,
  "preferred_circle_type": "study",
  "preferred_day": "2026-06-25",
  "preferred_start_time": "10:00",
  "preferred_end_time": "12:00",
  "preferred_vibes": ["focused"]
}
```

**Expected Response:**

```json
{
  "recommended_drop": {
    "drop_id": 1,
    "title": "DBMS Study Group",
    ...
  },
  "score": 62.0,
  "score_breakdown": {
    "circle_type_fit": 25.0,
    "time_fit": 0.0,
    "profile_fit": 10.0,
    "vibe_fit": 12.0,
    "urgency_boost": 5.0,
    "fairness_boost": 5.0,
    "total": 57.0
  },
  "reason": "This drop is a great match! 2/4 spots filled. Circle type: study, Time: 14:00-16:00"
}
```

✅ **Explanation:**
- Circle type: 25 (exact match)
- Time: 0 (no overlap - 10-12 vs 14-16)
- Still recommended because it's the best available
- Lower score (57) due to time mismatch

---

#### Test Case 3: Circle Type "Any" Preference

**Request:** Alice accepts any circle type

**POST /api/auto-place/suggest**

```json
{
  "user_id": 1,
  "preferred_circle_type": "any",
  "preferred_day": "2026-06-25",
  "preferred_start_time": "18:00",
  "preferred_end_time": "19:30",
  "preferred_vibes": ["casual"]
}
```

**Expected Response:**

```json
{
  "recommended_drop": {
    "drop_id": 2,
    "title": "Casual Coffee Hangout",
    "circle_type": "friend",
    ...
  },
  "score": 70.0,
  "score_breakdown": {
    "circle_type_fit": 15.0,
    "time_fit": 25.0,
    "profile_fit": 10.0,
    "vibe_fit": 15.0,
    "urgency_boost": 2.0,
    "fairness_boost": 5.0,
    "total": 72.0
  },
  "reason": "This drop is a great match! 1/5 spots filled. Circle type: friend, Time: 18:00-19:30"
}
```

✅ **Explanation:**
- Circle type: 15 (not exact match, but preferred is "any")
- Time: 25 (perfect match)
- Vibe: 15 (casual matches)
- Urgency: 2 (1/5 = 20% full, low fill so low boost)

---

#### Test Case 4: No Preferred Vibes

**Request:** Alice has no vibe preferences

**POST /api/auto-place/suggest**

```json
{
  "user_id": 1,
  "preferred_circle_type": "study",
  "preferred_day": "2026-06-25",
  "preferred_start_time": "14:00",
  "preferred_end_time": "16:00",
  "preferred_vibes": []
}
```

**Expected Response:**

Score breakdown shows vibe_fit: 7.5 (neutral when no preference)

---

#### Test Case 5: User Already Joined Drop (Exclusion)

**Step 1:** Alice joins drop 1

**POST /api/drop-members/join**
```json
{
  "drop_id": 1,
  "user_id": 1
}
```

**Step 2:** Try to get auto-place suggestion

**POST /api/auto-place/suggest**

```json
{
  "user_id": 1,
  "preferred_circle_type": "study",
  "preferred_day": "2026-06-25",
  "preferred_start_time": "14:00",
  "preferred_end_time": "16:00",
  "preferred_vibes": ["focused"]
}
```

**Expected Response:**

Should return drop 2 (friend drop) or no match, since drop 1 is excluded

```json
{
  "recommended_drop": {
    "drop_id": 2,
    "title": "Casual Coffee Hangout",
    ...
  },
  "score": 55.0,
  "score_breakdown": {
    "circle_type_fit": 0.0,
    "time_fit": 12.0,
    "profile_fit": 10.0,
    "vibe_fit": 0.0,
    "urgency_boost": 2.0,
    "fairness_boost": 3.0,
    "reason": "..."
  }
}
```

---

#### Test Case 6: Full Drop (Exclusion)

**Step 1:** Create a small drop (max_members=2)

**POST /api/drops/**
```json
{
  "creator_user_id": 2,
  "title": "Tiny Study Session",
  "description": "Just two people",
  "circle_type": "study",
  "location_id": 1,
  "scheduled_date": "2026-06-25",
  "start_time": "14:00",
  "end_time": "16:00",
  "max_members": 2,
  "urgency_level": "low",
  "vibe_tags": ["focused"],
  "expires_at": "2026-06-24T20:00:00"
}
```

Response: `id: 3, current_members: 1`

**Step 2:** Alice joins it

**POST /api/drop-members/join**
```json
{
  "drop_id": 3,
  "user_id": 1
}
```

Now drop 3 is full (2/2), status = "full"

**Step 3:** Try auto-place for another user

**POST /api/auto-place/suggest**

```json
{
  "user_id": 3,
  "preferred_circle_type": "study",
  "preferred_day": "2026-06-25",
  "preferred_start_time": "14:00",
  "preferred_end_time": "16:00",
  "preferred_vibes": []
}
```

Should return drop 1, NOT drop 3 (excluded because full)

---

#### Test Case 7: Unsafe Location (Exclusion)

**Step 1:** Create unsafe location

**POST /api/locations/**
```json
{
  "name": "Unsafe Location",
  "location_type": "unknown",
  "is_safe": false,
  "allowed_circle_types": "friend,study,build,random"
}
```

Response: `id: 3, is_safe: false`

**Step 2:** Create drop at unsafe location

**POST /api/drops/**
```json
{
  "creator_user_id": 2,
  "title": "Study at Unsafe Place",
  "description": "Bad location",
  "circle_type": "study",
  "location_id": 3,
  "scheduled_date": "2026-06-25",
  "start_time": "14:00",
  "end_time": "16:00",
  "max_members": 4,
  "urgency_level": "low",
  "vibe_tags": ["focused"],
  "expires_at": "2026-06-24T20:00:00"
}
```

**Step 3:** Try auto-place

**POST /api/auto-place/suggest**

Should NOT recommend this drop (excluded due to unsafe location)

---

#### Test Case 8: User's Own Drop (Exclusion)

**POST /api/auto-place/suggest**

```json
{
  "user_id": 2,
  "preferred_circle_type": "study",
  "preferred_day": "2026-06-25",
  "preferred_start_time": "14:00",
  "preferred_end_time": "16:00",
  "preferred_vibes": []
}
```

Should NOT recommend drop 1 (Bob created it) or drop 2 (Bob created it)

Response: No match found

```json
{
  "recommended_drop": null,
  "score": null,
  "score_breakdown": null,
  "reason": "No suitable drops found after filtering"
}
```

---

#### Test Case 9: Fairness Boost

**Scenario:** User with 0 drops joined gets higher fairness score

Compare auto-place scores for:
- Alice (0 drops joined): fairness_boost = 5.0
- Bob (already created/joined drops): fairness_boost = 1.0

Same drop recommendation but different fairness boost.

---

#### Test Case 10: Non-existent User

**POST /api/auto-place/suggest**

```json
{
  "user_id": 999,
  "preferred_circle_type": "study",
  "preferred_day": "2026-06-25",
  "preferred_start_time": "14:00",
  "preferred_end_time": "16:00",
  "preferred_vibes": []
}
```

Response: 

```json
{
  "recommended_drop": null,
  "score": null,
  "score_breakdown": null,
  "reason": "User not found"
}
```

---

## Scoring Rules Reference

| Component | Max Points | Calculation |
|-----------|-----------|-------------|
| Circle Type Fit | 25 | exact=25, any=15, mismatch=0 |
| Time Fit | 25 | overlap=25, same_day=12, none=0 |
| Profile Fit | 20 | keyword matching (0-20) |
| Vibe Fit | 15 | overlap ratio × 15 |
| Urgency Boost | 10 | based on fill %: 1-10 |
| Fairness Boost | 5 | users with fewer drops: 1-5 |
| **Total** | **100** | Sum of all |

---

## Exclusions Applied

- ❌ Drops created by same user
- ❌ Drops already joined by user
- ❌ Full drops (status = "full")
- ❌ Expired drops (status = "expired")
- ❌ Cancelled drops (status = "cancelled")
- ❌ Drops at unsafe locations

---

## Example JSON Request/Response

### Request
```json
{
  "user_id": 1,
  "preferred_circle_type": "study",
  "preferred_day": "2026-06-25",
  "preferred_start_time": "14:00",
  "preferred_end_time": "16:00",
  "preferred_vibes": ["focused", "productive"]
}
```

### Response (Success)
```json
{
  "recommended_drop": {
    "drop_id": 1,
    "title": "DBMS Study Group",
    "description": "Preparing for database exam",
    "circle_type": "study",
    "scheduled_date": "2026-06-25",
    "start_time": "14:00",
    "end_time": "16:00",
    "location_id": 1,
    "current_members": 2,
    "max_members": 4,
    "creator_user_id": 2,
    "vibe_tags": ["focused", "productive", "academic"]
  },
  "score": 85.0,
  "score_breakdown": {
    "circle_type_fit": 25.0,
    "time_fit": 25.0,
    "profile_fit": 10.0,
    "vibe_fit": 15.0,
    "urgency_boost": 5.0,
    "fairness_boost": 5.0,
    "total": 85.0
  },
  "reason": "This drop is a great match! 2/4 spots filled. Circle type: study, Time: 14:00-16:00"
}
```

### Response (No Match)
```json
{
  "recommended_drop": null,
  "score": null,
  "score_breakdown": null,
  "reason": "No suitable drops found after filtering"
}
```

---

## Testing Tips

1. **Test scores:** Create multiple drops with different circle types and times
2. **Test exclusions:** Verify all exclusion rules work
3. **Test rankings:** Multiple eligible drops should rank by score
4. **Test fairness:** Users with fewer drops should see fairness boost
5. **Test no matches:** Verify graceful handling when no drops match
