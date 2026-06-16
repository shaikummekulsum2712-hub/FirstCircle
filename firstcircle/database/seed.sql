-- FirstCircle Static Database Seeds
-- (Currently the core structure relies on dynamic tables, but we initialize system tracking parameters here)

-- Optional: System User seed
INSERT INTO users (id, email, hashed_password) VALUES (999, 'system@firstcircle.com', '$2b$12$dE7.d9K5D6s2Q/a1U0T2eeCq/Vd5D3E/sO3UqZ7.h4eN.c2P1F5L2') ON CONFLICT DO NOTHING;
INSERT INTO profiles (id, user_id, display_name, bio, age, gender, reliability_score, interests, comforts) VALUES (999, 999, 'System Bot', 'Automated matching engine representative.', 99, 'Other', 100.0, 'matching,ai,community', '{}') ON CONFLICT DO NOTHING;
