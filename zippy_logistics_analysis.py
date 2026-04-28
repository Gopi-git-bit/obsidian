#!/usr/bin/env python3
"""
PostgreSQL Data Pattern Extraction Script for Zippy Logistics
Analyzes pdf_chunks and raw_web_data tables for logistics insights
"""

import psycopg2
import re
import json
from datetime import datetime
from collections import defaultdict

# Database connection parameters
# SECURITY: Use environment variables for credentials. Never hardcode passwords.
import os

DB_URL = os.getenv("DATABASE_URL")

if DB_URL:
    DB_CONFIG = DB_URL
else:
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "database": os.getenv("DB_NAME", "zippy_logistics"),
        "user": os.getenv("DB_USER", "zippy"),
        "password": os.getenv("DB_PASSWORD", ""),  # REQUIRED: set DB_PASSWORD env var
    }


def connect_db():
    """Establish database connection"""
    if isinstance(DB_CONFIG, str):
        return psycopg2.connect(DB_CONFIG)
    return psycopg2.connect(**DB_CONFIG)


def get_table_info(cursor):
    """Get table structure information"""
    # Get pdf_chunks columns
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'pdf_chunks'
        ORDER BY ordinal_position
    """)
    pdf_chunks_cols = cursor.fetchall()

    # Get raw_web_data columns
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'raw_web_data'
        ORDER BY ordinal_position
    """)
    raw_web_data_cols = cursor.fetchall()

    return pdf_chunks_cols, raw_web_data_cols


def get_table_counts(cursor):
    """Get row counts for tables"""
    cursor.execute("SELECT COUNT(*) FROM pdf_chunks")
    pdf_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM raw_web_data")
    web_count = cursor.fetchone()[0]

    return pdf_count, web_count


# =============================================================================
# PATTERN 1: COST/FREIGHT RATE PATTERNS
# =============================================================================


def extract_cost_freight_patterns(cursor):
    """Extract freight rates, transportation costs, logistics costs"""

    # Keywords for cost/freight patterns
    cost_keywords = [
        "freight rate",
        "transportation cost",
        "logistics cost",
        "cost per km",
        "cost per ton",
        "freight cost",
        "shipping cost",
        "trucking cost",
        "cargo rate",
        "transport cost",
        "haulage cost",
        "freight charges",
        "rate per km",
        "rate per ton",
        "price per ton",
        "price per km",
        "INR per ton",
        "INR per km",
        "Rs per ton",
        "Rs per km",
        "ton-km cost",
        "cost of transport",
        "freight pricing",
    ]

    # Query for pdf_chunks
    cursor.execute(f"""
        SELECT id, file_name, chunk_index, chunk_text, extracted_at
        FROM pdf_chunks
        WHERE chunk_text ~* '({"|".join(cost_keywords)})'
        LIMIT 100
    """)
    pdf_results = cursor.fetchall()

    # Query for raw_web_data
    cursor.execute(f"""
        SELECT id, source, url, content, scraped_at
        FROM raw_web_data
        WHERE content ~* '({"|".join(cost_keywords)})'
        LIMIT 100
    """)
    web_results = cursor.fetchall()

    return pdf_results, web_results


def analyze_cost_patterns(pdf_results, web_results):
    """Analyze and structure cost/freight pattern findings"""
    findings = []

    # Mode detection patterns
    modes = [
        "road",
        "rail",
        "air",
        "sea",
        "waterway",
        "inland waterway",
        "highway",
        "expressway",
        "truck",
        "train",
        "vessel",
        "ship",
    ]

    # Cost extraction patterns
    cost_patterns = [
        r"(\d+(?:\.\d+)?)\s*(?:INR|Rs|USD|\$)?\s*(?:per|/)\s*(?:ton|km|tonne|TEU)",
        r"(?:cost|rate|price)\s*(?:of|is|:)?\s*(\d+(?:\.\d+)?)",
        r"(\d+(?:\.\d+)?)\s*(?:INR|Rs|USD|\$)",
    ]

    for row in pdf_results:
        id_, file_name, chunk_index, chunk_text, extracted_at = row
        text_lower = chunk_text.lower()

        # Detect mode
        detected_mode = None
        for mode in modes:
            if mode in text_lower:
                detected_mode = mode
                break

        # Try to extract cost value
        cost_value = None
        for pattern in cost_patterns:
            match = re.search(pattern, chunk_text, re.IGNORECASE)
            if match:
                cost_value = match.group(1)
                break

        # Extract route if mentioned
        route_match = re.search(r"(\w+)\s*(?:to|-)\s*(\w+)", chunk_text)
        route = (
            f"{route_match.group(1)}-{route_match.group(2)}" if route_match else None
        )

        findings.append(
            {
                "source_type": "PDF",
                "source": file_name,
                "chunk_index": chunk_index,
                "date": extracted_at,
                "mode": detected_mode,
                "cost_value": cost_value,
                "route": route,
                "text_snippet": chunk_text[:300] + "..."
                if len(chunk_text) > 300
                else chunk_text,
            }
        )

    for row in web_results:
        id_, source, url, content, scraped_at = row
        content_lower = content.lower()

        # Detect mode
        detected_mode = None
        for mode in modes:
            if mode in content_lower:
                detected_mode = mode
                break

        # Try to extract cost value
        cost_value = None
        for pattern in cost_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                cost_value = match.group(1)
                break

        findings.append(
            {
                "source_type": "Web",
                "source": url,
                "title": source,
                "date": scraped_at,
                "mode": detected_mode,
                "cost_value": cost_value,
                "text_snippet": content[:300] + "..."
                if len(content) > 300
                else content,
            }
        )

    return findings


# =============================================================================
# PATTERN 2: INFRASTRUCTURE & BOTTLENECK PATTERNS
# =============================================================================


def extract_infrastructure_patterns(cursor):
    """Extract infrastructure issues, congestion, delays, capacity constraints"""

    bottleneck_keywords = [
        "bottleneck",
        "congestion",
        "delay",
        "capacity constraint",
        "infrastructure gap",
        "capacity shortage",
        "traffic congestion",
        "port congestion",
        "terminal congestion",
        "infrastructure deficit",
        "inadequate infrastructure",
        "poor connectivity",
        "last mile",
        "insufficient capacity",
        "overloaded",
        "underdeveloped",
        "poor condition",
        "dilapidated",
        "congested corridor",
    ]

    # Query for pdf_chunks
    cursor.execute(f"""
        SELECT id, file_name, chunk_index, chunk_text, extracted_at
        FROM pdf_chunks
        WHERE chunk_text ~* '({"|".join(bottleneck_keywords)})'
        LIMIT 100
    """)
    pdf_results = cursor.fetchall()

    # Query for raw_web_data
    cursor.execute(f"""
        SELECT id, source, url, content, scraped_at
        FROM raw_web_data
        WHERE content ~* '({"|".join(bottleneck_keywords)})'
        LIMIT 100
    """)
    web_results = cursor.fetchall()

    return pdf_results, web_results


def analyze_infrastructure_patterns(pdf_results, web_results):
    """Analyze infrastructure and bottleneck findings"""
    findings = []

    # Location patterns
    location_patterns = [
        r"(\w+(?:\s\w+)?)\s+(?:port|station|terminal|hub|corridor|highway|route|city|state)",
        r"(?:at|near|in|on)\s+([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?)",
    ]

    # Severity indicators
    severity_keywords = [
        "severe",
        "critical",
        "major",
        "minor",
        "moderate",
        "significant",
    ]

    for row in pdf_results:
        id_, file_name, chunk_index, chunk_text, extracted_at = row
        text_lower = chunk_text.lower()

        # Extract location
        location = None
        for pattern in location_patterns:
            match = re.search(pattern, chunk_text)
            if match:
                location = match.group(1)
                break

        # Determine issue type
        issue_type = None
        if "bottleneck" in text_lower:
            issue_type = "Bottleneck"
        elif "congestion" in text_lower:
            issue_type = "Congestion"
        elif "delay" in text_lower:
            issue_type = "Delay"
        elif "capacity" in text_lower:
            issue_type = "Capacity Constraint"
        elif "infrastructure" in text_lower:
            issue_type = "Infrastructure Gap"

        # Determine severity
        severity = "Unknown"
        for sev in severity_keywords:
            if sev in text_lower:
                severity = sev.capitalize()
                break

        findings.append(
            {
                "source_type": "PDF",
                "source": file_name,
                "chunk_index": chunk_index,
                "date": extracted_at,
                "location": location,
                "issue_type": issue_type,
                "severity": severity,
                "text_snippet": chunk_text[:300] + "..."
                if len(chunk_text) > 300
                else chunk_text,
            }
        )

    for row in web_results:
        id_, source, url, content, scraped_at = row
        content_lower = content.lower()

        # Extract location
        location = None
        for pattern in location_patterns:
            match = re.search(pattern, content)
            if match:
                location = match.group(1)
                break

        # Determine issue type
        issue_type = None
        if "bottleneck" in content_lower:
            issue_type = "Bottleneck"
        elif "congestion" in content_lower:
            issue_type = "Congestion"
        elif "delay" in content_lower:
            issue_type = "Delay"
        elif "capacity" in content_lower:
            issue_type = "Capacity Constraint"
        elif "infrastructure" in content_lower:
            issue_type = "Infrastructure Gap"

        # Determine severity
        severity = "Unknown"
        for sev in severity_keywords:
            if sev in content_lower:
                severity = sev.capitalize()
                break

        findings.append(
            {
                "source_type": "Web",
                "source": url,
                "title": source,
                "date": scraped_at,
                "location": location,
                "issue_type": issue_type,
                "severity": severity,
                "text_snippet": content[:300] + "..."
                if len(content) > 300
                else content,
            }
        )

    return findings


# =============================================================================
# PATTERN 3: GOVERNMENT POLICY & INITIATIVE PATTERNS
# =============================================================================


def extract_policy_patterns(cursor):
    """Extract government schemes, policies, investments"""

    policy_keywords = [
        "PM Gati Shakti",
        "Bharatmala",
        "Sagarmala",
        "National Logistics Policy",
        "Make in India",
        "infrastructure scheme",
        "government scheme",
        "policy initiative",
        "investment plan",
        "economic corridor",
        "dedicated freight corridor",
        "DFC",
        "Expressway",
        "National Highway",
        "logistics policy",
        "transport policy",
        "infrastructure investment",
        "public investment",
        "government investment",
        "billion investment",
        "crore investment",
        "INR investment",
        "USD investment",
    ]

    # Query for pdf_chunks
    cursor.execute(f"""
        SELECT id, file_name, chunk_index, chunk_text, extracted_at
        FROM pdf_chunks
        WHERE chunk_text ~* '({"|".join(policy_keywords)})'
        LIMIT 100
    """)
    pdf_results = cursor.fetchall()

    # Query for raw_web_data
    cursor.execute(f"""
        SELECT id, source, url, content, scraped_at
        FROM raw_web_data
        WHERE content ~* '({"|".join(policy_keywords)})'
        LIMIT 100
    """)
    web_results = cursor.fetchall()

    return pdf_results, web_results


def analyze_policy_patterns(pdf_results, web_results):
    """Analyze government policy and initiative findings"""
    findings = []

    # Known schemes
    schemes = {
        "PM Gati Shakti": ["Gati Shakti", "PMGS"],
        "Bharatmala": ["Bharatmala", "Bharat Mala"],
        "Sagarmala": ["Sagarmala", "Sagar Mala"],
        "National Logistics Policy": ["National Logistics Policy", "NLP"],
        "Dedicated Freight Corridor": ["Dedicated Freight Corridor", "DFC"],
        "Make in India": ["Make in India"],
    }

    # Investment extraction patterns
    investment_patterns = [
        r"(\d+(?:\.\d+)?)\s*(?:billion|bn|B)\s*(?:USD|INR|\$)?",
        r"(\d+(?:\.\d+)?)\s*(?:crore|lakh|million)\s*(?:INR|Rs)?",
        r"INR\s*(\d+(?:\.\d+)?)\s*(?:crore|billion)",
    ]

    for row in pdf_results:
        id_, file_name, chunk_index, chunk_text, extracted_at = row
        text_lower = chunk_text.lower()

        # Detect scheme
        detected_scheme = None
        for scheme, keywords in schemes.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    detected_scheme = scheme
                    break
            if detected_scheme:
                break

        # Extract investment amount
        investment = None
        for pattern in investment_patterns:
            match = re.search(pattern, chunk_text, re.IGNORECASE)
            if match:
                investment = match.group(0)
                break

        # Extract coverage/area
        coverage_match = re.search(
            r"(?:cover|span|across|connect|link|network).*?(\d+(?:,\d+)*)\s*(?:km|kilometers?|states?|cities?|districts?)",
            chunk_text,
            re.IGNORECASE,
        )
        coverage = coverage_match.group(0) if coverage_match else None

        findings.append(
            {
                "source_type": "PDF",
                "source": file_name,
                "chunk_index": chunk_index,
                "date": extracted_at,
                "scheme_name": detected_scheme,
                "investment_amount": investment,
                "coverage_area": coverage,
                "text_snippet": chunk_text[:300] + "..."
                if len(chunk_text) > 300
                else chunk_text,
            }
        )

    for row in web_results:
        id_, source, url, content, scraped_at = row
        content_lower = content.lower()

        # Detect scheme
        detected_scheme = None
        for scheme, keywords in schemes.items():
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    detected_scheme = scheme
                    break
            if detected_scheme:
                break

        # Extract investment amount
        investment = None
        for pattern in investment_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                investment = match.group(0)
                break

        # Extract coverage/area
        coverage_match = re.search(
            r"(?:cover|span|across|connect|link|network).*?(\d+(?:,\d+)*)\s*(?:km|kilometers?|states?|cities?|districts?)",
            content,
            re.IGNORECASE,
        )
        coverage = coverage_match.group(0) if coverage_match else None

        findings.append(
            {
                "source_type": "Web",
                "source": url,
                "title": source,
                "date": scraped_at,
                "scheme_name": detected_scheme,
                "investment_amount": investment,
                "coverage_area": coverage,
                "text_snippet": content[:300] + "..."
                if len(content) > 300
                else content,
            }
        )

    return findings


# =============================================================================
# PATTERN 4: MODAL SPLIT DATA
# =============================================================================


def extract_modal_split_patterns(cursor):
    """Extract transportation mode statistics"""

    modal_keywords = [
        "modal share",
        "modal split",
        "transport share",
        "mode share",
        "percentage road",
        "percentage rail",
        "percentage air",
        "percentage water",
        "road transport",
        "rail transport",
        "air cargo",
        "water transport",
        "inland waterway",
        "road freight",
        "rail freight",
        "air freight",
    ]

    # Query for pdf_chunks
    cursor.execute(f"""
        SELECT id, file_name, chunk_index, chunk_text, extracted_at
        FROM pdf_chunks
        WHERE chunk_text ~* '({"|".join(modal_keywords)})'
        LIMIT 100
    """)
    pdf_results = cursor.fetchall()

    # Query for raw_web_data
    cursor.execute(f"""
        SELECT id, source, url, content, scraped_at
        FROM raw_web_data
        WHERE content ~* '({"|".join(modal_keywords)})'
        LIMIT 100
    """)
    web_results = cursor.fetchall()

    return pdf_results, web_results


def analyze_modal_split_patterns(pdf_results, web_results):
    """Analyze modal split data findings"""
    findings = []

    # Percentage extraction patterns
    percentage_patterns = [
        r"(\d+(?:\.\d+)?)%",
        r"(\d+(?:\.\d+)?)\s*percent",
        r"(\d+(?:\.\d+)?)\s*per\s*cent",
    ]

    # Mode detection
    modes = ["road", "rail", "air", "water", "waterway", "sea", "inland waterway"]

    for row in pdf_results:
        id_, file_name, chunk_index, chunk_text, extracted_at = row
        text_lower = chunk_text.lower()

        # Detect mode mentioned
        detected_mode = None
        for mode in modes:
            if mode in text_lower:
                detected_mode = mode
                break

        # Extract percentage
        percentage = None
        for pattern in percentage_patterns:
            match = re.search(pattern, chunk_text, re.IGNORECASE)
            if match:
                percentage = match.group(1)
                break

        # Detect trend
        trend = "Unknown"
        if (
            "increase" in text_lower
            or "growing" in text_lower
            or "rising" in text_lower
        ):
            trend = "Increasing"
        elif (
            "decrease" in text_lower
            or "declining" in text_lower
            or "falling" in text_lower
        ):
            trend = "Decreasing"
        elif "stable" in text_lower or "constant" in text_lower:
            trend = "Stable"

        findings.append(
            {
                "source_type": "PDF",
                "source": file_name,
                "chunk_index": chunk_index,
                "date": extracted_at,
                "mode": detected_mode,
                "percentage": percentage,
                "trend": trend,
                "text_snippet": chunk_text[:300] + "..."
                if len(chunk_text) > 300
                else chunk_text,
            }
        )

    for row in web_results:
        id_, source, url, content, scraped_at = row
        content_lower = content.lower()

        # Detect mode mentioned
        detected_mode = None
        for mode in modes:
            if mode in content_lower:
                detected_mode = mode
                break

        # Extract percentage
        percentage = None
        for pattern in percentage_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                percentage = match.group(1)
                break

        # Detect trend
        trend = "Unknown"
        if (
            "increase" in content_lower
            or "growing" in content_lower
            or "rising" in content_lower
        ):
            trend = "Increasing"
        elif (
            "decrease" in content_lower
            or "declining" in content_lower
            or "falling" in content_lower
        ):
            trend = "Decreasing"
        elif "stable" in content_lower or "constant" in content_lower:
            trend = "Stable"

        findings.append(
            {
                "source_type": "Web",
                "source": url,
                "title": source,
                "date": scraped_at,
                "mode": detected_mode,
                "percentage": percentage,
                "trend": trend,
                "text_snippet": content[:300] + "..."
                if len(content) > 300
                else content,
            }
        )

    return findings


# =============================================================================
# PATTERN 5: GROWTH & TREND PATTERNS
# =============================================================================


def extract_growth_patterns(cursor):
    """Extract CAGR, growth rates, future projections"""

    growth_keywords = [
        "CAGR",
        "growth rate",
        "annual growth",
        "projection",
        "forecast",
        "2025",
        "2030",
        "2035",
        "by 2025",
        "by 2030",
        "expected growth",
        "projected growth",
        "estimated growth",
        "future growth",
        "compound annual growth",
        "year over year",
        "YoY growth",
        "market growth",
        "sector growth",
        "industry growth",
    ]

    # Query for pdf_chunks
    cursor.execute(f"""
        SELECT id, file_name, chunk_index, chunk_text, extracted_at
        FROM pdf_chunks
        WHERE chunk_text ~* '({"|".join(growth_keywords)})'
        LIMIT 100
    """)
    pdf_results = cursor.fetchall()

    # Query for raw_web_data
    cursor.execute(f"""
        SELECT id, source, url, content, scraped_at
        FROM raw_web_data
        WHERE content ~* '({"|".join(growth_keywords)})'
        LIMIT 100
    """)
    web_results = cursor.fetchall()

    return pdf_results, web_results


def analyze_growth_patterns(pdf_results, web_results):
    """Analyze growth and trend findings"""
    findings = []

    # Growth rate extraction patterns
    growth_patterns = [
        r"CAGR\s*(?:of|:)?\s*(\d+(?:\.\d+)?)%",
        r"(\d+(?:\.\d+)?)%\s*(?:CAGR|annual growth)",
        r"growth\s*(?:rate|of|:)?\s*(\d+(?:\.\d+)?)%",
        r"(\d+(?:\.\d+)?)%\s*growth",
    ]

    # Year extraction
    year_patterns = [
        r"20(?:2[5-9]|3[0-9])",
        r"by\s*(20(?:2[5-9]|3[0-9]))",
        r"(?:to|until|till)\s*(20(?:2[5-9]|3[0-9]))",
    ]

    for row in pdf_results:
        id_, file_name, chunk_index, chunk_text, extracted_at = row
        text_lower = chunk_text.lower()

        # Extract growth rate
        growth_rate = None
        for pattern in growth_patterns:
            match = re.search(pattern, chunk_text, re.IGNORECASE)
            if match:
                growth_rate = match.group(1) + "%"
                break

        # Extract timeframe
        timeframe = None
        for pattern in year_patterns:
            match = re.search(pattern, chunk_text, re.IGNORECASE)
            if match:
                timeframe = match.group(0)
                break

        # Determine metric type
        metric = "General Growth"
        if "logistics" in text_lower:
            metric = "Logistics Sector Growth"
        elif "transport" in text_lower:
            metric = "Transport Sector Growth"
        elif "freight" in text_lower:
            metric = "Freight Growth"
        elif "cargo" in text_lower:
            metric = "Cargo Growth"
        elif "market" in text_lower:
            metric = "Market Growth"

        findings.append(
            {
                "source_type": "PDF",
                "source": file_name,
                "chunk_index": chunk_index,
                "date": extracted_at,
                "metric": metric,
                "growth_rate": growth_rate,
                "timeframe": timeframe,
                "text_snippet": chunk_text[:300] + "..."
                if len(chunk_text) > 300
                else chunk_text,
            }
        )

    for row in web_results:
        id_, source, url, content, scraped_at = row
        content_lower = content.lower()

        # Extract growth rate
        growth_rate = None
        for pattern in growth_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                growth_rate = match.group(1) + "%"
                break

        # Extract timeframe
        timeframe = None
        for pattern in year_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                timeframe = match.group(0)
                break

        # Determine metric type
        metric = "General Growth"
        if "logistics" in content_lower:
            metric = "Logistics Sector Growth"
        elif "transport" in content_lower:
            metric = "Transport Sector Growth"
        elif "freight" in content_lower:
            metric = "Freight Growth"
        elif "cargo" in content_lower:
            metric = "Cargo Growth"
        elif "market" in content_lower:
            metric = "Market Growth"

        findings.append(
            {
                "source_type": "Web",
                "source": url,
                "title": source,
                "date": scraped_at,
                "metric": metric,
                "growth_rate": growth_rate,
                "timeframe": timeframe,
                "text_snippet": content[:300] + "..."
                if len(content) > 300
                else content,
            }
        )

    return findings


def generate_sql_queries():
    """Generate SQL queries for reference"""
    queries = {
        "cost_freight": """
-- Cost/Freight Rate Patterns
SELECT id, file_name, chunk_index, chunk_text, extracted_at
FROM pdf_chunks
WHERE chunk_text ~* '(freight rate|transportation cost|logistics cost|cost per km|cost per ton|freight cost|shipping cost|trucking cost|cargo rate|transport cost|haulage cost|freight charges|rate per km|rate per ton|price per ton|price per km|INR per ton|INR per km|Rs per ton|Rs per km|ton-km cost|cost of transport|freight pricing)'
LIMIT 100;

SELECT id, source, url, content, scraped_at
FROM raw_web_data
WHERE content ~* '(freight rate|transportation cost|logistics cost|cost per km|cost per ton|freight cost|shipping cost|trucking cost|cargo rate|transport cost|haulage cost|freight charges|rate per km|rate per ton|price per ton|price per km|INR per ton|INR per km|Rs per ton|Rs per km|ton-km cost|cost of transport|freight pricing)'
LIMIT 100;
        """,
        "infrastructure": """
-- Infrastructure & Bottleneck Patterns
SELECT id, file_name, chunk_index, chunk_text, extracted_at
FROM pdf_chunks
WHERE chunk_text ~* '(bottleneck|congestion|delay|capacity constraint|infrastructure gap|capacity shortage|traffic congestion|port congestion|terminal congestion|infrastructure deficit|inadequate infrastructure|poor connectivity|last mile|insufficient capacity|overloaded|underdeveloped|poor condition|dilapidated|congested corridor)'
LIMIT 100;

SELECT id, source, url, content, scraped_at
FROM raw_web_data
WHERE content ~* '(bottleneck|congestion|delay|capacity constraint|infrastructure gap|capacity shortage|traffic congestion|port congestion|terminal congestion|infrastructure deficit|inadequate infrastructure|poor connectivity|last mile|insufficient capacity|overloaded|underdeveloped|poor condition|dilapidated|congested corridor)'
LIMIT 100;
        """,
        "policy": """
-- Government Policy & Initiative Patterns
SELECT id, file_name, chunk_index, chunk_text, extracted_at
FROM pdf_chunks
WHERE chunk_text ~* '(PM Gati Shakti|Bharatmala|Sagarmala|National Logistics Policy|Make in India|infrastructure scheme|government scheme|policy initiative|investment plan|economic corridor|dedicated freight corridor|DFC|Expressway|National Highway|logistics policy|transport policy|infrastructure investment|public investment|government investment|billion investment|crore investment|INR investment|USD investment)'
LIMIT 100;

SELECT id, source, url, content, scraped_at
FROM raw_web_data
WHERE content ~* '(PM Gati Shakti|Bharatmala|Sagarmala|National Logistics Policy|Make in India|infrastructure scheme|government scheme|policy initiative|investment plan|economic corridor|dedicated freight corridor|DFC|Expressway|National Highway|logistics policy|transport policy|infrastructure investment|public investment|government investment|billion investment|crore investment|INR investment|USD investment)'
LIMIT 100;
        """,
        "modal_split": """
-- Modal Split Data
SELECT id, file_name, chunk_index, chunk_text, extracted_at
FROM pdf_chunks
WHERE chunk_text ~* '(modal share|modal split|transport share|mode share|percentage road|percentage rail|percentage air|percentage water|road transport|rail transport|air cargo|water transport|inland waterway|road freight|rail freight|air freight)'
LIMIT 100;

SELECT id, source, url, content, scraped_at
FROM raw_web_data
WHERE content ~* '(modal share|modal split|transport share|mode share|percentage road|percentage rail|percentage air|percentage water|road transport|rail transport|air cargo|water transport|inland waterway|road freight|rail freight|air freight)'
LIMIT 100;
        """,
        "growth": """
-- Growth & Trend Patterns
SELECT id, file_name, chunk_index, chunk_text, extracted_at
FROM pdf_chunks
WHERE chunk_text ~* '(CAGR|growth rate|annual growth|projection|forecast|2025|2030|2035|by 2025|by 2030|expected growth|projected growth|estimated growth|future growth|compound annual growth|year over year|YoY growth|market growth|sector growth|industry growth)'
LIMIT 100;

SELECT id, source, url, content, scraped_at
FROM raw_web_data
WHERE content ~* '(CAGR|growth rate|annual growth|projection|forecast|2025|2030|2035|by 2025|by 2030|expected growth|projected growth|estimated growth|future growth|compound annual growth|year over year|YoY growth|market growth|sector growth|industry growth)'
LIMIT 100;
        """,
    }
    return queries


def generate_report(
    cost_findings,
    infra_findings,
    policy_findings,
    modal_findings,
    growth_findings,
    table_info,
    counts,
):
    """Generate comprehensive report"""

    pdf_cols, web_cols = table_info
    pdf_count, web_count = counts

    report = f"""
================================================================================
ZIPPY LOGISTICS DATABASE ANALYSIS REPORT
================================================================================

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Database: zippy_logistics
Host: localhost:5432

================================================================================
DATABASE OVERVIEW
================================================================================

Tables Analyzed:
- pdf_chunks: {pdf_count} rows
  Columns: {", ".join([col[0] for col in pdf_cols])}

- raw_web_data: {web_count} rows
  Columns: {", ".join([col[0] for col in web_cols])}

================================================================================
PATTERN 1: COST/FREIGHT RATE PATTERNS
================================================================================

Total Findings: {len(cost_findings)}

Breakdown by Mode:
"""

    mode_counts = defaultdict(int)
    for f in cost_findings:
        mode = f.get("mode") or "Unknown"
        mode_counts[mode] += 1

    for mode, count in sorted(mode_counts.items(), key=lambda x: x[1], reverse=True)[
        :10
    ]:
        report += f"  - {mode}: {count} mentions\n"

    report += f"""
Key Findings (Top 5):
"""

    for i, f in enumerate(cost_findings[:5], 1):
        source_str = str(f["source"])[:50] if f["source"] else "N/A"
        report += f"""
  {i}. Source: {source_str}...
     Mode: {f.get("mode", "N/A")}
     Cost: {f.get("cost_value", "N/A")}
     Route: {f.get("route", "N/A")}
     Date: {f.get("date")}
"""

    report += f"""
================================================================================
PATTERN 2: INFRASTRUCTURE & BOTTLENECK PATTERNS
================================================================================

Total Findings: {len(infra_findings)}

Breakdown by Issue Type:
"""

    issue_counts = defaultdict(int)
    for f in infra_findings:
        issue = f.get("issue_type") or "Unknown"
        issue_counts[issue] += 1

    for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[
        :10
    ]:
        report += f"  - {issue}: {count} mentions\n"

    report += f"""
Breakdown by Severity:
"""

    severity_counts = defaultdict(int)
    for f in infra_findings:
        sev = f.get("severity") or "Unknown"
        severity_counts[sev] += 1

    for sev, count in sorted(severity_counts.items(), key=lambda x: x[1], reverse=True):
        report += f"  - {sev}: {count}\n"

    report += f"""
Key Findings (Top 5):
"""

    for i, f in enumerate(infra_findings[:5], 1):
        source_str = str(f["source"])[:50] if f["source"] else "N/A"
        report += f"""
  {i}. Source: {source_str}...
     Location: {f.get("location", "N/A")}
     Issue: {f.get("issue_type", "N/A")}
     Severity: {f.get("severity", "N/A")}
"""

    report += f"""
================================================================================
PATTERN 3: GOVERNMENT POLICY & INITIATIVE PATTERNS
================================================================================

Total Findings: {len(policy_findings)}

Breakdown by Scheme:
"""

    scheme_counts = defaultdict(int)
    for f in policy_findings:
        scheme = f.get("scheme_name") or "Other/Unidentified"
        scheme_counts[scheme] += 1

    for scheme, count in sorted(
        scheme_counts.items(), key=lambda x: x[1], reverse=True
    )[:10]:
        report += f"  - {scheme}: {count} mentions\n"

    report += f"""
Key Findings (Top 5):
"""

    for i, f in enumerate(policy_findings[:5], 1):
        source_str = str(f["source"])[:50] if f["source"] else "N/A"
        report += f"""
  {i}. Source: {source_str}...
     Scheme: {f.get("scheme_name", "N/A")}
     Investment: {f.get("investment_amount", "N/A")}
     Coverage: {f.get("coverage_area", "N/A")}
"""

    report += f"""
================================================================================
PATTERN 4: MODAL SPLIT DATA
================================================================================

Total Findings: {len(modal_findings)}

Breakdown by Mode:
"""

    modal_mode_counts = defaultdict(int)
    for f in modal_findings:
        mode = f.get("mode") or "Unknown"
        modal_mode_counts[mode] += 1

    for mode, count in sorted(
        modal_mode_counts.items(), key=lambda x: x[1], reverse=True
    )[:10]:
        report += f"  - {mode}: {count} mentions\n"

    report += f"""
Breakdown by Trend:
"""

    trend_counts = defaultdict(int)
    for f in modal_findings:
        trend = f.get("trend") or "Unknown"
        trend_counts[trend] += 1

    for trend, count in sorted(trend_counts.items(), key=lambda x: x[1], reverse=True):
        report += f"  - {trend}: {count}\n"

    report += f"""
Key Findings (Top 5):
"""

    for i, f in enumerate(modal_findings[:5], 1):
        source_str = str(f["source"])[:50] if f["source"] else "N/A"
        report += f"""
  {i}. Source: {source_str}...
     Mode: {f.get("mode", "N/A")}
     Percentage: {f.get("percentage", "N/A")}%
     Trend: {f.get("trend", "N/A")}
"""

    report += f"""
================================================================================
PATTERN 5: GROWTH & TREND PATTERNS
================================================================================

Total Findings: {len(growth_findings)}

Breakdown by Metric Type:
"""

    metric_counts = defaultdict(int)
    for f in growth_findings:
        metric = f.get("metric") or "Unknown"
        metric_counts[metric] += 1

    for metric, count in sorted(
        metric_counts.items(), key=lambda x: x[1], reverse=True
    )[:10]:
        report += f"  - {metric}: {count} mentions\n"

    report += f"""
Key Findings (Top 5):
"""

    for i, f in enumerate(growth_findings[:5], 1):
        source_str = str(f["source"])[:50] if f["source"] else "N/A"
        report += f"""
  {i}. Source: {source_str}...
     Metric: {f.get("metric", "N/A")}
     Growth Rate: {f.get("growth_rate", "N/A")}
     Timeframe: {f.get("timeframe", "N/A")}
"""

    # Key Insights Section
    report += f"""
================================================================================
KEY INSIGHTS FOR ZIPPY LOGISTICS
================================================================================

1. COST OPTIMIZATION OPPORTUNITIES:
   - {mode_counts.get("road", 0)} road transport cost mentions
   - {mode_counts.get("rail", 0)} rail transport cost mentions
   - {mode_counts.get("air", 0)} air transport cost mentions
   - Consider multi-modal strategies for cost optimization

2. INFRASTRUCTURE CHALLENGES:
   - {issue_counts.get("Congestion", 0)} congestion-related issues identified
   - {issue_counts.get("Bottleneck", 0)} bottlenecks detected
   - {issue_counts.get("Capacity Constraint", 0)} capacity constraints noted
   - Plan alternative routes avoiding identified bottlenecks

3. GOVERNMENT INITIATIVES TO LEVERAGE:
   - {scheme_counts.get("PM Gati Shakti", 0)} PM Gati Shakti references
   - {scheme_counts.get("Bharatmala", 0)} Bharatmala references
   - {scheme_counts.get("National Logistics Policy", 0)} NLP references
   - Align operations with government corridors for efficiency

4. MODAL SHIFT TRENDS:
   - {modal_mode_counts.get("road", 0)} road transport mentions
   - {modal_mode_counts.get("rail", 0)} rail transport mentions
   - {trend_counts.get("Increasing", 0)} growth trends identified
   - Monitor modal shift opportunities

5. GROWTH PROJECTIONS:
   - {len(growth_findings)} growth metrics identified
   - {metric_counts.get("Logistics Sector Growth", 0)} logistics growth projections
   - Plan capacity for projected 2025-2030 growth

================================================================================
RECOMMENDATIONS FOR ZIPPY LOGISTICS
================================================================================

1. ROUTE OPTIMIZATION:
   - Use identified cost data to benchmark freight rates
   - Avoid routes with known congestion/bottlenecks
   - Consider rail for bulk cargo where cost-effective

2. STRATEGIC PLANNING:
   - Align with PM Gati Shakti corridors
   - Monitor Bharatmala project developments
   - Prepare for NLP implementation benefits

3. CAPACITY PLANNING:
   - Plan for {metric_counts.get("Logistics Sector Growth", 0)} logistics growth trends
   - Consider infrastructure gaps in expansion planning
   - Monitor modal split shifts for fleet planning

4. COST MANAGEMENT:
   - Benchmark against extracted freight rates
   - Explore multi-modal combinations
   - Leverage government initiatives for cost reduction

================================================================================
END OF REPORT
================================================================================
"""

    return report


def main():
    """Main execution function"""
    print("=" * 80)
    print("ZIPPY LOGISTICS DATABASE ANALYSIS")
    print("=" * 80)
    print("\nConnecting to database...")

    try:
        conn = connect_db()
        cursor = conn.cursor()
        print("Connected successfully\n")

        # Get table information
        print("Fetching table structure...")
        table_info = get_table_info(cursor)
        counts = get_table_counts(cursor)
        print(f">> Found {counts[0]} rows in pdf_chunks")
        print(f">> Found {counts[1]} rows in raw_web_data\n")

        # Pattern 1: Cost/Freight
        print("Analyzing Pattern 1: Cost/Freight Rates...")
        pdf_cost, web_cost = extract_cost_freight_patterns(cursor)
        cost_findings = analyze_cost_patterns(pdf_cost, web_cost)
        print(f">> Found {len(cost_findings)} cost/freight pattern matches\n")

        # Pattern 2: Infrastructure
        print("Analyzing Pattern 2: Infrastructure & Bottlenecks...")
        pdf_infra, web_infra = extract_infrastructure_patterns(cursor)
        infra_findings = analyze_infrastructure_patterns(pdf_infra, web_infra)
        print(f">> Found {len(infra_findings)} infrastructure pattern matches\n")

        # Pattern 3: Policy
        print("Analyzing Pattern 3: Government Policies...")
        pdf_policy, web_policy = extract_policy_patterns(cursor)
        policy_findings = analyze_policy_patterns(pdf_policy, web_policy)
        print(f">> Found {len(policy_findings)} policy pattern matches\n")

        # Pattern 4: Modal Split
        print("Analyzing Pattern 4: Modal Split Data...")
        pdf_modal, web_modal = extract_modal_split_patterns(cursor)
        modal_findings = analyze_modal_split_patterns(pdf_modal, web_modal)
        print(f">> Found {len(modal_findings)} modal split pattern matches\n")

        # Pattern 5: Growth
        print("Analyzing Pattern 5: Growth & Trends...")
        pdf_growth, web_growth = extract_growth_patterns(cursor)
        growth_findings = analyze_growth_patterns(pdf_growth, web_growth)
        print(f">> Found {len(growth_findings)} growth pattern matches\n")

        # Generate report
        print("Generating comprehensive report...")
        report = generate_report(
            cost_findings,
            infra_findings,
            policy_findings,
            modal_findings,
            growth_findings,
            table_info,
            counts,
        )

        # Save SQL queries
        sql_queries = generate_sql_queries()

        cursor.close()
        conn.close()
        print(">> Database connection closed\n")

        return {
            "report": report,
            "sql_queries": sql_queries,
            "findings": {
                "cost_freight": cost_findings,
                "infrastructure": infra_findings,
                "policy": policy_findings,
                "modal_split": modal_findings,
                "growth": growth_findings,
            },
        }

    except Exception as e:
        print(f"XX Error: {str(e)}")
        raise


if __name__ == "__main__":
    results = main()

    # Save report to file
    with open("zippy_analysis_report.txt", "w", encoding="utf-8") as f:
        f.write(results["report"])
    print("Report saved to: zippy_analysis_report.txt")

    # Save SQL queries to file
    with open("zippy_analysis_queries.sql", "w", encoding="utf-8") as f:
        for pattern, query in results["sql_queries"].items():
            f.write(f"\n{'=' * 80}\n")
            f.write(f"-- PATTERN: {pattern.upper()}\n")
            f.write(f"{'=' * 80}\n")
            f.write(query)
            f.write("\n")
    print("SQL queries saved to: zippy_analysis_queries.sql")

    # Save findings to JSON
    with open("zippy_analysis_findings.json", "w", encoding="utf-8") as f:
        # Convert findings to serializable format
        json_findings = {}
        for key, findings in results["findings"].items():
            json_findings[key] = [
                {k: str(v) if v is not None else None for k, v in finding.items()}
                for finding in findings
            ]
        json.dump(json_findings, f, indent=2, ensure_ascii=False)
    print("Findings saved to: zippy_analysis_findings.json")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

    # Print the report
    print(results["report"])
