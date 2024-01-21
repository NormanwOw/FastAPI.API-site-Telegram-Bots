from string import ascii_letters

from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from src.session import async_session
from src.auth.models import User
from src.users.schemas import UserUpdate


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
            if user.is_superuser or user.is_staff:
                stmt = delete(User).where(User.id == user.id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_user(data: UserUpdate, user: User):
        for char in data.first_name + data.last_name:
            if char not in ascii_letters + '-':
                raise HTTPException(
                    status_code=422,
                    detail='Incorrect First-name or Last-name'
                )

        async with async_session() as session:
            try:
                await session.execute(
                    update(User).values(**data.model_dump()).where(User.id == user.id)
                )
                await session.commit()
            except IntegrityError:
                raise HTTPException(
                    status_code=422,
                    detail='User with this email already exists'
                )


users = UsersORM()
