# FirstCircle Database Schema

FirstCircle uses a relational database schema (SQLite for development) to capture user relationships, active drops, matchmaking phases, and reviews.

---

## 1. Table Definitions & Fields

### Users & Profiles
*   `users`: Authentication credentials.
    *   `id` (PK, Integer)
    *   `email` (VARCHAR, Unique, Indexed)
    *   `hashed_password` (VARCHAR)
    *   `created_at` (TIMESTAMP)
*   `profiles`: Social details.
    *   `id` (PK, Integer)
    *   `user_id` (FK -> users.id, Unique)
    *   `display_name` (VARCHAR)
    *   `bio` (TEXT)
    *   `age` (Integer)
    *   `gender` (VARCHAR)
    *   `reliability_score` (Float, Default 100.0)
    *   `interests` (TEXT, Comma-separated or JSON array)
    *   `comforts` (TEXT, JSON storage of preferences)
*   `free_slots`: Calendaring windows.
    *   `id` (PK, Integer)
    *   `profile_id` (FK -> profiles.id)
    *   `day_of_week` (Integer, 0 = Monday, 6 = Sunday)
    *   `start_time` (VARCHAR, e.g., "18:00")
    *   `end_time` (VARCHAR, e.g., "22:00")

### Activities & Matching
*   `drops`: Event activities.
    *   `id` (PK, Integer)
    *   `host_id` (FK -> profiles.id)
    *   `title` (VARCHAR)
    *   `description` (TEXT)
    *   `category` (VARCHAR)
    *   `event_time` (TIMESTAMP)
    *   `location_name` (VARCHAR)
    *   `max_members` (Integer)
    *   `status` (VARCHAR, e.g., `open`, `matching`, `completed`, `cancelled`)
*   `drop_members`: Many-to-Many mapping for users joined in drops.
    *   `id` (PK, Integer)
    *   `drop_id` (FK -> drops.id)
    *   `profile_id` (FK -> profiles.id)
    *   `joined_at` (TIMESTAMP)
*   `vibe_votes`: Vibe preference submissions.
    *   `id` (PK, Integer)
    *   `drop_id` (FK -> drops.id)
    *   `profile_id` (FK -> profiles.id)
    *   `vibe_value` (VARCHAR)

### Outcomes (Proposals & Circles)
*   `proposals`: Blind match offers.
    *   `id` (PK, Integer)
    *   `drop_id` (FK -> drops.id)
    *   `members_json` (TEXT, JSON array of profile IDs in the proposed match)
    *   `votes_json` (TEXT, JSON object tracking member accepts/skips, e.g., `{"2": "accept", "3": "pending"}`)
    *   `status` (VARCHAR, e.g., `pending`, `accepted`, `expired`, `skipped`)
    *   `expires_at` (TIMESTAMP)
*   `circles`: Confirmed meetup groups.
    *   `id` (PK, Integer)
    *   `drop_id` (FK -> drops.id)
    *   `title` (VARCHAR)
    *   `event_time` (TIMESTAMP)
    *   `location_name` (VARCHAR)
    *   `status` (VARCHAR, e.g., `scheduled`, `completed`, `rescheduled`)
*   `soft_blacklists`: Exclusion pairs.
    *   `id` (PK, Integer)
    *   `user_id` (FK -> profiles.id)
    *   `blacklisted_user_id` (FK -> profiles.id)
*   `reliability_history`: Ledger of attendance events.
    *   `id` (PK, Integer)
    *   `profile_id` (FK -> profiles.id)
    *   `event_type` (VARCHAR, e.g., `on-time`, `late`, `no-show`)
    *   `delta` (Float)
    *   `created_at` (TIMESTAMP)
*   `feedbacks`: Ratings.
    *   `id` (PK, Integer)
    *   `circle_id` (FK -> circles.id)
    *   `reviewer_id` (FK -> profiles.id)
    *   `reviewee_id` (FK -> profiles.id)
    *   `rating` (Integer)
    *   `tags` (TEXT)
*   `reports`: Security claims.
    *   `id` (PK, Integer)
    *   `circle_id` (FK -> circles.id)
    *   `reporter_id` (FK -> profiles.id)
    *   `reportee_id` (FK -> profiles.id)
    *   `reason` (TEXT)
    *   `status` (VARCHAR)
