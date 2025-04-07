# /app/fetch_top_coins.py

import requests
from sqlalchemy import insert
from db_utils import get_engine
from models import top_coins
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_top_50_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    headers = {
        "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
    }
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false"
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    data = response.json()
    coins = []

    for coin in data:
        coins.append({
            "id": coin["id"],
            "symbol": coin["symbol"].upper(),
            "name": coin["name"],
            "market_cap_rank": coin["market_cap_rank"]
        })

    return coins

def store_top_coins(coins):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(top_coins.delete())  # Clear existing data
        conn.execute(insert(top_coins), coins)
        print(f"Inserted {len(coins)} coins into top_coins.")

def fetch_and_store_top_coins():
    coins = fetch_top_50_coins()
    store_top_coins(coins)

if __name__ == "__main__":
    fetch_and_store_top_coins()