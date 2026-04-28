import psycopg2
import os
from urllib.parse import urlparse

# Get DATABASE_URL from environment
db_url = os.getenv("DATABASE_URL")

if not db_url:
    print("FAILED: DATABASE_URL environment variable is not set.")
    exit(1)

try:
    # Try to connect
    conn = psycopg2.connect(db_url)
    print("SUCCESS: Connected to database")
    
    # Check table existence
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = [row[0] for row in cur.fetchall()]
        print(f"Tables found: {tables}")
        
        if 'vehicle_models' in tables:
            cur.execute("SELECT COUNT(*) FROM vehicle_models;")
            count = cur.fetchone()[0]
            print(f"Records in vehicle_models: {count}")
            
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")

