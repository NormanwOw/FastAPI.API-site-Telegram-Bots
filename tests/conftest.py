from typing import AsyncGenerator

import pytest
import asyncio

from httpx import AsyncClient
from sqlalchemy import NullPool, update, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.session import Base
from src.main import app
from src.session import get_async_session
from src.auth.models import User
from src.ordering.models import Order

from config import DATABASE_TEST, USER

engine_test = create_async_engine(DATABASE_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session

Base.metadata.bind = engine_test


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture
async def set_admin():
    async with engine_test.begin() as conn:
        stmt = update(User).where(User.email == USER).values(is_superuser=True, is_verified=True)

        await conn.execute(stmt)
        await conn.commit()


@pytest.fixture
async def mock_order_id():
    async with engine_test.begin() as conn:
        stmt = "UPDATE public.\"order\" SET order_id=123123 WHERE email='normjkeee@vk.com'"

        await conn.execute(text(stmt))
        await conn.commit()
