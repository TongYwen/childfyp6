-- =====================================================
-- Purchasable Learning Resources Database Schema
-- Supports direct purchase links to e-commerce sites
-- =====================================================

-- Main resources table with purchase information
CREATE TABLE IF NOT EXISTS purchasable_resources (
    id INT PRIMARY KEY AUTO_INCREMENT,

    -- Basic Information
    title VARCHAR(255) NOT NULL,
    description TEXT,
    type ENUM('book', 'workbook', 'flashcards', 'learning_toy', 'stationery', 'app', 'digital_course') NOT NULL,
    category VARCHAR(100), -- Math, Reading, Science, Art, etc.

    -- Target Audience
    min_age INT NOT NULL,
    max_age INT NOT NULL,
    grade_level VARCHAR(50),
    learning_style VARCHAR(50), -- visual, auditory, kinesthetic, reading

    -- Product Details
    author VARCHAR(255),
    publisher VARCHAR(255),
    isbn VARCHAR(20), -- For books
    language VARCHAR(50) DEFAULT 'English',
    pages INT, -- For books

    -- Media
    image_url VARCHAR(500),
    thumbnail_url VARCHAR(500),

    -- Pricing (in Malaysian Ringgit)
    price_rm DECIMAL(10, 2) NOT NULL,
    original_price_rm DECIMAL(10, 2), -- For showing discounts
    currency VARCHAR(10) DEFAULT 'MYR',

    -- Quality & Safety
    quality_rating DECIMAL(3, 2) DEFAULT 0, -- 0-5 stars
    review_count INT DEFAULT 0,
    safety_certified BOOLEAN DEFAULT FALSE,
    age_appropriate_verified BOOLEAN DEFAULT FALSE,

    -- Availability
    in_stock BOOLEAN DEFAULT TRUE,
    available_from DATE,
    available_until DATE,

    -- SEO & Search
    keywords TEXT, -- Comma-separated keywords
    tags TEXT, -- Comma-separated tags

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT, -- Admin user ID

    INDEX idx_type (type),
    INDEX idx_category (category),
    INDEX idx_age (min_age, max_age),
    INDEX idx_price (price_rm),
    INDEX idx_rating (quality_rating),
    FOREIGN KEY (created_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Purchase links to multiple e-commerce platforms
CREATE TABLE IF NOT EXISTS resource_purchase_links (
    id INT PRIMARY KEY AUTO_INCREMENT,
    resource_id INT NOT NULL,

    -- Platform Information
    platform ENUM('shopee', 'lazada', 'bookxcess', 'kinokuniya', 'popular', 'amazon', 'carousell', 'official_website') NOT NULL,
    platform_name VARCHAR(100),

    -- Purchase Link
    url VARCHAR(1000) NOT NULL,
    affiliate_link VARCHAR(1000), -- For monetization
    deep_link VARCHAR(1000), -- Mobile app deep link

    -- Pricing on this platform
    price_on_platform DECIMAL(10, 2),
    shipping_cost DECIMAL(10, 2) DEFAULT 0,
    free_shipping_threshold DECIMAL(10, 2),

    -- Availability
    in_stock BOOLEAN DEFAULT TRUE,
    delivery_days INT, -- Estimated delivery

    -- Seller Information
    seller_name VARCHAR(255),
    seller_rating DECIMAL(3, 2),
    verified_seller BOOLEAN DEFAULT FALSE,

    -- Tracking
    click_count INT DEFAULT 0,
    purchase_count INT DEFAULT 0, -- If we can track conversions
    last_verified TIMESTAMP, -- Last time link was checked

    -- Promotions
    promo_code VARCHAR(50),
    promo_description TEXT,
    promo_valid_until DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (resource_id) REFERENCES purchasable_resources(id) ON DELETE CASCADE,
    INDEX idx_platform (platform),
    INDEX idx_price (price_on_platform),
    UNIQUE KEY unique_resource_platform (resource_id, platform, url(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Track user clicks and purchases
CREATE TABLE IF NOT EXISTS resource_clicks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    child_id INT NOT NULL,
    resource_id INT NOT NULL,
    link_id INT, -- Which purchase link they clicked

    -- Click Information
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    platform VARCHAR(50),
    device VARCHAR(50), -- mobile, desktop, tablet

    -- Purchase Tracking (if available)
    purchased BOOLEAN DEFAULT FALSE,
    purchase_amount DECIMAL(10, 2),
    purchased_at TIMESTAMP NULL,

    -- Referral
    referral_code VARCHAR(100),
    commission_earned DECIMAL(10, 2),

    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    FOREIGN KEY (resource_id) REFERENCES purchasable_resources(id) ON DELETE CASCADE,
    FOREIGN KEY (link_id) REFERENCES resource_purchase_links(id) ON DELETE SET NULL,
    INDEX idx_child (child_id),
    INDEX idx_resource (resource_id),
    INDEX idx_purchased (purchased)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- User wishlists
CREATE TABLE IF NOT EXISTS resource_wishlists (
    id INT PRIMARY KEY AUTO_INCREMENT,
    child_id INT NOT NULL,
    resource_id INT NOT NULL,

    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    priority INT DEFAULT 0, -- 0=low, 1=medium, 2=high
    notes TEXT,
    purchased BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    FOREIGN KEY (resource_id) REFERENCES purchasable_resources(id) ON DELETE CASCADE,
    UNIQUE KEY unique_child_resource (child_id, resource_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Resource reviews from parents
CREATE TABLE IF NOT EXISTS resource_reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    resource_id INT NOT NULL,
    user_id INT NOT NULL,
    child_id INT, -- Optional: which child used it

    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,

    -- Specific ratings
    value_for_money INT CHECK (value_for_money BETWEEN 1 AND 5),
    educational_value INT CHECK (educational_value BETWEEN 1 AND 5),
    engagement INT CHECK (engagement BETWEEN 1 AND 5),
    quality INT CHECK (quality BETWEEN 1 AND 5),

    -- Usage
    child_age_when_used INT,
    duration_used VARCHAR(50), -- "1 week", "3 months", etc.
    would_recommend BOOLEAN DEFAULT TRUE,

    -- Verification
    verified_purchase BOOLEAN DEFAULT FALSE,
    helpful_count INT DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (resource_id) REFERENCES purchasable_resources(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE SET NULL,
    INDEX idx_rating (rating),
    INDEX idx_verified (verified_purchase)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =====================================================
-- Sample Data: Popular Learning Resources in Malaysia
-- =====================================================

-- Books
INSERT INTO purchasable_resources (title, description, type, category, min_age, max_age, author, publisher, isbn, price_rm, original_price_rm, quality_rating, review_count, image_url) VALUES
('Phonics Fun Activity Book', 'Comprehensive phonics workbook with 200+ activities for early readers', 'workbook', 'Reading', 4, 6, 'Sarah Johnson', 'Scholastic', '9781234567890', 19.90, 29.90, 4.5, 128, '/static/images/resources/phonics_fun.jpg'),
('Math Made Easy: Kindergarten', 'Fun math exercises covering counting, shapes, and basic addition', 'workbook', 'Math', 5, 6, 'Dr. Lee Wei Ming', 'Oxford Fajar', '9789876543210', 24.90, 0, 4.7, 95, '/static/images/resources/math_easy.jpg'),
('My First 1000 Words', 'Colorful picture dictionary with English and Bahasa Malaysia', 'book', 'Language', 3, 7, 'Various', 'Popular Publishing', '9781111222333', 35.00, 45.00, 4.8, 203, '/static/images/resources/1000_words.jpg'),
('Science Experiments for Kids', '50 safe and fun science experiments using household items', 'book', 'Science', 6, 10, 'Prof. Ahmad Ibrahim', 'Times Publishing', '9784444555666', 29.90, 0, 4.6, 87, '/static/images/resources/science_exp.jpg');

-- Learning Toys
INSERT INTO purchasable_resources (title, description, type, category, min_age, max_age, price_rm, quality_rating, review_count, image_url) VALUES
('Magnetic Letter Set (52pcs)', 'Colorful magnetic uppercase and lowercase letters for learning alphabets', 'learning_toy', 'Reading', 3, 6, 39.90, 4.4, 156, '/static/images/resources/magnetic_letters.jpg'),
('Counting Bears with Sorting Cups', '60 colorful counting bears with 6 sorting cups for math activities', 'learning_toy', 'Math', 3, 6, 45.00, 4.7, 189, '/static/images/resources/counting_bears.jpg'),
('Wooden Puzzle - Malaysia Map', 'Educational wooden puzzle of Malaysian states', 'learning_toy', 'Geography', 5, 8, 32.90, 4.5, 72, '/static/images/resources/malaysia_puzzle.jpg');

-- Stationery
INSERT INTO purchasable_resources (title, description, type, category, min_age, max_age, price_rm, image_url) VALUES
('Faber-Castell Colour Pencils (24 colors)', 'High-quality non-toxic colour pencils for creative artwork', 'stationery', 'Art', 3, 12, 15.90, '/static/images/resources/colour_pencils.jpg'),
('Learning to Write Practice Book', 'Tracing and writing practice sheets for preschoolers', 'workbook', 'Writing', 4, 6, 12.90, '/static/images/resources/writing_practice.jpg'),
('Flashcards Set - Animals & Numbers', 'Double-sided laminated flashcards with pictures and words', 'flashcards', 'Multiple', 2, 5, 18.90, '/static/images/resources/flashcards.jpg');

-- Digital Resources
INSERT INTO purchasable_resources (title, description, type, category, min_age, max_age, price_rm, quality_rating, image_url) VALUES
('ABCmouse Annual Subscription', 'Complete online curriculum for ages 2-8', 'digital_course', 'Multiple', 2, 8, 360.00, 4.6, '/static/images/resources/abcmouse.jpg'),
('Khan Academy Kids Premium', 'Ad-free learning app with advanced features', 'app', 'Multiple', 2, 7, 120.00, 4.7, '/static/images/resources/khan_kids.jpg');


-- =====================================================
-- Sample Purchase Links (Malaysian E-commerce)
-- =====================================================

-- Phonics Fun Activity Book - Available on multiple platforms
INSERT INTO resource_purchase_links (resource_id, platform, url, price_on_platform, in_stock, delivery_days, seller_rating) VALUES
(1, 'shopee', 'https://shopee.com.my/Phonics-Fun-Activity-Book-i.123456789', 19.90, TRUE, 3, 4.8),
(1, 'lazada', 'https://www.lazada.com.my/products/phonics-fun-activity-book-i123456789.html', 21.90, TRUE, 2, 4.7),
(1, 'bookxcess', 'https://www.bookxcess.com/phonics-fun-activity-book', 17.90, TRUE, 5, 5.0),
(1, 'popular', 'https://www.popular.com.my/phonics-fun-activity-book', 22.90, TRUE, 3, 4.9);

-- Math Made Easy - Available with promotions
INSERT INTO resource_purchase_links (resource_id, platform, url, price_on_platform, free_shipping_threshold, promo_code, promo_description, delivery_days) VALUES
(2, 'shopee', 'https://shopee.com.my/Math-Made-Easy-Kindergarten-i.987654321', 24.90, 50.00, 'EDU10', 'RM10 off for education books', 2),
(2, 'lazada', 'https://www.lazada.com.my/products/math-made-easy-kindergarten-i987654321.html', 24.90, 40.00, NULL, NULL, 3);

-- Learning Toys
INSERT INTO resource_purchase_links (resource_id, platform, url, price_on_platform, delivery_days) VALUES
(5, 'shopee', 'https://shopee.com.my/Magnetic-Letter-Set-52pcs-i.111222333', 39.90, 3),
(5, 'lazada', 'https://www.lazada.com.my/products/magnetic-letter-set-52pcs-i111222333.html', 42.90, 2),
(6, 'shopee', 'https://shopee.com.my/Counting-Bears-with-Sorting-Cups-i.444555666', 45.00, 4),
(6, 'lazada', 'https://www.lazada.com.my/products/counting-bears-sorting-cups-i444555666.html', 47.90, 3);


-- =====================================================
-- Useful Views for Quick Queries
-- =====================================================

-- View: Resources with best prices
CREATE OR REPLACE VIEW resources_best_prices AS
SELECT
    pr.id,
    pr.title,
    pr.type,
    pr.category,
    pr.min_age,
    pr.max_age,
    pr.price_rm as base_price,
    MIN(rpl.price_on_platform) as best_price,
    (SELECT platform FROM resource_purchase_links
     WHERE resource_id = pr.id
     ORDER BY price_on_platform ASC LIMIT 1) as best_platform,
    (SELECT url FROM resource_purchase_links
     WHERE resource_id = pr.id
     ORDER BY price_on_platform ASC LIMIT 1) as best_url
FROM purchasable_resources pr
LEFT JOIN resource_purchase_links rpl ON pr.id = rpl.resource_id
WHERE pr.in_stock = TRUE AND rpl.in_stock = TRUE
GROUP BY pr.id;


-- View: Popular resources (most clicked/purchased)
CREATE OR REPLACE VIEW popular_resources AS
SELECT
    pr.id,
    pr.title,
    pr.type,
    pr.category,
    pr.price_rm,
    pr.quality_rating,
    COUNT(DISTINCT rc.id) as click_count,
    SUM(CASE WHEN rc.purchased THEN 1 ELSE 0 END) as purchase_count,
    (SUM(CASE WHEN rc.purchased THEN 1 ELSE 0 END) / COUNT(DISTINCT rc.id)) * 100 as conversion_rate
FROM purchasable_resources pr
LEFT JOIN resource_clicks rc ON pr.id = rc.resource_id
GROUP BY pr.id
ORDER BY click_count DESC, purchase_count DESC;


-- View: Age-appropriate resources
CREATE OR REPLACE VIEW resources_by_age AS
SELECT
    pr.*,
    MIN(rpl.price_on_platform) as lowest_price,
    COUNT(DISTINCT rr.id) as review_count_actual,
    AVG(rr.rating) as avg_user_rating
FROM purchasable_resources pr
LEFT JOIN resource_purchase_links rpl ON pr.id = rpl.resource_id
LEFT JOIN resource_reviews rr ON pr.id = rr.resource_id
GROUP BY pr.id;
