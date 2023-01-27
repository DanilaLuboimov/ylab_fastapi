from .base import engine, metadate
from .tables import *

metadate.create_all(bind=engine)
