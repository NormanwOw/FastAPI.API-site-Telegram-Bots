import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

SECRET = os.environ.get('SECRET')
SECRET_AUTH = os.environ.get('SECRET_AUTH')

VERSION = 'v1'
