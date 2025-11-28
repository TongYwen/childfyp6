-- Migration Script: Add Soft Delete Support to Users Table
-- Date: 2025-01-28
-- Purpose: Enable soft delete functionality for inactive parent management

-- Add deleted_at column to track when account was soft deleted
ALTER TABLE users
ADD COLUMN deleted_at TIMESTAMP NULL DEFAULT NULL AFTER inactive_warning_sent;

-- Add deletion_reason column to track why account was deleted
ALTER TABLE users
ADD COLUMN deletion_reason VARCHAR(255) DEFAULT NULL AFTER deleted_at;

-- Verify the columns were added successfully
-- Run this query to check:
-- DESCRIBE users;

-- Expected output should show:
-- | deleted_at       | timestamp    | YES  |     | NULL                |                             |
-- | deletion_reason  | varchar(255) | YES  |     | NULL                |                             |
