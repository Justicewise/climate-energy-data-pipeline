import requests
from datetime import datetime
import os 
import json

def fetch_and_save_csv(url, save_dir="data/raw"):
     # Step 1: Fetch the raw file from the URL
     response = requests.get(url)
     response.raise_for_status() # throws an error if the download failed
     # Step 2: Build a filename with a timestamp, so each pull is kept separate
     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
     filename = f"{save_dir}/raw_data_{timestamp}.csv"
     # Step 3: Make sure the save directory actually exists
     os.makedirs(save_dir,exist_ok=True)
      # Step 4: Save the raw content, untouched, exactly as received
     with open(filename,"wb") as f:
        f.write(response.content)
     print(f"Saved raw file to: {filename}")
     return filename
import pandas as pd

def verify_csv(filepath):
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")
    print(df.head())
    return df
import json

def fetch_and_save_json(url, save_dir="data/raw"):
    response = requests.get(url)
    response.raise_for_status()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_dir}/raw_metadata_{timestamp}.json"
    

    os.makedirs(save_dir, exist_ok=True)

    with open(filename, "wb") as f:
        f.write(response.content)

    print(f"Saved raw file to: {filename}")
    return filename


def verify_json(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)

    print(f"Top-level type: {type(data)}")
    if isinstance(data, dict):
        print(f"Top-level keys: {list(data.keys())}")
    return data



def convert_to_parquet(csv_filepath, save_dir="data/raw"):

    df = pd.read_csv(csv_filepath)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_dir}/raw_data_{timestamp}.parquet"
    os.makedirs(save_dir, exist_ok=True)
    df.to_parquet(filename, index=False)
    print(f"Saved parquet file to: {filename}")
    return filename

def verify_parquet(filepath):
    df = pd.read_parquet(filepath)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")
    print(df.head())
    return df

 
def convert_to_xlsx(csv_filepath, save_dir="data/raw"):
    df = pd.read_csv(csv_filepath)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_dir}/raw_data_{timestamp}.xlsx"
    os.makedirs(save_dir, exist_ok=True)
    df.to_excel(filename, index=False)

    print(f"Saved xlsx file to: {filename}")
    return filename


def verify_xlsx(filepath):
    df = pd.read_excel(filepath)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")
    print(df.head())
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