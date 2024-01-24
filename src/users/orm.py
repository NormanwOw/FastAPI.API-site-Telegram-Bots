from typing import Union

from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException

from src.session import async_session
from src.auth.models import User
from src.users.schemas import UserUpdate, AdmUserUpdate


class UsersORM:

    @staticmethod
    async def get_users(limit: int, offset: int) -> list:
        if limit < 1 or offset < 0:
            raise HTTPException(
                detail='incorrect values [limit > 0 and offset >= 0]',
                status_code=422
            )

        async with async_session() as session:
            result = await session.scalars(
                select(User).limit(limit).offset(offset)
            )
            users_list = result.all()

        return users_list

    @staticmethod
    async def update_user(
            user: User,
            user_id: int = None,
            schema: Union[UserUpdate, AdmUserUpdate] = None
    ):
        result_user_id = user_id or user.id

        async with async_session() as session:
            user_dict = schema.model_dump()

            result_dict = {}
            for item in user_dict:
                if user_dict[item]:
                    result_dict[item] = user_dict[item]
            try:
                await session.execute(
                    update(User).values(**result_dict).where(
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

    @staticmethod
    async def delete_user(user: User, user_id: int = None):
        async with async_session() as session:
            result_id = user_id or user.id
            await session.execute(
                delete(User).where(User.id == result_id)
            )
            await session.commit()


users = UsersORM()
