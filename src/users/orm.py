from sqlalchemy import select, delete
from fastapi.encoders import jsonable_encoder

from src.session import async_session
from src.auth.models import User


class UsersORM:

    @staticmethod
    async def get_users(limit: int, offset: int) -> list:
        async with async_session() as session:

            query = select(User).limit(limit).offset(offset)
            resp = await session.execute(query)
            result = jsonable_encoder(resp.scalars().all())
            for item in result:
                del item['hashed_password']

            return result

    @staticmethod
    async def delete_user(user: User):
        async with async_session() as session:
            stmt = delete(User).where(User.id == user.id)
            await session.execute(stmt)
            await session.commit()


users = UsersORM()
