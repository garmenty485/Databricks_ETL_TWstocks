# Databricks_ETL_TWstocks
Welcome! If you're a recruiter, I recommend watching [this video] for a quick assessment of my abilities. The video is a review of this project.

## Inspiration:
This project is inspired by the idea of building a Databricks ETL pipeline for Taiwan stocks, aiming to explore quantitative trading strategies related to MVRH (Monthly Volume Record High). The design follows the Databricks multi-layer data lake architecture (Bronze/Silver/Gold) and integrates Azure Data Lake Storage Gen2 as the storage source.

## Navigation:
- The main part is in [advanced-dlt pipeline](./advanced-dlt pipeline), where I implemented a "Lakeflow Declarative Pipeline" (also known as "DLT") to complete this project.
- If you're new to Databricks, [basic-manual pipeline](./basic-manual pipeline) is a manual ETL pipeline where you might learn something from.
- Both of them are doing the same thing but different way.

## What it does:
- Connects to Azure Data Lake and reads daily and monthly Parquet candlesticks data for Taiwan stocks (using 2330[TSMC] as an example).
- Bronze layer: Extracts raw daily and monthly data and stores them as Delta Tables.
- Silver layer:
  - Checks for missing values.
  - For monthly data feature engineering: calculates Monthly Volume Record High (MVRH) and the percentage distance from the last MVRH.
  - For daily data feature engineering: calculates the highest/lowest return in the next 60 days. Note the definition of lowest return is the lowest "before" it hits the highest point during the period.
- Gold layer:
  - Further aggregates features from the Silver layer to produce tables suitable for machine learning (e.g., days since last MVRH, return rates, 60-day profitability labels, etc.).
- Add data visualization and automated reporting.
- Enhance data quality checks and anomaly detection.
