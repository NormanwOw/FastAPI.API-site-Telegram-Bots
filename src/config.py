import os
from dotenv import load_dotenv, find_dotenv

from alembic.config import Config
from redis import asyncio as aioredis

load_dotenv(find_dotenv())


DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

redis = aioredis.from_url(
    f'redis://{REDIS_HOST}:{REDIS_PORT}',
    encoding='utf8',
    decode_responses=True
)

SECRET = os.environ.get('SECRET')
SECRET_AUTH = os.environ.get('SECRET_AUTH')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

VERSION = 'v1'
SITE_NAME = 'site-telegram-bots'


alembic_cfg = Config()
alembic_cfg.set_main_option('sqlalchemy.url', DATABASE_URL)
