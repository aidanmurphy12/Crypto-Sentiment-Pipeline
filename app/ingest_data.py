# /app/ingest_data.py
import requests
from datetime import datetime
from sqlalchemy import insert
from db_utils import get_engine
from models import crypto_prices

COINS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "dogecoin": "DOGE"
}

def fetch_price_history(coin_id, coin_symbol, days=3):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
    }

    response = requests.get(url, params=params)
    
    try:
        response.raise_for_status()  # Raise an error if request failed
        data = response.json()
    except Exception as e:
        print(f"Failed to fetch {coin_symbol}: {e}")
        print("Raw response:", response.text)
        return []

    if "prices" not in data:
        print(f"Warning: 'prices' missing in CoinGecko response for {coin_symbol}")
        print("Response data:", data)
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
    all_rows = []
    for coin_id, coin_symbol in COINS.items():
        print(f"Fetching {coin_symbol}...")
        all_rows.extend(fetch_price_history(coin_id, coin_symbol))
    store_prices(all_rows)
    print(f"Inserted {len(all_rows)} rows into crypto_prices.")

if __name__ == "__main__":
    fetch_and_store_all()
