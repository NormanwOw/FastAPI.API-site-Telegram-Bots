from sqlalchemy import select, delete
from fastapi.encoders import jsonable_encoder

from src.database import async_session
from src.auth.models import User


class UsersORM:

    @classmethod
    async def get_users(cls, limit: int, offset: int) -> list:
        async with async_session() as session:

            query = select(User).limit(limit).offset(offset)
            resp = await session.execute(query)
            result = jsonable_encoder([item[0] for item in resp.all()])
            for item in result:
                del item['hashed_password']

            return result

    @classmethod
    async def get_user(cls, user_id: int) -> dict:
        async with async_session() as session:

            query = select(User).where(User.id == user_id)
            resp = await session.execute(query)
            result = jsonable_encoder(resp.scalar())
            del result['hashed_password']

            return result

    @classmethod
    async def delete_user(cls, user_id: int) -> None:
        async with async_session() as session:
            stmt = delete(User).where(User.id == user_id)
            await session.execute(stmt)
            await session.commit()
