# /app/ingest_data.py
import os
import requests
import time
from datetime import datetime
from sqlalchemy import insert, select
from db_utils import get_engine
from models import crypto_prices, top_coins
from dotenv import load_dotenv

load_dotenv()

def fetch_price_history(coin_id, coin_symbol, days=3):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    headers = {
        "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
    }
    params = {
        "vs_currency": "usd",
        "days": days,
    }

    response = requests.get(url, params=params, headers=headers)

    try:
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Failed to fetch {coin_symbol}: {e}")
        print("Raw response:", response.text)
        return []

    if "prices" not in data:
        print(f"Warning: 'prices' missing in response for {coin_symbol}")
        return []

    rows = []
    for point in data["prices"]:
        timestamp = datetime.utcfromtimestamp(point[0] / 1000.0)
        price_usd = point[1]
        rows.append({
            "symbol": coin_symbol,
            "name": coin_id,
            "price_usd": price_usd,
            "timestamp": timestamp
        })

    return rows

def store_prices(rows):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(insert(crypto_prices), rows)

def fetch_and_store_all():
    engine = get_engine()
    with engine.connect() as conn:
        coins = conn.execute(select(top_coins)).fetchall()

    all_rows = []
    for i, coin in enumerate(coins):
        coin_id = coin.id
        coin_symbol = coin.symbol.upper()
        print(f"Fetching {coin_symbol}... ({i+1}/{len(coins)})")

        all_rows.extend(fetch_price_history(coin_id, coin_symbol))
        time.sleep(2.1)  # Keep under 30 requests per minute

    store_prices(all_rows)
    print(f"Inserted {len(all_rows)} rows into crypto_prices.")

if __name__ == "__main__":
    fetch_and_store_all()
