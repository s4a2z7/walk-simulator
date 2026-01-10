-- Phoenix Pet Database Schema

-- Drop existing tables
DROP TABLE IF EXISTS allergy_check_records CASCADE;
DROP TABLE IF EXISTS user_allergies CASCADE;
DROP TABLE IF EXISTS evolution_records CASCADE;
DROP TABLE IF EXISTS feeding_records CASCADE;
DROP TABLE IF EXISTS step_records CASCADE;
DROP TABLE IF EXISTS friendships CASCADE;
DROP TABLE IF EXISTS pets CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    avatar_emoji VARCHAR(10) DEFAULT '😊',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- 2. Pets table
CREATE TABLE pets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) DEFAULT '불사조',
    current_stage INTEGER DEFAULT 1,
    stage_name VARCHAR(100) DEFAULT '신비한 알',
    stage_emoji VARCHAR(10) DEFAULT '🥚',
    total_exp INTEGER DEFAULT 0,
    current_exp INTEGER DEFAULT 0,
    exp_to_next_stage INTEGER DEFAULT 1000,
    hunger_level INTEGER DEFAULT 100 CHECK (hunger_level >= 0 AND hunger_level <= 100),
    happiness_level INTEGER DEFAULT 100 CHECK (happiness_level >= 0 AND happiness_level <= 100),
    total_steps INTEGER DEFAULT 0,
    today_steps INTEGER DEFAULT 0,
    last_fed_at TIMESTAMP,
    born_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_pets_user_id ON pets(user_id);
CREATE INDEX idx_pets_total_steps ON pets(total_steps DESC);

-- 3. Step records table
CREATE TABLE step_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    pet_id UUID NOT NULL REFERENCES pets(id) ON DELETE CASCADE,
    steps INTEGER NOT NULL CHECK (steps > 0),
    exp_gained INTEGER NOT NULL,
    recorded_at TIMESTAMP DEFAULT NOW(),
    record_date DATE DEFAULT CURRENT_DATE
);

CREATE INDEX idx_step_records_user_date ON step_records(user_id, record_date DESC);
CREATE INDEX idx_step_records_pet ON step_records(pet_id);

-- 4. Feeding records table
CREATE TABLE feeding_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    pet_id UUID NOT NULL REFERENCES pets(id) ON DELETE CASCADE,
    food_type VARCHAR(50) NOT NULL,
    hunger_restored INTEGER NOT NULL,
    happiness_gained INTEGER NOT NULL,
    fed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_feeding_records_pet ON feeding_records(pet_id);
CREATE INDEX idx_feeding_records_date ON feeding_records(fed_at DESC);

-- 5. Evolution records table
CREATE TABLE evolution_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pet_id UUID NOT NULL REFERENCES pets(id) ON DELETE CASCADE,
    from_stage INTEGER NOT NULL,
    to_stage INTEGER NOT NULL,
    from_stage_name VARCHAR(100) NOT NULL,
    to_stage_name VARCHAR(100) NOT NULL,
    total_exp_at_evolution INTEGER NOT NULL,
    evolved_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_evolution_records_pet ON evolution_records(pet_id);

-- 6. Friendships table
CREATE TABLE friendships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    friend_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'accepted',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, friend_id),
    CHECK (user_id != friend_id)
);

CREATE INDEX idx_friendships_user ON friendships(user_id, status);
CREATE INDEX idx_friendships_friend ON friendships(friend_id);

-- 7. User allergies table
CREATE TABLE user_allergies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    allergy_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, allergy_name)
);

CREATE INDEX idx_user_allergies_user ON user_allergies(user_id);

-- 8. Allergy check records table
CREATE TABLE allergy_check_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    image_url TEXT,
    ocr_text TEXT,
    verdict VARCHAR(20) NOT NULL,
    core_message TEXT,
    detected_ingredients TEXT[],
    judgment_reason TEXT,
    checked_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_allergy_check_records_user ON allergy_check_records(user_id, checked_at DESC);
-- You can uncomment these if you want sample data

/*
-- Sample user 1
INSERT INTO users (username, email, password_hash, display_name) VALUES
('testuser1', 'test1@example.com', '$2b$10$abcdefghijklmnopqrstuv', 'Test User 1');

-- Get the user_id
DO $$
DECLARE
    v_user_id UUID;
BEGIN
    SELECT id INTO v_user_id FROM users WHERE username = 'testuser1';
    
    -- Create pet for user 1
    INSERT INTO pets (user_id, name, current_stage, total_exp, current_exp, total_steps, today_steps) VALUES
    (v_user_id, '불사조', 3, 5000, 2000, 50000, 3500);
END $$;
*/
