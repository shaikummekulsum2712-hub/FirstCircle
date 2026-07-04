# Join Drop + Vibe Voting API Testing

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

### Step 1: Create Test Data

#### Create 2 Users
**POST /api/users/**

Request 1:
```json
{
  "name": "Alice",
  "email": "alice@nitk.ac.in",
  "roll_number": "CS001"
}
```

Response:
```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@nitk.ac.in",
  "roll_number": "CS001",
  "college_domain": "nitk.ac.in",
  "email_verified": false,
  "verification_status": "pending",
  "created_at": "2026-06-22T10:30:00"
}
```

Request 2:
```json
{
  "name": "Bob",
  "email": "bob@nitk.ac.in",
  "roll_number": "CS002"
}
```

Response: (Similar, with id=2)

#### Create 1 Safe Location
**POST /api/locations/**

Request:
```json
{
  "name": "Campus Café",
  "location_type": "café",
  "is_safe": true,
  "allowed_circle_types": "friend,study,build,random"
}
```

Response:
```json
{
  "id": 1,
  "name": "Campus Café",
  "location_type": "café",
  "is_safe": true,
  "allowed_circle_types": "friend,study,build,random"
}
```

#### Create 1 Drop (by User 1 - Alice)
**POST /api/drops/**

Request:
```json
{
  "creator_user_id": 1,
  "title": "Study Group Session",
  "description": "Let's study together",
  "circle_type": "study",
  "location_id": 1,
  "scheduled_date": "2026-06-25",
  "start_time": "14:00",
  "end_time": "16:00",
  "max_members": 4,
  "urgency_level": "medium",
  "vibe_tags": ["focused", "productive", "friendly"],
  "expires_at": "2026-06-24T20:00:00"
}
```

Response:
```json
{
  "id": 1,
  "creator_user_id": 1,
  "title": "Study Group Session",
  "description": "Let's study together",
  "circle_type": "study",
  "location_id": 1,
  "scheduled_date": "2026-06-25",
  "start_time": "14:00",
  "end_time": "16:00",
  "max_members": 4,
  "current_members": 1,
  "status": "open",
  "urgency_level": "medium",
  "vibe_tags": ["focused", "productive", "friendly"],
  "created_at": "2026-06-22T10:35:00",
  "expires_at": "2026-06-24T20:00:00"
}
```

---

### Step 2: Join Drop (Drop Member API)

#### Join Drop - Success Case
**POST /api/drop-members/join**

Request:
```json
{
  "drop_id": 1,
  "user_id": 2
}
```

Response:
```json
{
  "id": 1,
  "drop_id": 1,
  "user_id": 2,
  "role": "member",
  "join_status": "joined",
  "joined_at": "2026-06-22T10:40:00"
}
```

✅ **Drop is now:** GET /api/drops/1
```json
{
  "current_members": 2,
  "status": "open",
  ...
}
```

---

#### Join Drop - Error: Already Joined
**POST /api/drop-members/join**

Request (same user again):
```json
{
  "drop_id": 1,
  "user_id": 2
}
```

Response (400):
```json
{
  "detail": "User already joined this drop"
}
```

---

#### Join Drop - Error: Creator Cannot Join Again
**POST /api/drop-members/join**

Request:
```json
{
  "drop_id": 1,
  "user_id": 1
}
```

Response (400):
```json
{
  "detail": "Creator is already member of their drop"
}
```

---

#### Join Drop - Error: User Not Found
**POST /api/drop-members/join**

Request:
```json
{
  "drop_id": 1,
  "user_id": 999
}
```

Response (404):
```json
{
  "detail": "User not found"
}
```

---

#### Join Drop - Error: Drop Not Found
**POST /api/drop-members/join**

Request:
```json
{
  "drop_id": 999,
  "user_id": 2
}
```

Response (404):
```json
{
  "detail": "Drop not found"
}
```

---

### Step 3: Get Drop Members

#### Get All Members of a Drop
**GET /api/drop-members/drop/1**

Response:
```json
[
  {
    "id": 1,
    "drop_id": 1,
    "user_id": 2,
    "role": "member",
    "join_status": "joined",
    "joined_at": "2026-06-22T10:40:00"
  }
]
```

---

#### Get All Drops Joined by a User
**GET /api/drop-members/user/2**

Response:
```json
[
  {
    "id": 1,
    "drop_id": 1,
    "user_id": 2,
    "role": "member",
    "join_status": "joined",
    "joined_at": "2026-06-22T10:40:00"
  }
]
```

---

### Step 4: Leave Drop

#### Leave Drop - Success
**PATCH /api/drop-members/leave**

Request:
```json
{
  "drop_id": 1,
  "user_id": 2
}
```

Response:
```json
{
  "message": "Successfully left drop"
}
```

✅ **Drop is now:** GET /api/drops/1
```json
{
  "current_members": 1,
  "status": "open",
  ...
}
```

---

#### Leave Drop - Error: Creator Cannot Leave
**PATCH /api/drop-members/leave**

Request:
```json
{
  "drop_id": 1,
  "user_id": 1
}
```

Response (400):
```json
{
  "detail": "Creator cannot leave their drop"
}
```

---

#### Leave Drop - Error: Not Joined
**PATCH /api/drop-members/leave**

Request (user already left):
```json
{
  "drop_id": 1,
  "user_id": 2
}
```

Response (400):
```json
{
  "detail": "User is not joined to this drop"
}
```

---

### Step 5: Full Drop Status

#### Create a smaller drop to test "full" status
**POST /api/drops/**

Request:
```json
{
  "creator_user_id": 1,
  "title": "Small Group",
  "description": "Small study group",
  "circle_type": "study",
  "location_id": 1,
  "scheduled_date": "2026-06-26",
  "start_time": "15:00",
  "end_time": "16:00",
  "max_members": 2,
  "urgency_level": "low",
  "vibe_tags": ["casual"],
  "expires_at": "2026-06-25T20:00:00"
}
```

Response: (drop id=2, current_members=1, status="open")

#### Join the small drop
**POST /api/drop-members/join**

Request:
```json
{
  "drop_id": 2,
  "user_id": 2
}
```

Response: (id=2, success)

✅ **Check drop status:** GET /api/drops/2
```json
{
  "id": 2,
  "current_members": 2,
  "status": "full",
  ...
}
```

---

#### Try to join full drop
**POST /api/drop-members/join**

Create another user first (User 3):
```json
{
  "name": "Charlie",
  "email": "charlie@nitk.ac.in",
  "roll_number": "CS003"
}
```

Then try to join:
**POST /api/drop-members/join**

Request:
```json
{
  "drop_id": 2,
  "user_id": 3
}
```

Response (400):
```json
{
  "detail": "Drop is full"
}
```

---

### Step 6: Vibe Voting

#### Vote Up on a Vibe Tag
**POST /api/vibe-votes/**

Request:
```json
{
  "drop_id": 1,
  "user_id": 2,
  "vibe_tag": "focused",
  "vote_type": "up"
}
```

Response:
```json
{
  "id": 1,
  "drop_id": 1,
  "user_id": 2,
  "vibe_tag": "focused",
  "vote_type": "up",
  "created_at": "2026-06-22T10:50:00"
}
```

---

#### Vote Down on a Different Tag
**POST /api/vibe-votes/**

Request:
```json
{
  "drop_id": 1,
  "user_id": 2,
  "vibe_tag": "productive",
  "vote_type": "down"
}
```

Response:
```json
{
  "id": 2,
  "drop_id": 1,
  "user_id": 2,
  "vibe_tag": "productive",
  "vote_type": "down",
  "created_at": "2026-06-22T10:51:00"
}
```

---

#### Update Existing Vote
**POST /api/vibe-votes/**

Request (same user, same tag, different vote):
```json
{
  "drop_id": 1,
  "user_id": 2,
  "vibe_tag": "focused",
  "vote_type": "down"
}
```

Response (id=1, but vote_type changed to "down"):
```json
{
  "id": 1,
  "drop_id": 1,
  "user_id": 2,
  "vibe_tag": "focused",
  "vote_type": "down",
  "created_at": "2026-06-22T10:50:00"
}
```

---

#### Vote with Invalid Vote Type
**POST /api/vibe-votes/**

Request:
```json
{
  "drop_id": 1,
  "user_id": 2,
  "vibe_tag": "friendly",
  "vote_type": "invalid"
}
```

Response (422):
```json
{
  "detail": [
    {
      "loc": ["body", "vote_type"],
      "msg": "vote_type must be one of {'up', 'down'}",
      "type": "value_error"
    }
  ]
}
```

---

### Step 7: Get Vibe Votes

#### Get All Votes on a Drop
**GET /api/vibe-votes/drop/1**

Response:
```json
[
  {
    "id": 1,
    "drop_id": 1,
    "user_id": 2,
    "vibe_tag": "focused",
    "vote_type": "down",
    "created_at": "2026-06-22T10:50:00"
  },
  {
    "id": 2,
    "drop_id": 1,
    "user_id": 2,
    "vibe_tag": "productive",
    "vote_type": "down",
    "created_at": "2026-06-22T10:51:00"
  }
]
```

---

#### Get Vibe Vote Summary
**GET /api/vibe-votes/drop/1/summary**

Response:
```json
{
  "drop_id": 1,
  "summary": [
    {
      "vibe_tag": "focused",
      "upvotes": 0,
      "downvotes": 1,
      "net_votes": -1
    },
    {
      "vibe_tag": "productive",
      "upvotes": 0,
      "downvotes": 1,
      "net_votes": -1
    },
    {
      "vibe_tag": "friendly",
      "upvotes": 0,
      "downvotes": 0,
      "net_votes": 0
    }
  ]
}
```

---

#### Vote Summary with Multiple Users

Add votes from User 1 (Alice):

**POST /api/vibe-votes/**
```json
{
  "drop_id": 1,
  "user_id": 1,
  "vibe_tag": "focused",
  "vote_type": "up"
}
```

**POST /api/vibe-votes/**
```json
{
  "drop_id": 1,
  "user_id": 1,
  "vibe_tag": "friendly",
  "vote_type": "up"
}
```

Now check summary:
**GET /api/vibe-votes/drop/1/summary**

Response:
```json
{
  "drop_id": 1,
  "summary": [
    {
      "vibe_tag": "friendly",
      "upvotes": 1,
      "downvotes": 0,
      "net_votes": 1
    },
    {
      "vibe_tag": "focused",
      "upvotes": 1,
      "downvotes": 1,
      "net_votes": 0
    },
    {
      "vibe_tag": "productive",
      "upvotes": 0,
      "downvotes": 1,
      "net_votes": -1
    }
  ]
}
```

(Sorted by net_votes descending)

---

## Complete API Reference

### Drop Members Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /api/drop-members/join | Join a drop |
| PATCH | /api/drop-members/leave | Leave a drop |
| GET | /api/drop-members/drop/{drop_id} | Get members of a drop |
| GET | /api/drop-members/user/{user_id} | Get drops joined by user |

### Vibe Votes Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /api/vibe-votes/ | Vote on a vibe tag |
| GET | /api/vibe-votes/drop/{drop_id} | Get all votes on a drop |
| GET | /api/vibe-votes/drop/{drop_id}/summary | Get vote summary |

---

## Error Codes

| Code | Scenario |
|------|----------|
| 400 | User already joined / Drop full / Creator cannot leave / Invalid data |
| 404 | User not found / Drop not found |
| 422 | Validation error (e.g., invalid vote_type) |

---

## Business Rules Enforced

✅ User must exist
✅ Drop must exist and be open
✅ User cannot join twice
✅ Creator cannot join again
✅ Creator cannot leave
✅ Cannot join full drops
✅ Decrement current_members on leave
✅ Update drop status to "full" when needed
✅ One vote per user per vibe_tag per drop
✅ Update vote if voting again
✅ Summary sorted by net_votes descending
