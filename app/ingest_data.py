# app/ingest_data.py

from pycoingecko import CoinGeckoAPI
from sqlalchemy import insert
from db_utils import get_engine
from models import crypto_prices
from datetime import datetime

def fetch_and_store_prices(limit=10):
    cg = CoinGeckoAPI()
    engine = get_engine()

    data = cg.get_coins_markets(vs_currency='usd', per_page=limit)

    rows = []
    for coin in data:
        rows.append({
            "symbol": coin["symbol"].upper(),
            "name": coin["name"],
            "price_usd": coin["current_price"],
            "timestamp": datetime.utcnow()
        })

    with engine.begin() as conn:
        conn.execute(insert(crypto_prices), rows)

    print(f"Inserted {len(rows)} rows into crypto_prices.")
