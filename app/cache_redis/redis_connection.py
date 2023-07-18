import aioredis

from core.config import REDIS_URL

redis = aioredis.from_url(REDIS_URL)
