from databases import Database
from sqlalchemy import MetaData, create_engine

from core.config import DATABASE_URL

database = Database(DATABASE_URL)
metadate = MetaData()
engine = create_engine(
    DATABASE_URL,
)
