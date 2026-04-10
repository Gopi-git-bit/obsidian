
================================================================================
-- PATTERN: COST_FREIGHT
================================================================================

-- Cost/Freight Rate Patterns
SELECT id, file_name, chunk_index, chunk_text, extracted_at
FROM pdf_chunks
WHERE chunk_text ~* '(freight rate|transportation cost|logistics cost|cost per km|cost per ton|freight cost|shipping cost|trucking cost|cargo rate|transport cost|haulage cost|freight charges|rate per km|rate per ton|price per ton|price per km|INR per ton|INR per km|Rs per ton|Rs per km|ton-km cost|cost of transport|freight pricing)'
LIMIT 100;

SELECT id, source, url, content, scraped_at
FROM raw_web_data
WHERE content ~* '(freight rate|transportation cost|logistics cost|cost per km|cost per ton|freight cost|shipping cost|trucking cost|cargo rate|transport cost|haulage cost|freight charges|rate per km|rate per ton|price per ton|price per km|INR per ton|INR per km|Rs per ton|Rs per km|ton-km cost|cost of transport|freight pricing)'
LIMIT 100;
        

================================================================================
-- PATTERN: INFRASTRUCTURE
================================================================================

-- Infrastructure & Bottleneck Patterns
SELECT id, file_name, chunk_index, chunk_text, extracted_at
FROM pdf_chunks
WHERE chunk_text ~* '(bottleneck|congestion|delay|capacity constraint|infrastructure gap|capacity shortage|traffic congestion|port congestion|terminal congestion|infrastructure deficit|inadequate infrastructure|poor connectivity|last mile|insufficient capacity|overloaded|underdeveloped|poor condition|dilapidated|congested corridor)'
LIMIT 100;

SELECT id, source, url, content, scraped_at
FROM raw_web_data
WHERE content ~* '(bottleneck|congestion|delay|capacity constraint|infrastructure gap|capacity shortage|traffic congestion|port congestion|terminal congestion|infrastructure deficit|inadequate infrastructure|poor connectivity|last mile|insufficient capacity|overloaded|underdeveloped|poor condition|dilapidated|congested corridor)'
LIMIT 100;
        

================================================================================
-- PATTERN: POLICY
================================================================================

-- Government Policy & Initiative Patterns
SELECT id, file_name, chunk_index, chunk_text, extracted_at
FROM pdf_chunks
WHERE chunk_text ~* '(PM Gati Shakti|Bharatmala|Sagarmala|National Logistics Policy|Make in India|infrastructure scheme|government scheme|policy initiative|investment plan|economic corridor|dedicated freight corridor|DFC|Expressway|National Highway|logistics policy|transport policy|infrastructure investment|public investment|government investment|billion investment|crore investment|INR investment|USD investment)'
LIMIT 100;

SELECT id, source, url, content, scraped_at
FROM raw_web_data
WHERE content ~* '(PM Gati Shakti|Bharatmala|Sagarmala|National Logistics Policy|Make in India|infrastructure scheme|government scheme|policy initiative|investment plan|economic corridor|dedicated freight corridor|DFC|Expressway|National Highway|logistics policy|transport policy|infrastructure investment|public investment|government investment|billion investment|crore investment|INR investment|USD investment)'
LIMIT 100;
        

================================================================================
-- PATTERN: MODAL_SPLIT
================================================================================

-- Modal Split Data
SELECT id, file_name, chunk_index, chunk_text, extracted_at
FROM pdf_chunks
WHERE chunk_text ~* '(modal share|modal split|transport share|mode share|percentage road|percentage rail|percentage air|percentage water|road transport|rail transport|air cargo|water transport|inland waterway|road freight|rail freight|air freight)'
LIMIT 100;

SELECT id, source, url, content, scraped_at
FROM raw_web_data
WHERE content ~* '(modal share|modal split|transport share|mode share|percentage road|percentage rail|percentage air|percentage water|road transport|rail transport|air cargo|water transport|inland waterway|road freight|rail freight|air freight)'
LIMIT 100;
        

================================================================================
-- PATTERN: GROWTH
================================================================================

-- Growth & Trend Patterns
SELECT id, file_name, chunk_index, chunk_text, extracted_at
FROM pdf_chunks
WHERE chunk_text ~* '(CAGR|growth rate|annual growth|projection|forecast|2025|2030|2035|by 2025|by 2030|expected growth|projected growth|estimated growth|future growth|compound annual growth|year over year|YoY growth|market growth|sector growth|industry growth)'
LIMIT 100;

SELECT id, source, url, content, scraped_at
FROM raw_web_data
WHERE content ~* '(CAGR|growth rate|annual growth|projection|forecast|2025|2030|2035|by 2025|by 2030|expected growth|projected growth|estimated growth|future growth|compound annual growth|year over year|YoY growth|market growth|sector growth|industry growth)'
LIMIT 100;
        
