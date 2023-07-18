import os


CACHE_HOST = os.getenv("CACHE_HOST", "localhost")
CACHE_PORT = os.getenv("CACHE_PORT", "9000")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

PROD = os.getenv("PROD")
TESTING = os.getenv("TESTING")

if TESTING:
    DB_NAME = "test_ylab_menu"
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{TESTING}/{DB_NAME}"
    REDIS_URL = "redis://redis"
    RABBITMQ_URL = "pyamqp://rmuser:rmpassword@rabbit/rabbit_prod"
elif PROD:
    DB_NAME = "ylab_menu"
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{PROD}/{DB_NAME}"
    REDIS_URL = "redis://redis"
    RABBITMQ_URL = "pyamqp://rmuser:rmpassword@rabbit/rabbit_prod"
else:
    DB_NAME = "ylab_menu"
    DATABASE_URL = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    REDIS_URL = f"redis://{CACHE_HOST}:{CACHE_PORT}"
    RABBITMQ_URL = "pyamqp://rmuser:rmpassword@localhost:5672/rabbit_dev"
