-- Migration script to add updated_at column to orders table
-- Run this script on your database to add the updated_at column

ALTER TABLE tony.orders 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE;

-- Add comment to the column
COMMENT ON COLUMN tony.orders.updated_at IS 'Timestamp when the order was last updated';

