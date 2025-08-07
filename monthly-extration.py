import os
import io
from configparser import ConfigParser
from esun_marketdata import EsunMarketdata
from dotenv import load_dotenv
from azure.storage.filedatalake import DataLakeFileClient
import pyarrow as pa
import pyarrow.parquet as pq
import json
from datetime import datetime

load_dotenv()

# Load config and log in
config = ConfigParser()
config.read('./config.ini')
sdk = EsunMarketdata(config)
sdk.login()

stock = sdk.rest_client.stock

symbol = "2330"
timeframe = "M"
start_year = 2024  # e.g., 2010
end_year = 2024    # e.g., 2024

connection_string = os.getenv("AZURE_CONNECTION_STRING")

schema = pa.schema([
    pa.field("date", pa.string()),
    pa.field("open", pa.float64()),
    pa.field("high", pa.float64()),
    pa.field("low", pa.float64()),
    pa.field("close", pa.float64()),
    pa.field("volume", pa.int64()),
    pa.field("symbol", pa.string())
])

for year in range(start_year, end_year + 1):
    date_from = f"{year}-01-01"
    date_to = f"{year}-12-31"
    print(f"Fetching {symbol} data from {date_from} to {date_to} ...")
    data = stock.historical.candles(**{"symbol": symbol, "from": date_from, "to": date_to, "timeframe": timeframe})
    metadata = {k: v for k, v in data.items() if k != "data"}
    kline_data = data["data"]

    # Skip if no data
    if not kline_data:
        print(f"No data for {year}, skipping.")
        continue

    # Add symbol field
    for row in kline_data:
        row["symbol"] = metadata["symbol"]

    table = pa.Table.from_pylist(kline_data, schema=schema)
    parquet_buffer = io.BytesIO()
    pq.write_table(table, parquet_buffer)
    parquet_buffer.seek(0)
    parquet_bytes = parquet_buffer.read()

    # Smart filename: 2330_M_2010.parquet
    filename = f"{symbol}_{timeframe}_{year}.parquet"
    file_client = DataLakeFileClient.from_connection_string(connection_string, "twstocks/monthly", filename)

    try:
        file_client.create_file()
    except Exception as e:
        print("File might already exist, skipping creation. Error:", e)

    file_client.upload_data(parquet_bytes, overwrite=True)
    print(f"✅ {filename} uploaded successfully")
