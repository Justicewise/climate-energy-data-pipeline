# Climate & Energy Data Pipeline

A data engineering portfolio project that ingests, processes, and analyzes global solar and wind power generation data.

## Project Goal
Build an end-to-end data pipeline demonstrating real-world data engineering skills: multi-format ingestion, cloud storage, transformation, and analysis — using publicly available energy transition data.

## Current Progress: File Ingestion
The pipeline currently supports ingesting data in four formats:
- **CSV** — direct download from source
- **JSON** — metadata ingestion
- **Parquet** — converted from raw CSV for efficient columnar storage
- **XLSX** — converted from raw CSV for stakeholder-friendly reporting

Each ingestion method fetches data, saves it untouched to a raw/Bronze layer, then verifies it loaded correctly (row/column counts, schema check) — without any cleaning or transformation at this stage.

## Data Source
[Our World in Data — Solar and Wind Power Generation](https://ourworldindata.org/grapher/solar-and-wind-power-generation)

## Data Quality Observations (from initial ingestion)
- Regional aggregates (e.g., "ASEAN (Ember)") have null country codes, unlike individual countries
- Early years (pre-2000s) show 0.0 generation values in many regions, reflecting minimal solar/wind adoption historically.
- Scraped renewable energy data (Wikipedia/Ember) uses absolute values (TWh) with different structure than the Our World in Data source — will need alignment during transformation

## Tech Stack
- Python (pandas, requests)
- PostgreSQL / MySQL (planned — database ingestion layer)
- AWS (planned — S3, Glue, Athena)

## Roadmap
- [x] File ingestion (CSV, JSON, Parquet, XLSX)
- [x] Web scraping ingestion
- [ ] Database ingestion
- [ ] AWS layer (S3, Glue, Athena)
- [ ] Data cleaning and transformation (Silver layer)
- [ ] Business-ready aggregates (Gold layer)

## Author
Godson Justice — transitioning into data engineering, Data Analysis, Crm , Digital Marketing, Financial market analyst 