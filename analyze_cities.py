#!/usr/bin/env python3
"""
PostgreSQL Database Analysis Script for Zippy Logistics
Analyzes city pairs in logistics context from raw_web_data and pdf_chunks tables
"""

import sys
import re
from collections import Counter

# Try to import psycopg2, if not available, install it
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("psycopg2 not found. Installing...")
    import subprocess

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "psycopg2-binary", "-q"]
    )
    import psycopg2
    from psycopg2.extras import RealDictCursor

# Database connection parameters
# SECURITY: Use environment variables for credentials. Never hardcode passwords.
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "zippy_logistics"),
    "user": os.getenv("DB_USER", "zippy"),
    "password": os.getenv("DB_PASSWORD", ""),  # REQUIRED: set DB_PASSWORD env var
}

# Major Indian cities list
INDIAN_CITIES = [
    "Mumbai",
    "Delhi",
    "Chennai",
    "Kolkata",
    "Bangalore",
    "Hyderabad",
    "Ahmedabad",
    "Pune",
    "Surat",
    "Jaipur",
    "Kanpur",
    "Lucknow",
    "Nagpur",
    "Indore",
    "Thane",
    "Bhopal",
    "Visakhapatnam",
    "Pimpri",
    "Patna",
    "Vadodara",
    "Ghaziabad",
    "Ludhiana",
    "Agra",
    "Nashik",
    "Faridabad",
    "Meerut",
    "Rajkot",
    "Kalyan",
    "Dombivli",
    "Varanasi",
    "Srinagar",
    "Aurangabad",
    "Dhanbad",
    "Amritsar",
    "Navi Mumbai",
    "Allahabad",
    "Ranchi",
    "Howrah",
    "Coimbatore",
    "Jabalpur",
    "Gwalior",
    "Vijayawada",
    "Jodhpur",
    "Madurai",
    "Raipur",
    "Kota",
    "Guwahati",
    "Chandigarh",
    "Solapur",
    "Hubli",
    "Dharwad",
    "Tiruchirappalli",
    "Bareilly",
    "Mysore",
    "Tiruppur",
    "Gurgaon",
    "Aligarh",
    "Jalandhar",
    "Bhubaneswar",
    "Salem",
    "Warangal",
    "Guntur",
    "Bhiwandi",
    "Saharanpur",
    "Gorakhpur",
    "Bikaner",
    "Amravati",
    "Noida",
    "Jamshedpur",
    "Bhilai",
    "Cuttack",
    "Firozabad",
    "Kochi",
    "Nellore",
    "Bhavnagar",
    "Dehradun",
    "Durgapur",
    "Asansol",
    "Rourkela",
    "Nanded",
    "Kolhapur",
    "Ajmer",
    "Akola",
    "Gulbarga",
    "Jamnagar",
    "Ujjain",
    "Loni",
    "Siliguri",
    "Jhansi",
    "Ulhasnagar",
    "Jammu",
    "Sangli",
    "Miraj",
    "Kupwad",
    "Mangalore",
    "Erode",
    "Belgaum",
    "Ambattur",
    "Tirunelveli",
    "Malegaon",
    "Gaya",
    "Jalgaon",
    "Udaipur",
    "Maheshtala",
]

# Alternative spellings and variations
CITY_ALIASES = {
    "New Delhi": "Delhi",
    "Bengaluru": "Bangalore",
    "Madras": "Chennai",
    "Calcutta": "Kolkata",
    "Bombay": "Mumbai",
    "Poona": "Pune",
    "Cawnpore": "Kanpur",
    "Baroda": "Vadodara",
    "Benares": "Varanasi",
    "Allahabad": "Prayagraj",
    "Jullundur": "Jalandhar",
    "Trichy": "Tiruchirappalli",
    "Trivandrum": "Thiruvananthapuram",
    "Cochin": "Kochi",
    "Quilon": "Kollam",
    "Alleppey": "Alappuzha",
    "Cannanore": "Kannur",
    "Palghat": "Palakkad",
    "Trichur": "Thrissur",
    "Tellicherry": "Thalassery",
}

# Logistics keywords
LOGISTICS_KEYWORDS = [
    "freight",
    "cargo",
    "transport",
    "logistics",
    "shipping",
    "trade",
    "route",
    "corridor",
    "movement",
    "haulage",
    "shipment",
    "delivery",
    "supply chain",
    "warehouse",
    "distribution",
    "carrier",
    "transit",
    "consignment",
    "dispatch",
    "logistic",
    "transportation",
]


def connect_to_db():
    """Establish database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("[OK] Successfully connected to PostgreSQL database")
        return conn
    except Exception as e:
        print(f"[ERROR] Failed to connect to database: {e}")
        sys.exit(1)


def get_table_structure(conn, table_name):
    """Get column information for a table"""
    query = """
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = %s
    ORDER BY ordinal_position;
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (table_name,))
        return cur.fetchall()


def analyze_table_for_cities(conn, table_name, text_column):
    """Analyze a table for city mentions and logistics context"""
    print(f"\n--- Analyzing table: {table_name} (column: {text_column}) ---")

    # Query to get text content
    query = f"SELECT {text_column} FROM {table_name} WHERE {text_column} IS NOT NULL;"

    city_mentions = Counter()
    city_pairs = Counter()
    logistics_context_records = []

    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()

        print(f"  Found {len(rows)} records to analyze")

        for row in rows:
            text = str(row[0]) if row[0] else ""
            if not text:
                continue

            # Normalize text
            text_normalized = text.lower()

            # Check for logistics keywords
            has_logistics_context = any(
                keyword in text_normalized for keyword in LOGISTICS_KEYWORDS
            )

            # Find cities in the text
            found_cities = set()
            for city in INDIAN_CITIES:
                # Match whole words only
                pattern = r"\b" + re.escape(city.lower()) + r"\b"
                if re.search(pattern, text_normalized):
                    found_cities.add(city)
                    city_mentions[city] += 1

            # Check for aliases
            for alias, canonical in CITY_ALIASES.items():
                pattern = r"\b" + re.escape(alias.lower()) + r"\b"
                if re.search(pattern, text_normalized):
                    found_cities.add(canonical)
                    city_mentions[canonical] += 1

            # Generate city pairs
            if len(found_cities) >= 2:
                cities_list = sorted(found_cities)
                for i in range(len(cities_list)):
                    for j in range(i + 1, len(cities_list)):
                        pair = (cities_list[i], cities_list[j])
                        city_pairs[pair] += 1

                        # Store records with logistics context
                        if has_logistics_context:
                            logistics_context_records.append(
                                {
                                    "pair": pair,
                                    "text": text[:200],  # First 200 chars
                                }
                            )

    return {
        "city_mentions": city_mentions,
        "city_pairs": city_pairs,
        "logistics_records": logistics_context_records,
        "total_records": len(rows),
    }


def generate_report(web_data_results, pdf_results):
    """Generate comprehensive report"""
    print("\n" + "=" * 80)
    print("CITY PAIRS ANALYSIS REPORT FOR ZIPPY LOGISTICS")
    print("=" * 80)

    # Combine results
    combined_pairs = Counter()
    combined_pairs.update(web_data_results["city_pairs"])
    combined_pairs.update(pdf_results["city_pairs"])

    combined_mentions = Counter()
    combined_mentions.update(web_data_results["city_mentions"])
    combined_mentions.update(pdf_results["city_mentions"])

    print("\n" + "-" * 80)
    print("TOP 15 CITY PAIRS BY CO-OCCURRENCE FREQUENCY")
    print("-" * 80)

    top_pairs = combined_pairs.most_common(15)
    for i, (pair, count) in enumerate(top_pairs, 1):
        print(f"{i:2d}. {pair[0]} <-> {pair[1]}: {count} co-occurrences")

    print("\n" + "-" * 80)
    print("TOP 15 MOST FREQUENTLY MENTIONED CITIES")
    print("-" * 80)

    top_cities = combined_mentions.most_common(15)
    for i, (city, count) in enumerate(top_cities, 1):
        print(f"{i:2d}. {city}: {count} mentions")

    print("\n" + "-" * 80)
    print("SUMMARY STATISTICS")
    print("-" * 80)
    print(f"Raw web data records analyzed: {web_data_results['total_records']}")
    print(f"PDF chunks analyzed: {pdf_results['total_records']}")
    print(f"Total unique city pairs found: {len(combined_pairs)}")
    print(f"Total unique cities mentioned: {len(combined_mentions)}")
    print(f"Total co-occurrences across all pairs: {sum(combined_pairs.values())}")

    return top_pairs, top_cities


def main():
    print("=" * 80)
    print("ZIPPY LOGISTICS - INDIAN CITY PAIRS ANALYSIS")
    print("=" * 80)

    # Connect to database
    conn = connect_to_db()

    # Check if tables exist
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('raw_web_data', 'pdf_chunks');
        """)
        tables = [row[0] for row in cur.fetchall()]
        print(f"\nAvailable tables: {tables}")

    # Analyze raw_web_data
    web_results = {
        "city_pairs": Counter(),
        "city_mentions": Counter(),
        "logistics_records": [],
        "total_records": 0,
    }
    if "raw_web_data" in tables:
        # Get column structure
        columns = get_table_structure(conn, "raw_web_data")
        print(f"\nraw_web_data columns: {[c['column_name'] for c in columns]}")

        # Find text column
        text_column = None
        for col in columns:
            if (
                col["data_type"] in ["text", "character varying"]
                and "content" in col["column_name"].lower()
            ):
                text_column = col["column_name"]
                break

        if text_column:
            web_results = analyze_table_for_cities(conn, "raw_web_data", text_column)
        else:
            # Try common column names
            for col in ["content", "text", "data", "body", "description"]:
                try:
                    web_results = analyze_table_for_cities(conn, "raw_web_data", col)
                    break
                except:
                    continue

    # Analyze pdf_chunks
    pdf_results = {
        "city_pairs": Counter(),
        "city_mentions": Counter(),
        "logistics_records": [],
        "total_records": 0,
    }
    if "pdf_chunks" in tables:
        # Get column structure
        columns = get_table_structure(conn, "pdf_chunks")
        print(f"\npdf_chunks columns: {[c['column_name'] for c in columns]}")

        # Find text column
        text_column = None
        for col in columns:
            if (
                col["data_type"] in ["text", "character varying"]
                and "chunk" in col["column_name"].lower()
            ):
                text_column = col["column_name"]
                break

        if text_column:
            pdf_results = analyze_table_for_cities(conn, "pdf_chunks", text_column)
        else:
            # Try common column names
            for col in ["chunk_text", "text", "content", "data"]:
                try:
                    pdf_results = analyze_table_for_cities(conn, "pdf_chunks", col)
                    break
                except:
                    continue

    # Generate report
    top_pairs, top_cities = generate_report(web_results, pdf_results)

    # Print SQL queries used
    print("\n" + "=" * 80)
    print("SQL QUERIES USED")
    print("=" * 80)

    print("""
-- Query to check table structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'raw_web_data'
ORDER BY ordinal_position;

-- Query to check available tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Sample query for city search (used programmatically)
SELECT content FROM raw_web_data WHERE content IS NOT NULL;
SELECT chunk_text FROM pdf_chunks WHERE chunk_text IS NOT NULL;

-- Query to find records with specific cities and logistics keywords
SELECT * FROM raw_web_data 
WHERE content ~* 'Mumbai|Delhi|Chennai|Kolkata|Bangalore' 
AND content ~* 'freight|cargo|transport|logistics|shipping|trade|route|corridor';
""")

    conn.close()
    print("\n[DONE] Analysis complete. Database connection closed.")


if __name__ == "__main__":
    main()
