
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


def connect_to_bigquery():
    """Authenticates to BigQuery using a service account key file."""
    credentials = service_account.Credentials.from_service_account_file(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    bq_client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    print("connection to bq successful")
    return bq_client

