-- Migration: Add product classification fields
-- Created: 2025-11-28

-- Add classification columns to product_recommendations table
ALTER TABLE `product_recommendations`
ADD COLUMN `category` ENUM('books', 'art_craft', 'math_tools', 'stationery', 'educational_toys', 'digital_apps', 'other') DEFAULT 'other' AFTER `product_type`,
ADD COLUMN `subject` ENUM('mathematics', 'english', 'science', 'social_emotional', 'physical_development', 'general') DEFAULT 'general' AFTER `category`,
ADD COLUMN `learning_style` ENUM('visual', 'auditory', 'kinesthetic', 'reading_writing', 'mixed') DEFAULT 'mixed' AFTER `subject`,
ADD COLUMN `price_range` ENUM('budget', 'mid_range', 'premium') DEFAULT 'budget' AFTER `price_myr`;

-- Add indexes for better query performance on classification fields
CREATE INDEX idx_category ON product_recommendations(category);
CREATE INDEX idx_subject ON product_recommendations(subject);
CREATE INDEX idx_learning_style ON product_recommendations(learning_style);
CREATE INDEX idx_price_range ON product_recommendations(price_range);

-- Update price_range based on existing prices
UPDATE product_recommendations
SET price_range = CASE
    WHEN price_myr <= 20 THEN 'budget'
    WHEN price_myr > 20 AND price_myr <= 50 THEN 'mid_range'
    WHEN price_myr > 50 THEN 'premium'
    ELSE 'budget'
END;
