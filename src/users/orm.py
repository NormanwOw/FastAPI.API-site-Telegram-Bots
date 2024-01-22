from string import ascii_letters
from typing import Union

from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from src.session import async_session
from src.auth.models import User
from src.users.schemas import UserUpdate
from src.admin.schemas import AdmUserUpdate


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
    async def delete_user(user: User, user_id: int = None):
        async with async_session() as session:
            result_id = user_id or user.id
            await session.execute(
                delete(User).where(User.id == result_id)
            )
            await session.commit()

    @staticmethod
    async def update_user(
            user: User,
            user_id: int = None,
            schema: Union[UserUpdate, AdmUserUpdate] = None
    ):
        for char in schema.first_name + schema.last_name:
            if char not in ascii_letters + '-':
                raise HTTPException(
                    status_code=422,
                    detail='Incorrect First-name or Last-name'
                )
        result_user_id = user_id or user.id

        async with async_session() as session:
            try:
                await session.execute(
                    update(User).values(**schema.model_dump()).where(
                        User.id == result_user_id
                    )
                )
                await session.commit()
            except IntegrityError as e:
                if '(username)' in str(e):
                    msg = 'username'
                elif '(email)' in str(e):
                    msg = 'email'
                raise HTTPException(
                    status_code=422,
                    detail=f'User with this {msg} already exists'
                )


users = UsersORM()
