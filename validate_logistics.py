#!/usr/bin/env python3
"""
Additional SQL Queries to verify logistics context for city pairs
"""

import os
import psycopg2

# SECURITY: Use environment variables for credentials. Never hardcode passwords.
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "zippy_logistics"),
    "user": os.getenv("DB_USER", "zippy"),
    "password": os.getenv("DB_PASSWORD", ""),  # REQUIRED: set DB_PASSWORD env var
}


def run_query(conn, query, params=None):
    """Execute a query and return results"""
    with conn.cursor() as cur:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        return cur.fetchall()


def main():
    conn = psycopg2.connect(**DB_CONFIG)

    print("=" * 80)
    print("ADDITIONAL SQL QUERIES FOR LOGISTICS CONTEXT VALIDATION")
    print("=" * 80)

    # Query 1: Find records mentioning top city pairs with logistics keywords
    print("\n--- Query 1: Records with Delhi-Mumbai pair + logistics keywords ---")
    query1 = """
    SELECT 
        'raw_web_data' as source,
        LEFT(content, 150) as snippet
    FROM raw_web_data 
    WHERE content ~* 'Delhi.*Mumbai|Mumbai.*Delhi'
    AND content ~* 'freight|cargo|transport|logistics|shipping|trade|route|corridor|movement'
    
    UNION ALL
    
    SELECT 
        'pdf_chunks' as source,
        LEFT(chunk_text, 150) as snippet
    FROM pdf_chunks 
    WHERE chunk_text ~* 'Delhi.*Mumbai|Mumbai.*Delhi'
    AND chunk_text ~* 'freight|cargo|transport|logistics|shipping|trade|route|corridor|movement'
    LIMIT 5;
    """
    results = run_query(conn, query1)
    for i, row in enumerate(results, 1):
        print(f"{i}. [{row[0]}] {row[1]}...")

    # Query 2: Count records with logistics context by source
    print("\n--- Query 2: Count of logistics-related records by table ---")
    query2 = """
    SELECT 
        'raw_web_data' as source,
        COUNT(*) as logistics_records
    FROM raw_web_data 
    WHERE content ~* 'freight|cargo|transport|logistics|shipping|trade|route|corridor|movement'
    
    UNION ALL
    
    SELECT 
        'pdf_chunks' as source,
        COUNT(*) as logistics_records
    FROM pdf_chunks 
    WHERE chunk_text ~* 'freight|cargo|transport|logistics|shipping|trade|route|corridor|movement';
    """
    results = run_query(conn, query2)
    for row in results:
        print(f"  {row[0]}: {row[1]} records")

    # Query 3: Top cities appearing with logistics keywords
    print("\n--- Query 3: Sample of city co-occurrences in logistics context ---")
    logistics_keywords = (
        "freight|cargo|transport|logistics|shipping|trade|route|corridor"
    )

    query3 = f"""
    SELECT 
        'pdf_chunks' as source,
        file_name,
        chunk_index,
        LEFT(chunk_text, 200) as snippet
    FROM pdf_chunks 
    WHERE chunk_text ~* 'Delhi.*Ahmedabad|Ahmedabad.*Delhi'
    AND chunk_text ~* '{logistics_keywords}'
    LIMIT 3;
    """
    results = run_query(conn, query3)
    for i, row in enumerate(results, 1):
        print(f"\n{i}. Source: {row[0]}, File: {row[1]}, Chunk: {row[2]}")
        print(f"   Text: {row[3]}...")

    # Query 4: Data sources overview
    print("\n--- Query 4: Data sources overview ---")
    query4 = """
    SELECT 
        source,
        COUNT(*) as record_count,
        MIN(scraped_at) as earliest,
        MAX(scraped_at) as latest
    FROM raw_web_data 
    GROUP BY source;
    """
    try:
        results = run_query(conn, query4)
        print("\nRaw web data sources:")
        for row in results:
            print(f"  {row[0]}: {row[1]} records (from {row[2]} to {row[3]})")
    except:
        print("  (Could not retrieve web data sources)")

    query5 = """
    SELECT 
        file_name,
        COUNT(*) as chunk_count,
        MIN(extracted_at) as earliest,
        MAX(extracted_at) as latest
    FROM pdf_chunks 
    GROUP BY file_name
    ORDER BY chunk_count DESC
    LIMIT 5;
    """
    results = run_query(conn, query5)
    print("\nTop PDF sources (by chunk count):")
    for row in results:
        print(f"  {row[0]}: {row[1]} chunks (from {row[2]} to {row[3]})")

    print("\n" + "=" * 80)
    print("DETAILED SQL QUERIES FOR FURTHER ANALYSIS")
    print("=" * 80)

    print("""
-- Count city mentions with logistics context
SELECT 
    CASE 
        WHEN content ~* 'Mumbai' THEN 'Mumbai'
        WHEN content ~* 'Delhi' THEN 'Delhi'
        WHEN content ~* 'Chennai' THEN 'Chennai'
        WHEN content ~* 'Kolkata' THEN 'Kolkata'
        WHEN content ~* 'Bangalore' THEN 'Bangalore'
        WHEN content ~* 'Ahmedabad' THEN 'Ahmedabad'
        WHEN content ~* 'Hyderabad' THEN 'Hyderabad'
        WHEN content ~* 'Pune' THEN 'Pune'
    END as city,
    COUNT(*) as mentions
FROM pdf_chunks
WHERE chunk_text ~* 'freight|cargo|transport|logistics|shipping|trade|route|corridor'
GROUP BY city
ORDER BY mentions DESC;

-- Find specific city pair co-occurrences
SELECT 
    file_name,
    chunk_index,
    LEFT(chunk_text, 300) as context
FROM pdf_chunks
WHERE chunk_text ~* 'Bangalore'
AND chunk_text ~* 'Mumbai'
AND chunk_text ~* 'logistics|freight|transport'
ORDER BY chunk_index;

-- Extract date range of data
SELECT 
    MIN(extracted_at) as earliest_record,
    MAX(extracted_at) as latest_record,
    COUNT(DISTINCT file_name) as unique_files
FROM pdf_chunks;
""")

    conn.close()
    print("\n[OK] Validation queries completed.")


if __name__ == "__main__":
    main()
