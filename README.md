# DW_ETL_TWstocks

## Inspiration:
本專案靈感來自於希望建立一個台灣股票的數據倉儲（Data Warehouse）ETL流程，並以此探索量化交易策略與機器學習應用。專案設計參考了Databricks的多層資料湖（Bronze/Silver/Gold）架構，並結合Azure Data Lake作為儲存來源。

## What it does:
- 連接Azure Data Lake，讀取台灣股票（以2330為例）每日與每月的Parquet數據。
- Bronze層：彙整原始每日、每月資料，存為Delta Table。
- Silver層：
  - 檢查缺失值。
  - 對月資料計算歷史最大成交量（MVRH）及距離上次MVRH的百分比。
  - 對日資料計算未來60日內最高/最低報酬率。
- Gold層：
  - 將Silver層特徵進一步彙整，產生可用於機器學習的表格（如距離MVRH的天數、報酬率、是否60天內獲利等標籤）。

## How to start it (databricks):
1. 在Databricks建立Notebook，依序上傳並執行本專案的ipynb檔案：
   - 1.data architecture.ipynb：建立Catalog與Schema。
   - 2.bronze.ipynb：連接Azure Data Lake，建立bronze層資料表。
   - 3.silver.ipynb：進行資料清理與特徵工程，建立silver層資料表。
   - 4.gold.ipynb：彙整特徵，建立gold層資料表。
2. 請確保已設定好Azure Data Lake的IAM權限與Databricks連線（參考2.bronze.ipynb開頭的YouTube教學連結）。

## Good SQL to learn (indicate the corresponding file for each):
- 建立Schema與Catalog（1.data architecture.ipynb）
  ```sql
  USE CATALOG kenworkspace;
  CREATE SCHEMA IF NOT EXISTS TW_stocks_db;
  ```
- 建立Bronze層表格（2.bronze.ipynb）
  ```python
  df_combined.write \
      .format("delta") \
      .mode("overwrite") \
      .saveAsTable(f"kenworkspace.tw_stocks_db.bronze_{folder[0]}")
  ```
- Silver層月資料特徵工程（3.silver.ipynb）
  ```sql
  CREATE OR REPLACE TABLE kenworkspace.tw_stocks_db.silver_mvrh_monthly AS
    WITH base AS (...)
    ...
  ```
- Silver層日資料特徵工程（3.silver.ipynb）
  ```python
  @pandas_udf(...)
  def calculate_future_returns(...):
      ...
  ```
- Gold層資料彙整與標籤（4.gold.ipynb）
  ```sql
  CREATE OR REPLACE TABLE kenworkspace.tw_stocks_db.gold_ml_mvrh_daily AS
    WITH monthly_mvrh AS (...), ...
  ```

## What's next:
- 增加更多股票代碼的自動化處理與批次ETL。
- 將Gold層資料導入MLflow或其他ML平台進行模型訓練與評估。
- 增加資料視覺化與自動化報表。
- 強化資料品質檢查與異常偵測。