import pandas as pd
from sqlalchemy import create_engine
import os 

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")




def load_csv_to_postgres(csv_filepath, table_name, db_user, db_password, db_name, db_host="localhost", db_port="5432"):
    df = pd.read_csv(csv_filepath)

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(connection_string)

    df.to_sql(table_name, engine, if_exists="replace", index=False)

    print(f"Loaded {len(df)} rows into table '{table_name}'")


if __name__ == "__main__":
    load_csv_to_postgres(
        csv_filepath="data/raw/raw_data_20260812_020809.csv",  # use one of your actual saved CSVs
        table_name="solar_wind_generation",
        db_user=DB_USER,
        db_password=DB_PASSWORD,
        db_name=DB_NAME
    )