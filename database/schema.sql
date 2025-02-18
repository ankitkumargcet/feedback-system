-- Drop tables if they exist to avoid conflicts
DROP TABLE IF EXISTS users, questions, responses, ml_question_scores CASCADE;

-- Users Table (Anonymized & Secure)
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id TEXT UNIQUE NOT NULL,  -- Internal identifier (not exposed)
    full_name TEXT NOT NULL,
    ads_id TEXT UNIQUE NOT NULL,  -- Active Directory ID
    manager_id TEXT NOT NULL,  -- Manager’s Employee ID
    manager_name TEXT NOT NULL,
    manager_email_hash TEXT NOT NULL,  -- Hashed for anonymity
    department TEXT NOT NULL,
    band TEXT NOT NULL,  -- Employee band level
    job_title TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,  -- Indicates if user is currently active
    email_hash TEXT UNIQUE NOT NULL,  -- Hashed for anonymity
    created_at TIMESTAMP DEFAULT NOW()
);

-- Questions Table (Categorized & Adaptive)
CREATE TABLE questions (
    question_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_text TEXT NOT NULL,
    category TEXT NOT NULL,  -- Technology, Culture, Leadership, etc.
    question_type TEXT CHECK (question_type IN ('comment', 'emoji', 'radio')) NOT NULL,
    difficulty_level INT CHECK (difficulty_level BETWEEN 1 AND 5),
    last_used_at TIMESTAMP DEFAULT NULL
);

-- Responses Table (Structured for ML & Insights)
CREATE TABLE responses (
    response_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id UUID REFERENCES questions(question_id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,

    response_text TEXT,  -- For comment-based answers
    response_emoji INT CHECK (response_emoji BETWEEN 1 AND 5),  -- 1: 😠, 2: 🙁, 3: 😐, 4: 🙂, 5: 😀
    response_radio TEXT,  -- For radio button-based answers

    sentiment TEXT CHECK (sentiment IN ('Positive', 'Neutral', 'Negative')),  
    submitted_at TIMESTAMP DEFAULT NOW(),
    defer_count INT DEFAULT 0,
	skipped BOOLEAN DEFAULT FALSE;
);

ALTER TABLE responses 
ADD COLUMN defer_count INT DEFAULT 0,
ADD COLUMN skipped BOOLEAN DEFAULT FALSE;

-- ML Scores Table (Ranking Questions per User)
CREATE TABLE ml_question_scores (
    score_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id UUID REFERENCES questions(question_id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    relevance_score FLOAT NOT NULL,  -- ML-based question ranking
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for Optimized Query Performance
CREATE INDEX idx_questions_category ON questions(category);
CREATE INDEX idx_responses_user ON responses(user_id);
CREATE INDEX idx_responses_question ON responses(question_id);
CREATE INDEX idx_ml_scores ON ml_question_scores(user_id, question_id);

-- ===========================
-- Insert Sample Data
-- ===========================

-- Insert Sample Users (Anonymized)
INSERT INTO users (employee_id, full_name, ads_id, manager_id, manager_name, manager_email_hash, department, band, job_title, is_active, email_hash)
VALUES 
('EMP12345', 'Alice Johnson', 'ADS001', 'MGR001', 'Bob Smith', 'hash_mgr1', 'Engineering', 'Band 3', 'Software Engineer', TRUE, 'hash_emp1'),
('EMP67890', 'David Lee', 'ADS002', 'MGR002', 'Carol White', 'hash_mgr2', 'Product', 'Band 2', 'Product Manager', TRUE, 'hash_emp2');

-- Insert Sample Questions (With Types)
INSERT INTO questions (question_text, category, question_type, difficulty_level)
VALUES 
('How satisfied are you with the current tech stack?', 'Technology', 'comment', 3),
('How would you rate your collaboration with colleagues?', 'Colleague Experience', 'emoji', 2),
('Would you recommend your manager to others?', 'Leadership', 'radio', 4);

-- Insert Sample Responses (Comment-Based)
INSERT INTO responses (question_id, user_id, response_text, sentiment)
VALUES
((SELECT question_id FROM questions WHERE question_text = 'How satisfied are you with the current tech stack?' LIMIT 1),
 (SELECT user_id FROM users WHERE employee_id = 'EMP12345' LIMIT 1),
 'I feel we need better DevOps tools.', 'Neutral');

-- Insert Sample Responses (Emoji-Based)
INSERT INTO responses (question_id, user_id, response_emoji)
VALUES
((SELECT question_id FROM questions WHERE question_text = 'How would you rate your collaboration with colleagues?' LIMIT 1),
 (SELECT user_id FROM users WHERE employee_id = 'EMP67890' LIMIT 1),
 5);

-- Insert Sample Responses (Radio-Based)
INSERT INTO responses (question_id, user_id, response_radio)
VALUES
((SELECT question_id FROM questions WHERE question_text = 'Would you recommend your manager to others?' LIMIT 1),
 (SELECT user_id FROM users WHERE employee_id = 'EMP12345' LIMIT 1),
 'Yes');

-- Insert Sample ML Scores (ML-Based Question Ranking)
INSERT INTO ml_question_scores (question_id, user_id, relevance_score)
VALUES 
((SELECT question_id FROM questions WHERE question_text = 'How satisfied are you with the current tech stack?' LIMIT 1),
 (SELECT user_id FROM users WHERE employee_id = 'EMP12345' LIMIT 1),
 0.85);

select * from users;
select * from questions;
select * from responses;
select * from ml_question_scores

-- truncate table responses;
