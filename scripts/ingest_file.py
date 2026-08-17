import requests
from datetime import datetime
import os
import json
import pandas as pd
from logger_config import setup_logger

logger = setup_logger("ingest_file")


def fetch_and_save_csv(url, save_dir="data/raw"):
    # Step 1: Fetch the raw file from the URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # throws an error if the download failed
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch data from {url}: {e}")
        raise

    # Step 2: Build a filename with a timestamp, so each pull is kept separate
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_dir}/raw_data_{timestamp}.csv"

    # Step 3: Make sure the save directory actually exists
    os.makedirs(save_dir, exist_ok=True)

    # Step 4: Save the raw content, untouched, exactly as received
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


def fetch_and_save_json(url, save_dir="data/raw"):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch JSON from {url}: {e}")
        raise

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_dir}/raw_metadata_{timestamp}.json"

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
    try:
        df = pd.read_csv(csv_filepath)
    except Exception as e:
        logger.error(f"Failed to read csv file from {csv_filepath}: {e}")
        raise

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_dir}/raw_data_{timestamp}.parquet"
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
    try:
        df = pd.read_csv(csv_filepath)
    except Exception as e:
        logger.error(f"Failed to read csv file from {csv_filepath}: {e}")
        raise

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_dir}/raw_data_{timestamp}.xlsx"
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


if __name__ == "__main__":
    url = "https://ourworldindata.org/grapher/solar-and-wind-power-generation.csv?v=1&csvType=full&useColumnShortNames=false"
    saved_csv = fetch_and_save_csv(url)
    verify_csv(saved_csv)

    json_url = "https://ourworldindata.org/grapher/solar-and-wind-power-generation.metadata.json?v=1&csvType=full&useColumnShortNames=false"
    saved_json = fetch_and_save_json(json_url)
    verify_json(saved_json)

    saved_parquet = convert_to_parquet(saved_csv)
    verify_parquet(saved_parquet)

    saved_xlsx = convert_to_xlsx(saved_csv)
    verify_xlsx(saved_xlsx)