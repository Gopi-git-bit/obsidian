# Indian City Pairs Logistics Analysis Report
## Zippy Logistics Database - PostgreSQL Analysis

**Database:** zippy_logistics  
**Host:** localhost:5432  
**Analysis Date:** 2026-04-05  

---

## Executive Summary

Analysis of `raw_web_data` and `pdf_chunks` tables revealed **405 unique city pairs** with **1,461 total co-occurrences** across 53 distinct Indian cities. The analysis focused on content containing logistics keywords such as freight, cargo, transport, logistics, shipping, trade, route, corridor, and movement.

### Data Sources
- **raw_web_data**: 3 records (web scraping from FreightWaves, JOC, SupplyChainDive)
- **pdf_chunks**: 1,811 chunks from 5 PDF documents:
  - HVT059_Final-Report_.pdf (440 chunks)
  - GP-IN1 UT.pdf (322 chunks)
  - FreightReportNationalLevel.pdf (282 chunks)
  - Industry-Report-on-Logistics-in-India (255 chunks)
  - DTEE_TNA_India_en.pdf (201 chunks)

- **Records with logistics context**: 1,405 records (77.5% of total)

---

## Top 15 City Pairs by Co-occurrence Frequency

| Rank | City Pair | Co-occurrences | Significance |
|------|-----------|----------------|--------------|
| 1 | **Delhi <-> Mumbai** | 52 | National capital ↔ Financial capital. Major freight corridor |
| 2 | **Ahmedabad <-> Delhi** | 42 | Gujarat industrial hub ↔ National capital. Key trade route |
| 3 | **Kolkata <-> Mumbai** | 32 | Eastern port ↔ Western port. Historic trade corridor |
| 4 | **Bangalore <-> Delhi** | 31 | Tech hub ↔ Capital. Electronics & IT logistics |
| 5 | **Chennai <-> Delhi** | 31 | Southern manufacturing ↔ Northern distribution |
| 6 | **Chennai <-> Mumbai** | 29 | Major port cities. Coastal freight movement |
| 7 | **Delhi <-> Kolkata** | 29 | Eastern freight corridor. Golden Quadrilateral route |
| 8 | **Bangalore <-> Mumbai** | 26 | Tech & manufacturing link. Pune-Mumbai-Bangalore belt |
| 9 | **Delhi <-> Hyderabad** | 26 | Pharma & IT corridor. Emerging logistics route |
| 10 | **Bangalore <-> Hyderabad** | 25 | South Indian tech corridor. Pharma logistics |
| 11 | **Ahmedabad <-> Mumbai** | 24 | Gujarat-Maharashtra trade. Textile & chemical freight |
| 12 | **Chennai <-> Kolkata** | 32 | Coastal corridor. Port-to-port shipping |
| 13 | **Hyderabad <-> Mumbai** | 24 | Deccan plateau route. Bulk commodity transport |
| 14 | **Delhi <-> Pune** | 20 | Auto corridor. Manufacturing belt connection |
| 15 | **Chennai <-> Hyderabad** | 20 | Southern freight route. Manufacturing & pharma |

### Key Observations:
1. **Delhi** appears in 8 of the top 15 pairs - confirming its role as the central logistics hub
2. **Mumbai** appears in 7 of the top 15 pairs - highlighting its importance as a major port and financial center
3. **Ahmedabad-Delhi** pair (#2) is significant - reflecting Gujarat's industrial strength
4. **Bangalore-Hyderabad** pair (#10) represents the emerging South Indian tech/pharma corridor

---

## Top 15 Most Mentioned Cities (Overall)

| Rank | City | Mentions | Key Industries |
|------|------|----------|----------------|
| 1 | **Delhi** | 222 | Distribution, warehousing, e-commerce |
| 2 | **Ahmedabad** | 207 | Textiles, chemicals, pharmaceuticals |
| 3 | **Mumbai** | 95 | Finance, shipping, trade |
| 4 | **Bangalore** | 60 | IT, electronics, aerospace |
| 5 | **Kochi** | 43 | Port city, coastal shipping |
| 6 | **Kolkata** | 41 | Eastern hub, jute, manufacturing |
| 7 | **Chennai** | 40 | Auto, manufacturing, port |
| 8 | **Hyderabad** | 40 | Pharma, IT, pearls |
| 9 | **Pune** | 35 | Auto, manufacturing |
| 10 | **Dharwad** | 23 | Education, logistics hub |
| 11 | **Nanded** | 20 | Sikh pilgrimage, agri-processing |
| 12 | **Jaipur** | 20 | Tourism, gems, textiles |
| 13 | **Rajkot** | 19 | Auto parts, machine tools |
| 14 | **Nagpur** | 18 | Central India logistics hub |
| 15 | **Gurgaon** | 13 | Auto, IT, BPO |

### Notable Findings:
- **Ahmedabad** has unusually high mentions (207), suggesting Gujarat-focused logistics documents
- **Kochi** (43 mentions) is significant - indicates coastal/port logistics content
- **Tier-2 cities** like Dharwad, Nanded, and Rajkot are well-represented, showing diverse coverage

---

## SQL Queries Used

### 1. Database Connection & Structure Analysis
```sql
-- Connect to database
\c zippy_logistics;

-- List tables in public schema
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Get table structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'raw_web_data'
ORDER BY ordinal_position;

SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'pdf_chunks'
ORDER BY ordinal_position;
```

### 2. City Mention Analysis
```sql
-- Search for specific cities in content
SELECT 
    id,
    source,
    LEFT(content, 200) as snippet
FROM raw_web_data 
WHERE content ~* 'Mumbai|Delhi|Chennai|Kolkata|Bangalore';

-- Search pdf_chunks for cities
SELECT 
    id,
    file_name,
    chunk_index,
    LEFT(chunk_text, 200) as snippet
FROM pdf_chunks 
WHERE chunk_text ~* 'Ahmedabad|Pune|Hyderabad|Kochi|Jaipur';
```

### 3. Logistics Context Filtering
```sql
-- Find records with logistics keywords
SELECT 
    file_name,
    chunk_index,
    LEFT(chunk_text, 300) as context
FROM pdf_chunks
WHERE chunk_text ~* 'freight|cargo|transport|logistics|shipping|trade|route|corridor|movement';

-- Count logistics-related records
SELECT 
    'pdf_chunks' as table_name,
    COUNT(*) as logistics_records
FROM pdf_chunks 
WHERE chunk_text ~* 'freight|cargo|transport|logistics|shipping|trade|route|corridor|movement'
UNION ALL
SELECT 
    'raw_web_data' as table_name,
    COUNT(*) as logistics_records
FROM raw_web_data 
WHERE content ~* 'freight|cargo|transport|logistics|shipping|trade|route|corridor|movement';
```

### 4. City Pair Co-occurrence Analysis
```sql
-- Find specific city pair mentions
SELECT 
    file_name,
    chunk_index,
    LEFT(chunk_text, 400) as context
FROM pdf_chunks
WHERE chunk_text ~* 'Delhi.*Mumbai|Mumbai.*Delhi'
AND chunk_text ~* 'logistics|freight|transport|cargo';

-- Count records with multiple cities
SELECT 
    file_name,
    COUNT(*) as multi_city_chunks
FROM pdf_chunks
WHERE (
    (chunk_text ~* 'Delhi' AND chunk_text ~* 'Mumbai')
    OR (chunk_text ~* 'Bangalore' AND chunk_text ~* 'Chennai')
    OR (chunk_text ~* 'Ahmedabad' AND chunk_text ~* 'Kolkata')
)
GROUP BY file_name;
```

### 5. Data Source Analysis
```sql
-- Analyze web data sources
SELECT 
    source,
    COUNT(*) as record_count,
    MIN(scraped_at) as earliest,
    MAX(scraped_at) as latest
FROM raw_web_data 
GROUP BY source;

-- Analyze PDF sources
SELECT 
    file_name,
    COUNT(*) as chunk_count,
    MIN(extracted_at) as earliest,
    MAX(extracted_at) as latest
FROM pdf_chunks 
GROUP BY file_name
ORDER BY chunk_count DESC;
```

### 6. Advanced Pattern Matching Queries
```sql
-- Find city pairs with logistics context (using regex)
WITH city_mentions AS (
    SELECT 
        file_name,
        chunk_index,
        chunk_text,
        CASE WHEN chunk_text ~* '\bDelhi\b' THEN 1 ELSE 0 END as has_delhi,
        CASE WHEN chunk_text ~* '\bMumbai\b' THEN 1 ELSE 0 END as has_mumbai,
        CASE WHEN chunk_text ~* '\bBangalore\b' THEN 1 ELSE 0 END as has_bangalore,
        CASE WHEN chunk_text ~* '\bChennai\b' THEN 1 ELSE 0 END as has_chennai,
        CASE WHEN chunk_text ~* '\bAhmedabad\b' THEN 1 ELSE 0 END as has_ahmedabad,
        CASE WHEN chunk_text ~* '\bKolkata\b' THEN 1 ELSE 0 END as has_kolkata,
        CASE WHEN chunk_text ~* '\bHyderabad\b' THEN 1 ELSE 0 END as has_hyderabad,
        CASE WHEN chunk_text ~* '\bPune\b' THEN 1 ELSE 0 END as has_pune
    FROM pdf_chunks
    WHERE chunk_text ~* 'freight|cargo|transport|logistics|shipping|trade|route|corridor'
)
SELECT 
    'Delhi-Mumbai' as pair,
    COUNT(*) as co_occurrences
FROM city_mentions
WHERE has_delhi = 1 AND has_mumbai = 1
UNION ALL
SELECT 
    'Delhi-Ahmedabad' as pair,
    COUNT(*)
FROM city_mentions
WHERE has_delhi = 1 AND has_ahmedabad = 1
UNION ALL
SELECT 
    'Mumbai-Kolkata' as pair,
    COUNT(*)
FROM city_mentions
WHERE has_mumbai = 1 AND has_kolkata = 1
ORDER BY co_occurrences DESC;
```

---

## Methodology

### Analysis Process:
1. **Database Connection**: Established connection to PostgreSQL using psycopg2
2. **Schema Discovery**: Identified available tables (`raw_web_data`, `pdf_chunks`)
3. **Column Analysis**: Determined text columns (`content`, `chunk_text`)
4. **City Pattern Matching**: Used regular expressions with word boundaries (`\b`) for 100+ Indian cities
5. **Logistics Context Filtering**: Applied logistics keyword filters to focus on relevant content
6. **Pair Generation**: For each record with 2+ cities, generated all unique city combinations
7. **Frequency Counting**: Used Counter to aggregate co-occurrence frequencies
8. **Validation**: Ran SQL queries to verify programmatic results

### Cities Analyzed:
The analysis covered 100+ major Indian cities including:
- **Tier-1**: Mumbai, Delhi, Chennai, Kolkata, Bangalore, Hyderabad, Ahmedabad, Pune
- **Tier-2**: Surat, Jaipur, Kanpur, Lucknow, Nagpur, Indore, Thane, Bhopal, Visakhapatnam, etc.
- **Tier-3/Regional**: Kochi, Dharwad, Nanded, Rajkot, etc.

### Logistics Keywords Used:
freight, cargo, transport, logistics, shipping, trade, route, corridor, movement, haulage, shipment, delivery, supply chain, warehouse, distribution, carrier, transit, consignment, dispatch, logistic, transportation

---

## Insights & Recommendations

### Logistics Corridors Identified:
1. **Delhi-Mumbai Industrial Corridor**: 52 co-occurrences - The backbone of Indian freight
2. **Ahmedabad-Delhi Trade Route**: 42 co-occurrences - Gujarat's manufacturing strength
3. **Eastern Corridor (Kolkata-Delhi)**: 29+ co-occurrences - Golden Quadrilateral segment
4. **Southern Tech Corridor (Bangalore-Hyderabad)**: 25 co-occurrences - Emerging pharma & IT logistics

### Strategic Recommendations:
1. **Focus on Delhi-Hub Strategy**: Delhi's centrality in 8/15 top pairs suggests hub-spoke model viability
2. **Ahmedabad Priority**: High mention count (207) suggests strong Gujarat logistics opportunity
3. **Coastal Corridors**: Chennai-Mumbai-Kolkata triangle important for port-to-port logistics
4. **Emerging Routes**: Bangalore-Hyderabad-Pune triangle growing for tech/pharma logistics

---

## Technical Notes

### Database Schema:
```
raw_web_data:
- id (integer)
- source (varchar)
- url (varchar)
- content (text)
- scraped_at (timestamp)

pdf_chunks:
- id (integer)
- file_name (varchar)
- chunk_index (integer)
- chunk_text (text)
- extracted_at (timestamp)
```

### Regex Patterns Used:
- City matching: `\b(city_name)\b` with case-insensitive flag (`~*`)
- Pair matching: `city1.*city2|city2.*city1` for co-occurrence
- Logistics context: `keyword1|keyword2|...|keywordN` combined with city filters

### Data Quality:
- 1,405 of 1,814 records (77.5%) contain logistics keywords
- 53 of 100+ cities appeared in the corpus
- 405 unique pairs from potential 2,650+ combinations

---

## Conclusion

The analysis successfully identified major Indian city pairs in logistics context from the Zippy Logistics database. The **Delhi-Mumbai corridor** leads with 52 co-occurrences, followed by **Ahmedabad-Delhi** at 42. The data reflects India's major logistics patterns including:

1. North-South corridors (Delhi-Bangalore, Delhi-Hyderabad)
2. East-West connections (Mumbai-Kolkata, Chennai-Mumbai)
3. Industrial belts (Ahmedabad-Mumbai, Delhi-Pune)
4. Emerging tech corridors (Bangalore-Hyderabad)

The analysis is based on 1,814 records from web scraping and PDF processing, with 77.5% containing logistics context keywords.

---

**Analysis completed:** 2026-04-05  
**Analyst:** Automated PostgreSQL Analysis System  
**Report generated by:** analyze_cities.py, validate_logistics.py
