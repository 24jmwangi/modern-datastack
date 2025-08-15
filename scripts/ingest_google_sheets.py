
import gspread
import pandas as pd
import os
from sqlalchemy import create_engine
from google.cloud import bigquery
from google.oauth2 import service_account



def connect_to_gsheets():
    gc = gspread.service_account(filename="gcp-key.json")
    _sh = gc.open_by_key("1XV31clJBum7yNtZBqF_gD_w-6AFp_8wPtOvyG8HBueM")
    print("=========Connected=========")
    return _sh

def download_data(_sh):
    # Assumes you have two sheets: "ticker" and one per ticker symbol
    ticker_ws = _sh.worksheet("ticker")
    ticker_df = pd.DataFrame(ticker_ws.get_all_records())
    # Standardize column names
    ticker_df.columns = [c.lower().replace(" ", "_").replace("-", "_") for c in ticker_df.columns]
    history_dfs = {}
    for ticker in list(ticker_df["ticker"]):
        try:
            ws = _sh.worksheet(ticker)
            df = pd.DataFrame(ws.get_all_records())
            # Standardize column names
            df.columns = [c.lower()for c in df.columns]
            history_dfs[ticker] = df
        except gspread.WorksheetNotFound:
            continue


    return ticker_df, history_dfs

_sh = connect_to_gsheets()

df1,df2 = download_data(_sh)

# load dfs to postgres db

# Read Postgres credentials from env variables
PG_USER = os.getenv("POSTGRES_USER")
PG_PASS = os.getenv("POSTGRES_PASSWORD")
PG_DB = os.getenv("POSTGRES_DB")
PG_HOST = os.getenv("POSTGRES_HOST")
PG_PORT = os.getenv("POSTGRES_PORT")

# Create SQLAlchemy connection string
connection_str = f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"
engine = create_engine(connection_str)

df1.to_sql("tickers", engine, if_exists="replace", index=False)

for table_name, df in df2.items():
    df.to_sql(table_name, engine, index=False, if_exists="replace")  
    print(f" ingested {table_name} into PostgreSQL")

print("data ingested successfully")


### INCREMENTAL LOADING
def connect_to_bigquery():
    """Authenticates to BigQuery using a service account key file."""
    credentials = service_account.Credentials.from_service_account_file("gcp-key.json")
    bq_client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    print("connection to bq successful")
    return bq_client

def get_last_load_timestamp(bq_client, dataset_id, table_name, timestamp_column):
    """
    Retrieves the maximum timestamp from a BigQuery table to determine the last load.
    Returns None if the table does not exist.
    """
    try:
        query = f"SELECT MAX({timestamp_column}) FROM `{bq_client.project}.{dataset_id}.{table_name}`"
        query_job = bq_client.query(query)
        result = query_job.result().to_dataframe()
        return result.iloc[0, 0]
    except Exception as e:
        print(f"BigQuery table '{table_name}' not found or empty. Performing a full load.")
        return None


def load_to_bigquery(bq_client, engine, dataset_id, pg_table_name, bq_table_name, timestamp_column):
    """
    Performs an incremental data load from a PostgreSQL table to a BigQuery table.
    """
    print(f"Starting incremental load for table: {pg_table_name}")

    # Get the last load timestamp from BigQuery
    last_load_timestamp = get_last_load_timestamp(bq_client, dataset_id, bq_table_name, timestamp_column)

    # Build the PostgreSQL query
    if last_load_timestamp:
        # Filter for new records
        # Note: Datetime columns in BigQuery are in UTC, so ensure your Postgres timestamps are handled correctly.
        pg_query = f"SELECT * FROM {pg_table_name} WHERE {timestamp_column} > '{last_load_timestamp}'"
    else:
        # Full load if the table doesn't exist in BigQuery
        pg_query = f"SELECT * FROM {pg_table_name}"

    try:
        new_data_df = pd.read_sql(pg_query, engine)
    except Exception as e:
        print(f"Error reading from PostgreSQL table {pg_table_name}: {e}")
        return

    if new_data_df.empty:
        print(f"No new records found for table: {pg_table_name}")
        return

    # Load new data to BigQuery
    print(f"Found {len(new_data_df)} new records for table: {pg_table_name}. Loading to BigQuery...")
    job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_APPEND)
    
    bq_table_ref = bq_client.dataset(dataset_id).table(bq_table_name)
    job = bq_client.load_table_from_dataframe(new_data_df, bq_table_ref, job_config=job_config)
    
    try:
        job.result()  # Wait for the job to complete
        print(f"Successfully loaded {len(new_data_df)} records into {bq_table_name} in BigQuery.")
    except Exception as e:
        print(f"Error loading data to BigQuery for table {bq_table_name}: {e}")
        print(job.errors)



# Initialize clients
bq_client = connect_to_bigquery()

# Get the BigQuery dataset ID from the client's project
project_id = bq_client.project
dataset_id = f"{project_id}_silver"

# Define table names and their respective timestamp columns
tables_to_load = {
    "tickers": "last_trade_time",
    "AAPL": "date",
    "GOOG": "date"
    # Add all other tables from your GSheets
}

# Run the incremental load for each table
for pg_table_name, timestamp_column in tables_to_load.items():
    load_to_bigquery(
        bq_client=bq_client,
        engine=engine,
        dataset_id=dataset_id,
        pg_table_name=pg_table_name,
        bq_table_name=pg_table_name,
        timestamp_column=timestamp_column
    )
