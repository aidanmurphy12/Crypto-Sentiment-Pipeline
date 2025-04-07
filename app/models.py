# models.py

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
from datetime import datetime
from db_utils import get_engine

engine = get_engine()
metadata = MetaData()

crypto_prices = Table(
    "crypto_prices", metadata,
    Column("id", Integer, primary_key=True),
    Column("symbol", String),
    Column("name", String),
    Column("price_usd", Float),
    Column("timestamp", DateTime, default=datetime.utcnow)
)

sentiment_data = Table(
    "sentiment_data", metadata,
    Column("id", Integer, primary_key=True),
    Column("source", String),
    Column("coin", String),
    Column("text", String),
    Column("sentiment_score", Float),
    Column("timestamp", DateTime, default=datetime.utcnow)
)

top_coins = Table(
    "top_coins", metadata,
    Column("id", String, primary_key=True),           # CoinGecko's coin ID (e.g., "bitcoin")
    Column("symbol", String),                         # Ticker symbol (e.g., "BTC")
    Column("name", String),                           # Full name (e.g., "Bitcoin")
    Column("market_cap_rank", Integer)                # CoinGecko market cap rank
)

def create_tables(engine):
    metadata.create_all(engine)
