from db_utils import get_engine
from models import create_tables

engine = get_engine()
create_tables(engine)