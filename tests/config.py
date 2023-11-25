import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


DB_HOST_TEST = os.environ.get('DB_HOST_TEST')
DB_PORT_TEST = os.environ.get('DB_PORT_TEST')
DB_USER_TEST = os.environ.get('DB_USER_TEST')
DB_PASS_TEST = os.environ.get('DB_PASS_TEST')
DB_NAME_TEST = os.environ.get('DB_NAME_TEST')

USER = os.environ.get('USER')

DATABASE_TEST = f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@' \
                f'{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'


