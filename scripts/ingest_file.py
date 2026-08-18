import requests
from datetime import datetime
import os
import json
from config import SOLAR_WIND_CSV_URL, SOLAR_WIND_JSON_URL, RAW_DATA_DIR
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential
from logger_config import setup_logger

logger = setup_logger("ingest_file")

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def fetch_and_save_csv(url, save_dir="data/raw"):
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{save_dir}/raw_data_{date_str}.csv"

    # Idempotency check: if the file already exists, skip downloading
    if os.path.exists(filename):
        logger.info(f"File for {filename} already exists. Skipping download.")
        return filename

    # Fetch the raw file from the URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # throws an error if the download failed
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch data from {url}: {e}")
        raise

    # Make sure the save directory actually exists
    os.makedirs(save_dir, exist_ok=True)

    # Save the raw content, untouched, exactly as received
    with open(filename, "wb") as f:
        f.write(response.content)

    logger.info(f"Saved raw file to: {filename}")
    return filename


def verify_csv(filepath):
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        logger.error(f"Failed to load CSV from {filepath}: {e}")
        raise

    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    logger.info(f"Columns: {list(df.columns)}")
    logger.info(f"\n{df.head()}")
    return df




@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)

def fetch_and_save_json(url, save_dir="data/raw"):
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{save_dir}/raw_metadata_{date_str}.json"

    if os.path.exists(filename):
        logger.info(f"File for {filename} already exists. Skipping download.")
        return filename

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch JSON from {url}: {e}")
        raise

    os.makedirs(save_dir, exist_ok=True)

    with open(filename, "wb") as f:
        f.write(response.content)

    logger.info(f"Saved raw file to: {filename}")
    return filename


def verify_json(filepath):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON from {filepath}: {e}")
        raise

    logger.info(f"Top-level type: {type(data)}")
    if isinstance(data, dict):
        logger.info(f"Top-level keys: {list(data.keys())}")
    return data


def convert_to_parquet(csv_filepath, save_dir="data/raw"):

    date_str = datetime.now().strftime("%Y%m%d") 
    filename = f"{save_dir}/raw_data_{date_str}.parquet"
    if os.path.exists(filename):
        logger.info(f"File for {filename} already exists. Skipping conversion.")
        return filename
    try:
        df = pd.read_csv(csv_filepath)
    except Exception as e:
        logger.error(f"Failed to read csv file from {csv_filepath}: {e}")
        raise

    os.makedirs(save_dir, exist_ok=True)
    df.to_parquet(filename, index=False)
    logger.info(f"Saved parquet file to: {filename}")
    return filename


def verify_parquet(filepath):
    try:
        df = pd.read_parquet(filepath)
    except Exception as e:
        logger.error(f"Failed to load parquet from {filepath}: {e}")
        raise

    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    logger.info(f"Columns: {list(df.columns)}")
    logger.info(f"\n{df.head()}")
    return df


def convert_to_xlsx(csv_filepath, save_dir="data/raw"):
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{save_dir}/raw_data_{date_str}.xlsx"
    if os.path.exists(filename):
        logger.info(f"File for {filename} already exists. Skipping conversion.")
        return filename
    
    try:
        df = pd.read_csv(csv_filepath)
    except Exception as e:
        logger.error(f"Failed to read csv file from {csv_filepath}: {e}")
        raise

    os.makedirs(save_dir, exist_ok=True)
    df.to_excel(filename, index=False)

    logger.info(f"Saved xlsx file to: {filename}")
    return filename


def verify_xlsx(filepath):
    try:
        df = pd.read_excel(filepath)
    except Exception as e:
        logger.error(f"Failed to load xlsx from {filepath}: {e}")
        raise

    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    logger.info(f"Columns: {list(df.columns)}")
    logger.info(f"\n{df.head()}")
    return df


from validate_schema import validate_dataframe, solar_wind_schema

if __name__ == "__main__":
    
    saved_csv = fetch_and_save_csv(SOLAR_WIND_CSV_URL, save_dir=RAW_DATA_DIR)
    df = verify_csv(saved_csv)
    df = validate_dataframe(df, solar_wind_schema, source_name="CSV ingestion")

    saved_json = fetch_and_save_json(SOLAR_WIND_JSON_URL, save_dir=RAW_DATA_DIR)
    verify_json(saved_json)

    saved_parquet = convert_to_parquet(saved_csv, save_dir=RAW_DATA_DIR)
    verify_parquet(saved_parquet)

    saved_xlsx = convert_to_xlsx(saved_csv, save_dir=RAW_DATA_DIR)
    verify_xlsx(saved_xlsx)