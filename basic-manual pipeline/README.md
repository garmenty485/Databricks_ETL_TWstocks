# Databricks_ETL_TWstocks
[video review](https://youtu.be/v6nYd0esfg8), I suggest watch it in 2X speed because of my slow English :)

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

## Good SQL/Pyspark to learn:
- **Window Functions for Running Maximum (3.silver.ipynb)**
  ```sql
  MAX(volume) OVER (ORDER BY date) AS max_volume_so_far
  ```
  *Purpose: Calculates the running maximum of volume up to each row, useful for identifying record highs.*

- **LAG with IGNORE NULLS for Last Record Retrieval (3.silver.ipynb)**
  ```sql
  LAG(CASE WHEN mvrh THEN volume ELSE NULL END) IGNORE NULLS OVER (ORDER BY date) AS last_mvrh_volume
  ```
  *Purpose: Retrieves the last non-null value of a column (e.g., last record high volume), skipping nulls, which is powerful for time series analysis.*

- **Complex Feature Engineering with Pandas UDF (3.silver.ipynb)**
  ```python
  @pandas_udf(returnType=StructType([...]))
  def calculate_future_returns(closes: pd.Series, highs: pd.Series, lows: pd.Series) -> pd.DataFrame:
      # ...
  ```
  *Purpose: Uses Pandas UDF to calculate future window-based statistics (e.g., 60-day future high/low returns) efficiently in Spark.*

- **Lateral Join (LEFT JOIN LATERAL) for Latest Related Record (4.gold.ipynb)**
  ```sql
  LEFT JOIN LATERAL (
    SELECT * FROM monthly_mvrh mm
    WHERE mm.mvrh_month_date < DATE_TRUNC('month', d.date)
    ORDER BY mm.mvrh_month_date DESC
    LIMIT 1
  ) mm
  ```
  *Purpose: For each daily record, finds the most recent monthly record high before that day. This is a powerful pattern for time-aligned joins.*

- **Boolean Labeling and Conditional Logic (4.gold.ipynb)**
  ```sql
  (60fhr_percent > 20 AND 60flr_percent > -10) AS 60_days_profitable
  ```
  *Purpose: Creates a boolean label for ML based on multiple conditions, useful for classification tasks.*
- Add data visualization and automated reporting.
- Enhance data quality checks and anomaly detection.
