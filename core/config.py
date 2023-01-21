import os

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()


DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

PROD = os.getenv("PROD")
TESTING = os.getenv("TESTING")

if TESTING:
    # Используем отдельную базу данных для тестов
    DB_NAME = "test_ylab_menu"
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{TESTING}/{DB_NAME}"
    )
elif PROD:
    DB_NAME = "ylab_menu"
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{PROD}/{DB_NAME}"
    )
else:
    DB_NAME = "ylab_menu"
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
