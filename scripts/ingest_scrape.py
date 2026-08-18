import requests
from datetime import datetime
import os
from bs4 import BeautifulSoup
import pandas as pd 
from tenacity import retry, stop_after_attempt, wait_exponential
from logger_config import setup_logger

logger = setup_logger("ingest_scrape")

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)

def fetch_and_save_html(url, save_dir="data/raw"):
    headers = {"User-Agent": "Mozilla/5.0 (educational data engineering project)"}
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{save_dir}/raw_page_{date_str}.html"
    if os.path.exists(filename):
        logger.info(f"File for {filename} already exists. Skipping download.")
        return filename
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch HTML from {url}: {e}")
        raise
    
    os.makedirs(save_dir, exist_ok=True)
    with open(filename, "wb") as f:
        f.write(response.content)

    logger.info(f"Saved raw HTML to: {filename}")
    return filename



    

def parse_renewable_table(html_filepath):
    try:
        with open(html_filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    except Exception as e:
        logger.error(f"Failed to open or parse HTML file {html_filepath}: {e}")
        raise

    table = soup.find("table", {"class": "wikitable"})
    if not table:
        logger.error("Could not find the renewable electricity production table.")
        raise ValueError("Could not find the renewable electricity production table.")
    
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr")[1:]:  # Skip header row
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cells:
            rows.append(cells)
    
    df = pd.DataFrame(rows, columns=headers)
    logger.info(f"Parsed {len(df)} rows and {len(df.columns)} columns")
    return df

if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_renewable_electricity_production"
    saved_html = fetch_and_save_html(url)
    df =parse_renewable_table(saved_html)

    logger.info(f"Columns: {list(df.columns)}")
    logger.info(f"\n{df.head()}")