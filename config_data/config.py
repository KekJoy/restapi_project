import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
DB_PATH = os.getenv("DB_PATH")
