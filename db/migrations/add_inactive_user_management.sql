-- Migration: Add inactive user management fields
-- Date: 2025-11-27
-- Description: Adds fields for tracking user login activity and managing automatic account deletion

-- Add new columns to users table
ALTER TABLE `users`
ADD COLUMN `last_login` timestamp NULL DEFAULT NULL AFTER `created_at`,
ADD COLUMN `is_active` tinyint(1) DEFAULT 1 AFTER `last_login`,
ADD COLUMN `protected_from_deletion` tinyint(1) DEFAULT 0 AFTER `is_active`,
ADD COLUMN `inactive_warning_sent` timestamp NULL DEFAULT NULL AFTER `protected_from_deletion`;

-- Initialize last_login for existing users to their created_at timestamp
-- This prevents immediate deletion of existing accounts
UPDATE `users` SET `last_login` = `created_at` WHERE `last_login` IS NULL;

-- Add index for performance on inactive user queries
CREATE INDEX idx_last_login ON `users`(`last_login`);
CREATE INDEX idx_is_active ON `users`(`is_active`);
CREATE INDEX idx_protected_from_deletion ON `users`(`protected_from_deletion`);
