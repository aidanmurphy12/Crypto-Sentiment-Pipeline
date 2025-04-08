# app/reddit_ingest.py

import os
from datetime import datetime
import praw
from dotenv import load_dotenv
from sqlalchemy import insert
from db_utils import get_engine
from models import sentiment_data
from sqlalchemy.exc import IntegrityError

# Load variables from .env file
load_dotenv()

# Basic coin keyword mapping (expand this later using top_coins table if needed)
COIN_KEYWORDS = {
    "BTC": ["bitcoin", "btc"],
    "ETH": ["ethereum", "eth"],
    "DOGE": ["dogecoin", "doge"],
    "SOL": ["solana", "sol"],
    "ADA": ["cardano", "ada"],
    "XRP": ["xrp", "ripple"]
}

def identify_coin(post_text):
    lower_text = post_text.lower()
    for symbol, keywords in COIN_KEYWORDS.items():
        if any(keyword in lower_text for keyword in keywords):
            return symbol
    return "UNKNOWN"

def get_reddit_posts(subreddit="CryptoCurrency", limit=50):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    posts = []
    for post in reddit.subreddit(subreddit).hot(limit=limit):
        posts.append({
            "source": "reddit",
            "coin": "UNKNOWN",
            "text": f"{post.title} {post.selftext}".strip(),
            "timestamp": datetime.utcfromtimestamp(post.created_utc)
        })


    return posts

def store_reddit_posts(posts):
    engine = get_engine()
    with engine.begin() as conn:
        try:
            conn.execute(insert(sentiment_data), posts)
            print(f"Inserted {len(posts)} Reddit posts into sentiment_data.")
        except IntegrityError as e:
            print("Error inserting Reddit posts:", e)

def fetch_and_store_reddit():
    posts = get_reddit_posts()
    store_reddit_posts(posts)

if __name__ == "__main__":
    fetch_and_store_reddit()
