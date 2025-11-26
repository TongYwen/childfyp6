-- Rollback Migration: Drop user_sessions table
-- Purpose: Rollback the user_sessions table creation if needed
-- Date: 2025-11-26

DROP TABLE IF EXISTS user_sessions;
