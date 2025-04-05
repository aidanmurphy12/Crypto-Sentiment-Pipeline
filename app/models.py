from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, text
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