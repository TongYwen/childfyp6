-- Migration: Add product recommendations for e-commerce integration
-- Created: 2025-11-28

-- Table to store recommended products with purchase links
CREATE TABLE IF NOT EXISTS `product_recommendations` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `child_id` INT(11) NOT NULL,
  `tutoring_result_id` INT(11) DEFAULT NULL,
  `product_name` VARCHAR(255) NOT NULL,
  `product_type` ENUM('book', 'learning_tool', 'stationery', 'toy', 'app', 'subscription', 'workbook', 'flashcard', 'game') NOT NULL,
  `description` TEXT,
  `age_range` VARCHAR(50) DEFAULT NULL,
  `price_myr` DECIMAL(10, 2) DEFAULT NULL,
  `amazon_url` VARCHAR(500) DEFAULT NULL,
  `shopee_url` VARCHAR(500) DEFAULT NULL,
  `lazada_url` VARCHAR(500) DEFAULT NULL,
  `popular_url` VARCHAR(500) DEFAULT NULL,
  `other_url` VARCHAR(500) DEFAULT NULL,
  `priority` ENUM('high', 'medium', 'low') DEFAULT 'medium',
  `reason` TEXT,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `child_id` (`child_id`),
  KEY `tutoring_result_id` (`tutoring_result_id`),
  CONSTRAINT `product_recommendations_ibfk_1` FOREIGN KEY (`child_id`) REFERENCES `children` (`id`) ON DELETE CASCADE,
  CONSTRAINT `product_recommendations_ibfk_2` FOREIGN KEY (`tutoring_result_id`) REFERENCES `ai_results` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table to track product clicks/purchases (analytics)
CREATE TABLE IF NOT EXISTS `product_clicks` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `product_recommendation_id` INT(11) NOT NULL,
  `parent_id` INT(11) NOT NULL,
  `retailer` VARCHAR(50) NOT NULL,
  `clicked_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `product_recommendation_id` (`product_recommendation_id`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `product_clicks_ibfk_1` FOREIGN KEY (`product_recommendation_id`) REFERENCES `product_recommendations` (`id`) ON DELETE CASCADE,
  CONSTRAINT `product_clicks_ibfk_2` FOREIGN KEY (`parent_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add index for better query performance
CREATE INDEX idx_product_type_priority ON product_recommendations(product_type, priority);
CREATE INDEX idx_child_created ON product_recommendations(child_id, created_at DESC);
