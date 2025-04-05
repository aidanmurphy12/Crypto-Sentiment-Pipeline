from db_utils import get_engine
from models import create_tables

engine = get_engine()
create_tables(engine)

from ingest_data import fetch_and_store_prices
fetch_and_store_prices()
