-- FirstCircle Rich Sample Data
-- Note: The bcrypt hash below is for 'password123'

-- Insert Sample Users
INSERT INTO users (id, email, hashed_password, created_at) VALUES 
(1, 'alice@example.com', '$2b$12$EryG3.E8OQW7M1GzPjHqLe3cK1Rj9E21/Tj/Z51H7.8W91c9Yy25S', '2026-06-15 10:00:00'),
(2, 'bob@example.com', '$2b$12$EryG3.E8OQW7M1GzPjHqLe3cK1Rj9E21/Tj/Z51H7.8W91c9Yy25S', '2026-06-15 10:05:00'),
(3, 'charlie@example.com', '$2b$12$EryG3.E8OQW7M1GzPjHqLe3cK1Rj9E21/Tj/Z51H7.8W91c9Yy25S', '2026-06-15 10:10:00'),
(4, 'diana@example.com', '$2b$12$EryG3.E8OQW7M1GzPjHqLe3cK1Rj9E21/Tj/Z51H7.8W91c9Yy25S', '2026-06-15 10:15:00'),
(5, 'ethan@example.com', '$2b$12$EryG3.E8OQW7M1GzPjHqLe3cK1Rj9E21/Tj/Z51H7.8W91c9Yy25S', '2026-06-15 10:20:00');

-- Insert Sample Profiles
INSERT INTO profiles (id, user_id, display_name, bio, age, gender, reliability_score, interests, comforts) VALUES
(1, 1, 'Alice Smith', 'Love indie rock, craft coffee, and strategy board games. Software engineer by day.', 26, 'Female', 98.0, 'boardgames,tech,indierock,coffee', '{"group_size_pref": 4, "vibe_pref": "chill"}'),
(2, 2, 'Bob Jones', 'Avid hiker and coffee lover. Always looking for new trails and board game groups.', 28, 'Male', 95.0, 'boardgames,coffee,hiking,movies', '{"group_size_pref": 4, "vibe_pref": "active"}'),
(3, 3, 'Charlie Brown', 'Tech nerd who loves gaming, anime, and local indie music gigs. Friendly introvert!', 24, 'Male', 100.0, 'tech,indierock,gaming,anime', '{"group_size_pref": 4, "vibe_pref": "chill"}'),
(4, 4, 'Diana Prince', 'Outdoor photography enthusiast. Let''s explore parks and take awesome sunset shots.', 29, 'Female', 92.0, 'hiking,coffee,photography,travel', '{"group_size_pref": 4, "vibe_pref": "active"}'),
(5, 5, 'Ethan Hunt', 'Board games night organizer. Huge foodie who loves trying out street food markets.', 27, 'Male', 100.0, 'boardgames,gaming,coffee,foodie', '{"group_size_pref": 4, "vibe_pref": "chill"}');

-- Insert Free Slots (0 = Mon, 4 = Fri, 5 = Sat, 6 = Sun)
INSERT INTO free_slots (profile_id, day_of_week, start_time, end_time) VALUES
(1, 4, '18:00', '22:00'), (1, 5, '12:00', '16:00'),
(2, 4, '18:00', '22:00'), (2, 5, '12:00', '16:00'), (2, 6, '14:00', '18:00'),
(3, 4, '18:00', '22:00'), (3, 5, '12:00', '16:00'),
(4, 5, '12:00', '16:00'), (4, 6, '14:00', '18:00'),
(5, 4, '18:00', '22:00'), (5, 5, '12:00', '16:00');

-- Insert Drops
INSERT INTO drops (id, host_id, title, description, category, event_time, location_name, max_members, status) VALUES
(1, 1, 'Board Games & Coffee at Geek Haven', 'Let''s meet at Geek Haven to play Settlers of Catan and drink cold brew!', 'Board Games', '2026-06-20 18:30:00', 'Geek Haven Cafe, Downtown', 5, 'open'),
(2, 2, 'Echo Canyon Scenic Trail Hike', 'Morning loop hike around Echo Canyon. Intermediate difficulty, 3 hours total.', 'Hiking', '2026-06-14 09:00:00', 'Echo Canyon Trailhead Parking', 4, 'completed'),
(3, 4, 'Coffee & Street Photography Walk', 'Exploring local alleys and capturing street vibes. Bring your camera or phone!', 'Photography', '2026-06-21 14:00:00', 'Central Market Clocktower', 6, 'open');

-- Insert Drop Members (For active/completed drops)
INSERT INTO drop_members (drop_id, profile_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 5), -- Alice, Bob, Charlie, Ethan joined Board Games
(2, 2), (2, 4), (2, 5),          -- Bob, Diana, Ethan joined Hike
(3, 4), (3, 1);                  -- Diana, Alice joined Photography

-- Insert Vibe Votes
INSERT INTO vibe_votes (drop_id, profile_id, vibe_value) VALUES
(1, 1, 'chill'), (1, 2, 'intellectual'), (1, 3, 'chill'), (1, 5, 'chill'),
(2, 2, 'active'), (2, 4, 'active'), (2, 5, 'active');

-- Insert Proposals
-- Proposal for Drop 1: Pending matching decision
INSERT INTO proposals (id, drop_id, members_json, votes_json, status, expires_at) VALUES
(1, 1, '[1,2,3,5]', '{"1":"accept","2":"pending","3":"accept","5":"pending"}', 'pending', '2026-06-22 22:00:00');

-- Insert Circles
-- Circle for Drop 2: Confirmed and completed
INSERT INTO circles (id, drop_id, title, event_time, location_name, status) VALUES
(1, 2, 'Echo Canyon Scenic Trail Hike Circle', '2026-06-14 09:00:00', 'Echo Canyon Trailhead Parking', 'completed');

-- Insert Feedbacks for Circle 1
INSERT INTO feedbacks (circle_id, reviewer_id, reviewee_id, rating, tags) VALUES
(1, 2, 4, 5, 'friendly,energetic'),
(1, 2, 5, 5, 'helpful,punctual'),
(1, 4, 2, 5, 'friendly,active'),
(1, 4, 5, 4, 'quiet,polite'),
(1, 5, 2, 4, 'friendly'),
(1, 5, 4, 5, 'organized,enthusiastic');
