import asyncio
from typing import AsyncGenerator
from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import insert

from src.session import get_async_session, Base
from src.auth.models import User
from tests.config import (DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST,
                          DB_USER_TEST)
from src.main import app

# DATABASE
DATABASE_URL_TEST = f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
async def authorized_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        await ac.post('api/v1/auth/registration', json={
            'username': 'username',
            'email': 'user@example.com',
            'password': 'stringstring',
            'confirm_password': 'stringstring'
        })

        await ac.post('api/v1/auth/login', json={
            'username': 'username',
            'password': 'stringstring'
        })
        yield ac


@pytest.fixture(scope='session')
async def admin() -> AsyncGenerator[AsyncClient, None]:
    async with engine_test.begin() as conn:
        await conn.execute(
            insert(User).values(
                (10, 'pbkdf2_sha256$720000$IVtwOaY2WoUoR6ks39yRyT$lRda490enZstOAkqdFD15DP'
                    'SafQn2XyEWjtpMcZdfcg=', datetime.utcnow(),
                 True, 'admin', 'admin@example.com', True, True, None, None,
                 datetime.utcnow())
            )
        )

    async with AsyncClient(app=app, base_url='http://test') as ac:
        await ac.post('api/v1/auth/login', json={
            'username': 'admin',
            'password': 'stringstring'
        })

        yield ac
