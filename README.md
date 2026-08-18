# Climate & Energy Data Pipeline

A data engineering portfolio project that ingests, processes, and analyzes global solar and wind power generation data.

## Project Goal
Build an end-to-end data pipeline demonstrating real-world data engineering skills: multi-format ingestion, cloud storage, transformation, and analysis — using publicly available energy transition data.

## Current Progress: Ingestion Layer (Complete)
The pipeline ingests data through four methods, each following the same disciplined pattern: fetch/query → save raw (Bronze layer) → verify → validate.

- **File ingestion** — CSV, JSON, Parquet, XLSX (download and format conversion)
- **Web scraping** — BeautifulSoup, manual HTML parsing of a live Wikipedia table
- **Database ingestion** — PostgreSQL via SQLAlchemy

### Production-grade practices built into the ingestion layer
- **Structured logging** — every script logs to both console and a persistent `logs/pipeline.log` file, with timestamps and severity levels (INFO/ERROR), replacing ad-hoc print statements
- **Error handling** — try/except blocks placed precisely at each function's actual point of failure (not blindly wrapped), with clear error logging before re-raising
- **Retry logic** — network-facing functions (file downloads, web scraping, database queries) use exponential backoff retry (via `tenacity`) to handle transient failures gracefully
- **Idempotency** — all ingestion functions use date-based filenames and existence checks to avoid duplicate work on repeated runs, with consistent return types across skip/execute code paths
- **Schema validation** — explicit data contracts defined with `pandera`, validating column types, nullability, and value ranges for every ingested dataset before it's considered trustworthy
- **Secured credentials** — database credentials managed via `.env` (excluded from version control), never hardcoded

## Data Sources
- [Our World in Data — Solar and Wind Power Generation](https://ourworldindata.org/grapher/solar-and-wind-power-generation) (file/API ingestion)
- [Wikipedia — List of countries by renewable electricity production](https://en.wikipedia.org/wiki/List_of_countries_by_renewable_electricity_production) (web scraping)

## Data Quality Observations
- Regional aggregates (e.g., "ASEAN (Ember)") have null country codes, unlike individual countries — reflected as a nullable field in the schema, not an error
- Early years (pre-2000s) show 0.0 generation values in many regions, reflecting minimal solar/wind adoption historically
- Scraped renewable energy data (Wikipedia/Ember) uses absolute values (TWh) as raw strings with comma formatting, and a different structure than the Our World in Data source — will need type conversion and alignment during transformation

## Tech Stack
- **Python** — pandas, requests, BeautifulSoup, SQLAlchemy, tenacity, pandera
- **PostgreSQL** — database ingestion layer
- **Logging** — Python's built-in `logging` module, custom shared config
- **AWS** (planned) — S3, Glue, Athena

## Roadmap
- [x] File ingestion (CSV, JSON, Parquet, XLSX)
- [x] Web scraping ingestion
- [x] Database ingestion
- [x] Logging, error handling, retry logic, idempotency, schema validation
- [ ] AWS layer (S3, Glue, Athena)
- [ ] Data cleaning and transformation (Silver layer)
- [ ] Business-ready aggregates (Gold layer)

## Author
Godson Justice — transitioning into data engineering, Data Analysis, Crm , Digital Marketing, Financial market analyst 