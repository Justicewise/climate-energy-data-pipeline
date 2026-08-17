import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from logger_config import setup_logger

logger = setup_logger("ingest_db")

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")





def fetch_from_postgres(table_name, db_user, db_password, db_name, db_host="localhost", db_port="5432", save_dir="data/raw"):
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(connection_string)

    query = f"SELECT * FROM {table_name}"
    try:
        df = pd.read_sql(query, engine)
    except Exception as e:
        logger.error(f"Failed to query table '{table_name}': {e}")
        raise

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_dir}/raw_from_db_{timestamp}.csv"

    os.makedirs(save_dir, exist_ok=True)
    df.to_csv(filename, index=False)

    logger.info(f"Pulled {len(df)} rows from '{table_name}' and saved to {filename}")
    return df


if __name__ == "__main__":
    df = fetch_from_postgres(
        table_name="solar_wind_generation",
        db_user=DB_USER,
        db_password=DB_PASSWORD,
        db_name=DB_NAME
    )
    logger.info(f"\n{df.head()}")