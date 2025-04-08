# /app/main.py

from db_utils import get_engine
from models import create_tables
from ingest_data import fetch_and_store_all
from fetch_top_coins import fetch_and_store_top_coins
from reddit_ingest import get_reddit_posts           # fetch raw Reddit posts
from sentiment import analyze_and_store              # analyze + store sentiment

def main():
    engine = get_engine()
    create_tables(engine)              # Ensures all necessary tables exist

    #fetch_and_store_top_coins()        # Fetch & store top 50 coins by market cap
    #fetch_and_store_all()              # Backfill price history for all top coins

    reddit_posts = get_reddit_posts(limit=50)        # You can adjust the limit here
    analyze_and_store(reddit_posts)                  # Perform sentiment analysis and store

if __name__ == "__main__":
    main()
