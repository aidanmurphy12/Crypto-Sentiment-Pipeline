# /app/main.py

from db_utils import get_engine
from models import create_tables
from ingest_data import fetch_and_store_all
from fetch_top_coins import fetch_and_store_top_coins

def main():
    engine = get_engine()
    create_tables(engine)  # Ensures all necessary tables are created

    fetch_and_store_top_coins()  # Fetches & stores the top 50 coins by market cap
    fetch_and_store_all()        # Backfills price history for BTC, ETH, and DOGE

if __name__ == "__main__":
    main()
