# FirstCircle API Contract

This contract defines the JSON REST interfaces between the React frontend and FastAPI backend.

---

## 1. Authentication
*   `POST /api/auth/register`: Create a new user.
    *   *Request*: `{"email": "...", "password": "..."}`
    *   *Response*: `{"token": "...", "user": {"id": 1, "email": "..."}}`
*   `POST /api/auth/login`: Login existing user.
    *   *Request*: `{"email": "...", "password": "..."}`
    *   *Response*: `{"token": "...", "user": {"id": 1, "email": "..."}}`

---

## 2. Profile Setup & Availability
*   `GET /api/profile/me`: Retrieve self profile.
    *   *Response*: `{"id": 1, "display_name": "...", "bio": "...", "interests": ["#tech"], "comforts": {}, "reliability_score": 100}`
*   `PUT /api/profile/me`: Update profile details.
*   `GET /api/profile/slots`: Fetch free slots list.
    *   *Response*: `[{"day_of_week": 5, "start_time": "18:00", "end_time": "22:00"}]`
*   `POST /api/profile/slots`: Save / replace free slots.

---

## 3. Drops (Activity Proposals)
*   `GET /api/drops`: Browse active drops, optionally filtered.
    *   *Params*: `?category=food&query=dinner`
*   `POST /api/drops`: Create a new Drop.
    *   *Request*: `{"title": "...", "description": "...", "category": "...", "event_time": "2026-06-20T19:00:00Z", "location_name": "...", "max_members": 5}`
*   `POST /api/drops/{id}/join`: Join a drop.
*   `POST /api/drops/{id}/vibe-vote`: Vote on drop vibes.
    *   *Request*: `{"vibe": "chill"}`

---

## 4. Proposals (Blind Matching Groups)
*   `GET /api/proposals/active`: Get active proposal.
    *   *Response*: `{"id": 10, "drop_title": "...", "members_summary": [{"age": 25, "gender": "F", "shared_interests": ["#boardgames"]}], "expires_at": "...", "time_left_seconds": 3600}`
*   `POST /api/proposals/{id}/accept`: Vote to accept the group match.
*   `POST /api/proposals/{id}/skip`: Vote to skip/reject group.

---

## 5. Circles (Confirmed Events & Chat)
*   `GET /api/circles/active`: List currently active confirmed circles.
*   `GET /api/circles/{id}`: Detailed circle page including member full reveal and group chat logs.
*   `POST /api/circles/{id}/reschedule`: Request reschedule.
    *   *Request*: `{"proposed_time": "2026-06-21T18:00:00Z"}`

---

## 6. Feedback & Safety Reports
*   `POST /api/feedback`: Post ratings and confirm attendance.
    *   *Request*: `{"circle_id": 1, "attendance": [{"profile_id": 2, "status": "on-time"}], "ratings": [{"profile_id": 2, "rating": 5}]}`
*   `POST /api/report`: Flag safety incidents.
