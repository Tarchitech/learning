#!/usr/bin/env python3
"""
Script to add updated_at column to orders table.
Run this script to migrate the database schema.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine
from sqlalchemy import text


def add_updated_at_column():
    """Add updated_at column to orders table."""
    try:
        with engine.connect() as conn:
            # Check if column already exists
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'tony' 
                AND table_name = 'orders' 
                AND column_name = 'updated_at'
            """)
            result = conn.execute(check_query)
            if result.fetchone():
                print("Column 'updated_at' already exists in tony.orders table.")
                return
            
            # Add the column
            alter_query = text("""
                ALTER TABLE tony.orders 
                ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE
            """)
            conn.execute(alter_query)
            conn.commit()
            print("Successfully added 'updated_at' column to tony.orders table.")
            
    except Exception as e:
        print(f"Error adding updated_at column: {str(e)}")
        print("Please run the SQL script manually:")
        print("ALTER TABLE tony.orders ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE;")
        sys.exit(1)


if __name__ == "__main__":
    print("Adding updated_at column to orders table...")
    add_updated_at_column()
    print("Migration completed successfully!")

