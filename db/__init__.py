from .tables import *
from .base import metadate, engine

metadate.create_all(bind=engine)
