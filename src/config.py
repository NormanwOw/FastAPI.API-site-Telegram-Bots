import os
from dotenv import load_dotenv, find_dotenv

from redis import asyncio as aioredis

load_dotenv(find_dotenv())

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')

SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

redis = aioredis.from_url('redis://localhost', encoding='utf8', decode_responses=True)

SECRET = os.environ.get('SECRET')
SECRET_AUTH = os.environ.get('SECRET_AUTH')

VERSION = 'v1'
