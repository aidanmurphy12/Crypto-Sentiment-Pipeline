# setup_db.py
from models import create_tables
from db_utils import get_engine

if __name__ == "__main__":
    engine = get_engine()
    create_tables(engine)
    print("Tables created successfully.")
