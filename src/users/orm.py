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
