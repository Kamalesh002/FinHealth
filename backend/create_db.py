"""
Script to create the PostgreSQL database for SME Financial Health Platform
Run this once before starting the application
"""
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

# Database configuration - update password as needed
DB_NAME = "financial_health"
DB_USER = "postgres"
DB_PASSWORD = "Kamalesh@123"  # Change this to your actual password
DB_HOST = "localhost"
DB_PORT = "5432"

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to default 'postgres' database first
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"✅ Database '{DB_NAME}' created successfully!")
        else:
            print(f"ℹ️ Database '{DB_NAME}' already exists.")
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ PostgreSQL connection successful!")
        print(f"   Host: {DB_HOST}:{DB_PORT}")
        print(f"   Database: {DB_NAME}")
        print(f"   User: {DB_USER}")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ Failed to connect to PostgreSQL!")
        print(f"   Error: {e}")
        print(f"\n💡 Tips:")
        print(f"   1. Make sure PostgreSQL is running")
        print(f"   2. Check the password in this script (line 13)")
        print(f"   3. Update the .env file with the correct password")
        return False

if __name__ == "__main__":
    success = create_database()
    sys.exit(0 if success else 1)
