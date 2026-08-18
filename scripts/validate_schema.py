

import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema, Check

import pandas as pd
from logger_config import setup_logger

logger = setup_logger("validate_schema")

solar_wind_schema = DataFrameSchema({
    "Entity": Column(str, nullable=False),
    "Code": Column(str, nullable=True),  # regional aggregates have no code, so nullable
    "Year": Column(int, Check.in_range(1900, 2100), nullable=False),
    "Solar and wind": Column(float, Check.greater_than_or_equal_to(0), nullable=True),
})


def validate_dataframe(df, schema, source_name="unknown"):
    try:
        validated_df = schema.validate(df, lazy=True)
        logger.info(f"Validation passed for {source_name}: {len(validated_df)} rows conform to schema")
        return validated_df
    except pa.errors.SchemaErrors as e:
        logger.error(f"Validation FAILED for {source_name}:\n{e.failure_cases}")
        raise


renewable_table_schema = DataFrameSchema({
    "Location": Column(str, nullable=False),
    "Renew.": Column(str, nullable=True),
    "Hydro": Column(str, nullable=True),
    "Wind": Column(str, nullable=True),
    "Solar": Column(str, nullable=True),
    "Bio.": Column(str, nullable=True),
    "Other": Column(str, nullable=True),
    "Year": Column(str, nullable=True),
})