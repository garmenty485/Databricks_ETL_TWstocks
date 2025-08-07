# Databricks_ETL_TWstocks
[video review](https://youtu.be/XXX)

## What it does:
- Connects to Azure Data Lake and reads daily and monthly Parquet candlesticks data for Taiwan stocks (using 2330[TSMC] as an example).
- Bronze layer: Extracts raw daily and monthly data and stores them as Delta Tables. With Autoloader's help, we can incrementally fetch new data from the source storage instead of scanning the whole source.
- Silver layer:
  - Checks for missing values.
  - For monthly data feature engineering: calculates Monthly Volume Record High (MVRH) and the percentage distance from the last MVRH.
  - For daily data feature engineering: calculates the highest/lowest return in the next 60 days. Note the definition of lowest return is the lowest "before" it hits the highest point during the period.
- Gold layer:
  - Further aggregates features from the Silver layer to produce tables suitable for machine learning (e.g., days since last MVRH, return rates, 60-day profitability labels, etc.).

## How to start it (databricks):
1. In Databricks, create a new pipeline and set the source codes as 2python.dlt_pipeline and 2sql.dlt_pipeline:
2. Make sure you have set up Azure Data Lake IAM permissions and Databricks connection (refer to the [YouTube tutorial](https://www.youtube.com/watch?v=VkjqViooMtQ)).
3. Watch my video.

## Good SQL/Pyspark to learn:
- **XXX**
  ```sql
  XXXX
  ```
  *Purpose: XXXXX.*
- Add data visualization and automated reporting.
- Enhance data quality checks and anomaly detection.
