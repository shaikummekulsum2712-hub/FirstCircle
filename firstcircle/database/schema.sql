-- FirstCircle Database Schema (SQLite compatible)

-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Profiles Table
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    bio TEXT,
    age INTEGER,
    gender TEXT,
    reliability_score REAL DEFAULT 100.0,
    interests TEXT, -- Comma-separated tags (e.g. "tech,boardgames,coffee")
    comforts TEXT,   -- JSON string representing vibe/expense choices
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Free Slots Table
CREATE TABLE IF NOT EXISTS free_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL, -- 0 = Monday, 6 = Sunday
    start_time TEXT NOT NULL,      -- "HH:MM" format
    end_time TEXT NOT NULL,        -- "HH:MM" format
    FOREIGN KEY(profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- Drops Table
CREATE TABLE IF NOT EXISTS drops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL,
    event_time TIMESTAMP NOT NULL,
    location_name TEXT NOT NULL,
    max_members INTEGER DEFAULT 5,
    status TEXT DEFAULT 'open', -- 'open', 'matching', 'completed', 'cancelled'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(host_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- Drop Members Table
CREATE TABLE IF NOT EXISTS drop_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drop_id INTEGER NOT NULL,
    profile_id INTEGER NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(drop_id) REFERENCES drops(id) ON DELETE CASCADE,
    FOREIGN KEY(profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
    UNIQUE(drop_id, profile_id)
);

-- Vibe Votes Table
CREATE TABLE IF NOT EXISTS vibe_votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drop_id INTEGER NOT NULL,
    profile_id INTEGER NOT NULL,
    vibe_value TEXT NOT NULL,
    FOREIGN KEY(drop_id) REFERENCES drops(id) ON DELETE CASCADE,
    FOREIGN KEY(profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
    UNIQUE(drop_id, profile_id)
);

-- Proposals Table
CREATE TABLE IF NOT EXISTS proposals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drop_id INTEGER NOT NULL,
    members_json TEXT NOT NULL, -- JSON array of profile IDs, e.g. [1, 2, 3, 4]
    votes_json TEXT NOT NULL,   -- JSON object, e.g. {"1": "pending", "2": "accept"}
    status TEXT DEFAULT 'pending', -- 'pending', 'accepted', 'expired', 'skipped'
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(drop_id) REFERENCES drops(id) ON DELETE CASCADE
);

-- Circles Table
CREATE TABLE IF NOT EXISTS circles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drop_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    event_time TIMESTAMP NOT NULL,
    location_name TEXT NOT NULL,
    status TEXT DEFAULT 'scheduled', -- 'scheduled', 'completed', 'rescheduled'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(drop_id) REFERENCES drops(id) ON DELETE CASCADE
);

-- Soft Blacklist Table
CREATE TABLE IF NOT EXISTS soft_blacklists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    blacklisted_user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES profiles(id) ON DELETE CASCADE,
    FOREIGN KEY(blacklisted_user_id) REFERENCES profiles(id) ON DELETE CASCADE,
    UNIQUE(user_id, blacklisted_user_id)
);

-- Reliability History Table
CREATE TABLE IF NOT EXISTS reliability_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    event_type TEXT NOT NULL, -- 'on-time', 'late', 'no-show'
    delta REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- Feedbacks Table
CREATE TABLE IF NOT EXISTS feedbacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    circle_id INTEGER NOT NULL,
    reviewer_id INTEGER NOT NULL,
    reviewee_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    tags TEXT, -- Comma-separated descriptors
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(circle_id) REFERENCES circles(id) ON DELETE CASCADE,
    FOREIGN KEY(reviewer_id) REFERENCES profiles(id) ON DELETE CASCADE,
    FOREIGN KEY(reviewee_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- Reports Table
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    circle_id INTEGER NOT NULL,
    reporter_id INTEGER NOT NULL,
    reportee_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    status TEXT DEFAULT 'pending', -- 'pending', 'resolved', 'dismissed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(circle_id) REFERENCES circles(id) ON DELETE CASCADE,
    FOREIGN KEY(reporter_id) REFERENCES profiles(id) ON DELETE CASCADE,
    FOREIGN KEY(reportee_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_profiles_user ON profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_slots_profile ON free_slots(profile_id);
CREATE INDEX IF NOT EXISTS idx_drops_status ON drops(status);
CREATE INDEX IF NOT EXISTS idx_drop_members_drop ON drop_members(drop_id);
CREATE INDEX IF NOT EXISTS idx_drop_members_profile ON drop_members(profile_id);
CREATE INDEX IF NOT EXISTS idx_proposals_status ON proposals(status);
CREATE INDEX IF NOT EXISTS idx_circles_status ON circles(status);
