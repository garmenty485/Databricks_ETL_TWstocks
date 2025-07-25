# DW_ETL_TWstocks

## Inspiration:
This project is inspired by the idea of building a data warehouse ETL pipeline for Taiwan stocks, aiming to explore quantitative trading strategies related to MVRH (Monthly Volume Record High) and machine learning applications. The design follows the Databricks multi-layer data lake architecture (Bronze/Silver/Gold) and integrates Azure Data Lake Storage as the storage source.

## What it does:
- Connects to Azure Data Lake and reads daily and monthly Parquet candlesticks data for Taiwan stocks (using 2330[TSMC] as an example).
- Bronze layer: Extracts raw daily and monthly data and stores them as Delta Tables.
- Silver layer:
  - Checks for missing values.
  - For monthly data feature engineering: calculates Monthly Volume Record High (MVRH) and the percentage distance from the last MVRH.
  - For daily data feature engineering: calculates the highest/lowest return in the next 60 days. Note the definition of lowest return is the lowest "before" it hits the highest point during the period.
- Gold layer:
  - Further aggregates features from the Silver layer to produce tables suitable for machine learning (e.g., days since last MVRH, return rates, 60-day profitability labels, etc.).

## How to start it (databricks):
1. In Databricks, create a new Notebook and upload/execute the project notebooks in order:
   - 1.data architecture.ipynb: Create Catalog and Schema.
   - 2.bronze.ipynb: Connect to Azure Data Lake and create bronze layer tables.
   - 3.silver.ipynb: Perform data cleaning and feature engineering to create silver layer tables.
   - 4.gold.ipynb: Aggregate features and create gold layer tables.
2. Make sure you have set up Azure Data Lake IAM permissions and Databricks connection (refer to the YouTube tutorial link at the beginning of 2.bronze.ipynb).

## Good SQL to learn:
- Create Schema and Catalog (1.data architecture.ipynb)
  ```sql
  USE CATALOG kenworkspace;
  CREATE SCHEMA IF NOT EXISTS TW_stocks_db;
  ```
- Create Bronze layer tables (2.bronze.ipynb)
  ```python
  df_combined.write \
      .format("delta") \
      .mode("overwrite") \
      .saveAsTable(f"kenworkspace.tw_stocks_db.bronze_{folder[0]}")
  ```
- Silver layer monthly feature engineering (3.silver.ipynb)
  ```sql
  CREATE OR REPLACE TABLE kenworkspace.tw_stocks_db.silver_mvrh_monthly AS
    WITH base AS (...)
    ...
  ```
- Silver layer daily feature engineering (3.silver.ipynb)
  ```python
  @pandas_udf(...)
  def calculate_future_returns(...):
      ...
  ```
- Gold layer aggregation and labeling (4.gold.ipynb)
  ```sql
  CREATE OR REPLACE TABLE kenworkspace.tw_stocks_db.gold_ml_mvrh_daily AS
    WITH monthly_mvrh AS (...), ...
  ```

## What's next:
- More features.
- Automate ETL and batch processing for more stock symbols using DLT and Autoloader with scheduler.
- Import Gold layer data into MLflow or other ML platforms for model training and evaluation.
- Add data visualization and automated reporting.
- Enhance data quality checks and anomaly detection.
