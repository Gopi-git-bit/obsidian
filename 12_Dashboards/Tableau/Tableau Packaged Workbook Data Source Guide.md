---
type: tableau_packaged_workbook_guidance
domain: dashboard_packaging
status: active
created_at: 2026-04-30
linked_workbook: "ZippyLogitech Corridor Delay Analytics"
---
# Tableau Packaged Workbook Data Source Guide

## Purpose

This guide explains how to package the Zippy corridor dashboard as a Tableau `.twbx` file for offline prototyping, sharing and stakeholder demos.

## What a TWBX Contains

A `.twbx` is a zipped packaged workbook that can include:

```text
Workbook definition (.twb XML)
Extracted data (.hyper or .tde)
Local CSV/Excel/JSON files
Images and custom shapes
Custom geocoding files
README/documentation files
```

## Key Rule

```text
TWBX can embed file-based data sources and extracts.
Live PostgreSQL/API connections are not portable unless the recipient has access.
```

## Recommended Data Sources for Zippy Prototype

| Source | Format | Use |
|---|---|---|
| sample_corridors.csv | CSV | Lane-level aggregates and corridor map |
| sample_lane_delay_events.csv | CSV | Shipment-level delay analysis |
| sample_lane_reliability_scores.csv | CSV | Scorecards and alert logic |
| sample_asct_performance.csv | CSV | Adaptive routing impact |
| sample_carriers.csv | CSV | Carrier ranking and benchmarks |
| hyper extracts | Hyper | Faster packaged production demo |

## Supported Embeddable Sources

| Source Type | Extension | Best For |
|---|---|---|
| CSV/Text | .csv, .txt, .tsv | Quick sample data |
| Excel | .xlsx, .xls | Multi-sheet prototypes |
| JSON | .json | API response samples |
| Tableau Extract | .hyper, .tde | Fast packaged demos |
| Spatial files | .shp, .kml, .geojson | Corridor and warehouse maps |
| PDF tables | .pdf | Report extraction demos |

## Not Ideal for Portable TWBX

| Source | Issue | Alternative |
|---|---|---|
| Live PostgreSQL | Requires credentials/network | Create `.hyper` extract |
| ULIP/GSTN APIs | Auth/live query required | Snapshot to CSV/JSON |
| Kafka/IoT streams | Continuous ingestion unsupported | Snapshot to CSV |
| Very large warehouse extracts | File bloat/performance | Pre-aggregate by lane/day |
| User-specific credentials | Security risk | Publish to Tableau Server with RLS |

## Packaging Steps

1. Build workbook using sample CSVs.
2. Hide unused fields.
3. Create extracts if performance is slow.
4. Save as `.twbx`.
5. Test offline on a machine without database access.
6. Include README with data dictionary and refresh instructions.

## Recommended TWBX Structure

```text
ZippyLogitech_Corridor_Dashboard.twbx
├── workbook.twb
├── datasources/
│   ├── corridors_extract.hyper
│   ├── delay_events_sample.hyper
│   └── carriers_benchmarks.csv
├── shapes/
│   ├── reliability_grade_a.png
│   ├── reliability_grade_b.png
│   └── alert_critical.png
├── geocoding/
│   └── south_india_cities_custom.csv
└── README.txt
```

## Portability Checklist

| Check | Pass |
|---|---|
| Opens without PostgreSQL access |  |
| File size below 25 MB for easy sharing |  |
| Sample data anonymized |  |
| All calculated fields work |  |
| Maps render city coordinates |  |
| README included |  |
| Version and data date documented |  |

## Best Practice

Use CSV for first build, Hyper extracts for polished demo, and Tableau Server/Online for live production dashboards.
