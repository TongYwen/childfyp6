-- Migration Script: Add Structured Grade Level System
-- Date: 2025-11-30
-- Purpose: Implement standardized grade levels with subject mappings for ages 3-6

-- ============================================
-- 1. CREATE GRADE_LEVELS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS grade_levels (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(20) NOT NULL UNIQUE COMMENT 'Short code like NURSERY, K1, K2, GRADE1',
    name VARCHAR(50) NOT NULL COMMENT 'Display name like "Nursery"',
    description TEXT COMMENT 'Description of this grade level',
    min_age INT NOT NULL COMMENT 'Minimum recommended age in years',
    max_age INT NOT NULL COMMENT 'Maximum recommended age in years',
    display_order INT NOT NULL COMMENT 'Order for displaying in dropdowns',
    is_active TINYINT(1) DEFAULT 1 COMMENT 'Whether this grade level is currently in use',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert predefined grade levels for ages 3-6
INSERT INTO grade_levels (code, name, description, min_age, max_age, display_order, is_active) VALUES
('NURSERY', 'Nursery', 'Play-based learning with foundational skills for ages 3-4', 3, 4, 1, 1),
('K1', 'Kindergarten 1 (K1)', 'Early academics and basic skills for ages 4-5', 4, 5, 2, 1),
('K2', 'Kindergarten 2 (K2)', 'Pre-primary curriculum for ages 5-6', 5, 6, 3, 1),
('GRADE1', 'Grade 1 / Primary 1', 'Primary school curriculum for ages 6+', 6, 7, 4, 1);

-- ============================================
-- 2. CREATE SUBJECTS TABLE (Reference)
-- ============================================
CREATE TABLE IF NOT EXISTS subjects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(20) NOT NULL UNIQUE COMMENT 'Subject code like "english", "math"',
    name VARCHAR(50) NOT NULL COMMENT 'Display name',
    description TEXT,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert subjects (matching existing academic_scores subjects)
INSERT INTO subjects (code, name, description, is_active) VALUES
('english', 'English', 'English language and literacy skills', 1),
('chinese', 'Chinese', 'Chinese language skills', 1),
('bm', 'Bahasa Malaysia', 'Malay language skills', 1),
('math', 'Mathematics', 'Mathematical concepts and problem solving', 1),
('science', 'Science', 'Basic scientific concepts and exploration', 1);

-- ============================================
-- 3. CREATE GRADE_SUBJECT_MAPPINGS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS grade_subject_mappings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    grade_level_id INT NOT NULL,
    subject_id INT NOT NULL,
    is_core TINYINT(1) DEFAULT 1 COMMENT 'Whether this subject is core (required) for this grade',
    is_recommended TINYINT(1) DEFAULT 1 COMMENT 'Whether formal assessment is recommended',
    description TEXT COMMENT 'Grade-specific subject description/expectations',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grade_level_id) REFERENCES grade_levels(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    UNIQUE KEY unique_grade_subject (grade_level_id, subject_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Define which subjects are appropriate for each grade level
-- NURSERY (ages 3-4): Only basic English and Math
INSERT INTO grade_subject_mappings (grade_level_id, subject_id, is_core, is_recommended, description)
SELECT
    gl.id,
    s.id,
    CASE
        WHEN s.code IN ('english', 'math') THEN 1
        ELSE 0
    END as is_core,
    CASE
        WHEN s.code IN ('english', 'math') THEN 1
        ELSE 0
    END as is_recommended,
    CASE
        WHEN s.code = 'english' THEN 'Basic vocabulary, colors, shapes, animals. Focus on listening and simple words.'
        WHEN s.code = 'math' THEN 'Counting 1-10, basic shapes, colors, size concepts. Play-based learning.'
        WHEN s.code = 'chinese' THEN 'Not recommended for formal assessment at this age. Optional exposure only.'
        WHEN s.code = 'bm' THEN 'Not recommended for formal assessment at this age. Optional exposure only.'
        WHEN s.code = 'science' THEN 'Not recommended for formal assessment at this age. Exploration only.'
    END as description
FROM grade_levels gl
CROSS JOIN subjects s
WHERE gl.code = 'NURSERY';

-- K1 (ages 4-5): English, Math core; Chinese/Malay optional; Science basic
INSERT INTO grade_subject_mappings (grade_level_id, subject_id, is_core, is_recommended, description)
SELECT
    gl.id,
    s.id,
    CASE
        WHEN s.code IN ('english', 'math') THEN 1
        ELSE 0
    END as is_core,
    CASE
        WHEN s.code IN ('english', 'math', 'science') THEN 1
        WHEN s.code IN ('chinese', 'bm') THEN 1  -- Optional but can be assessed
        ELSE 0
    END as is_recommended,
    CASE
        WHEN s.code = 'english' THEN 'Alphabet recognition, simple words, phonics. Basic reading readiness.'
        WHEN s.code = 'math' THEN 'Counting to 20, number recognition, basic addition concepts, patterns.'
        WHEN s.code = 'chinese' THEN 'Optional: Basic characters, simple words. Can start formal introduction.'
        WHEN s.code = 'bm' THEN 'Optional: Basic vocabulary, simple phrases. Can start formal introduction.'
        WHEN s.code = 'science' THEN 'Basic concepts: living vs non-living, weather, plants, animals.'
    END as description
FROM grade_levels gl
CROSS JOIN subjects s
WHERE gl.code = 'K1';

-- K2 (ages 5-6): All subjects recommended
INSERT INTO grade_subject_mappings (grade_level_id, subject_id, is_core, is_recommended, description)
SELECT
    gl.id,
    s.id,
    1 as is_core,  -- All subjects are core at K2 level
    1 as is_recommended,
    CASE
        WHEN s.code = 'english' THEN 'Reading simple sentences, writing letters/simple words, storytelling.'
        WHEN s.code = 'math' THEN 'Counting to 50+, addition/subtraction within 10, measurement, time concepts.'
        WHEN s.code = 'chinese' THEN 'Character recognition, simple reading, basic writing strokes.'
        WHEN s.code = 'bm' THEN 'Basic reading and writing, simple conversations, common vocabulary.'
        WHEN s.code = 'science' THEN 'Scientific observation, simple experiments, nature, basic life cycles.'
    END as description
FROM grade_levels gl
CROSS JOIN subjects s
WHERE gl.code = 'K2';

-- GRADE1 (ages 6+): Full primary curriculum
INSERT INTO grade_subject_mappings (grade_level_id, subject_id, is_core, is_recommended, description)
SELECT
    gl.id,
    s.id,
    1 as is_core,
    1 as is_recommended,
    CASE
        WHEN s.code = 'english' THEN 'Formal reading and writing, comprehension, grammar basics, creative writing.'
        WHEN s.code = 'math' THEN 'Addition/subtraction mastery, introduction to multiplication, word problems.'
        WHEN s.code = 'chinese' THEN 'Formal reading and writing, character strokes, simple compositions.'
        WHEN s.code = 'bm' THEN 'Formal curriculum: reading, writing, grammar, comprehension.'
        WHEN s.code = 'science' THEN 'Formal science concepts, experiments, scientific method basics.'
    END as description
FROM grade_levels gl
CROSS JOIN subjects s
WHERE gl.code = 'GRADE1';

-- ============================================
-- 4. UPDATE CHILDREN TABLE
-- ============================================
-- Add grade_level_code column to store standardized grade level
ALTER TABLE children
ADD COLUMN grade_level_code VARCHAR(20) DEFAULT NULL COMMENT 'Standardized grade level code' AFTER grade_level,
ADD INDEX idx_grade_level_code (grade_level_code);

-- Optionally add foreign key (commented out for flexibility)
-- ALTER TABLE children
-- ADD CONSTRAINT fk_children_grade_level
-- FOREIGN KEY (grade_level_code) REFERENCES grade_levels(code) ON DELETE SET NULL;

-- ============================================
-- 5. MIGRATE EXISTING DATA
-- ============================================
-- Migrate existing free-text grade_level to standardized codes
-- This is a best-effort migration based on common patterns

-- Update exact matches (case-insensitive)
UPDATE children
SET grade_level_code = 'NURSERY'
WHERE LOWER(TRIM(grade_level)) IN ('nursery', 'n', 'pre-nursery');

UPDATE children
SET grade_level_code = 'K1'
WHERE LOWER(TRIM(grade_level)) IN ('k1', 'kindergarten 1', 'kinder 1', 'kg1');

UPDATE children
SET grade_level_code = 'K2'
WHERE LOWER(TRIM(grade_level)) IN ('k2', 'kindergarten 2', 'kinder 2', 'kg2');

UPDATE children
SET grade_level_code = 'GRADE1'
WHERE LOWER(TRIM(grade_level)) IN ('grade 1', 'grade1', 'primary 1', 'p1', '1', 'standard 1');

-- For single letter grades (a, b, etc.) - map to K1 or K2 based on age
UPDATE children c
SET grade_level_code = CASE
    WHEN c.age <= 4 THEN 'K1'
    WHEN c.age >= 5 THEN 'K2'
    ELSE 'K1'
END
WHERE LOWER(TRIM(grade_level)) IN ('a', 'b', 'c')
AND grade_level_code IS NULL;

-- For any remaining unmapped children, infer from age
UPDATE children
SET grade_level_code = CASE
    WHEN age <= 3 THEN 'NURSERY'
    WHEN age = 4 THEN 'K1'
    WHEN age = 5 THEN 'K2'
    WHEN age >= 6 THEN 'GRADE1'
    ELSE 'K1'  -- Default to K1 if age is unknown
END
WHERE grade_level_code IS NULL;

-- ============================================
-- 6. CREATE HELPER VIEWS
-- ============================================
-- View to easily see children with their grade level details
CREATE OR REPLACE VIEW v_children_with_grade AS
SELECT
    c.id,
    c.parent_id,
    c.name,
    c.dob,
    c.age,
    c.grade_level as grade_level_legacy,
    c.grade_level_code,
    gl.name as grade_level_name,
    gl.description as grade_level_description,
    gl.min_age as grade_min_age,
    gl.max_age as grade_max_age,
    c.gender,
    c.notes,
    c.created_at
FROM children c
LEFT JOIN grade_levels gl ON c.grade_level_code = gl.code;

-- View to see which subjects are available/recommended for each child
CREATE OR REPLACE VIEW v_child_available_subjects AS
SELECT
    c.id as child_id,
    c.name as child_name,
    c.grade_level_code,
    gl.name as grade_level_name,
    s.code as subject_code,
    s.name as subject_name,
    gsm.is_core,
    gsm.is_recommended,
    gsm.description as subject_expectations
FROM children c
LEFT JOIN grade_levels gl ON c.grade_level_code = gl.code
LEFT JOIN grade_subject_mappings gsm ON gl.id = gsm.grade_level_id
LEFT JOIN subjects s ON gsm.subject_id = s.id
WHERE gsm.is_recommended = 1  -- Only show recommended subjects
ORDER BY c.id, gl.display_order, s.code;

-- ============================================
-- VERIFICATION QUERIES (Run these to check)
-- ============================================
-- SELECT * FROM grade_levels;
-- SELECT * FROM subjects;
-- SELECT * FROM grade_subject_mappings;
-- SELECT * FROM v_children_with_grade;
-- SELECT * FROM v_child_available_subjects;
-- SELECT grade_level, grade_level_code, COUNT(*) FROM children GROUP BY grade_level, grade_level_code;

-- ============================================
-- ROLLBACK (if needed - use with caution!)
-- ============================================
-- DROP VIEW IF EXISTS v_child_available_subjects;
-- DROP VIEW IF EXISTS v_children_with_grade;
-- ALTER TABLE children DROP COLUMN grade_level_code;
-- DROP TABLE IF EXISTS grade_subject_mappings;
-- DROP TABLE IF EXISTS subjects;
-- DROP TABLE IF EXISTS grade_levels;
