from sqlalchemy import select, delete
from fastapi.exceptions import HTTPException

from src.session import async_session
from src.auth.models import User


class AdminORM:

    # @staticmethod
    # async def get_user(user_id: int, user: User) -> UserResponse:
    #
    #     async with async_session() as session:
    #         result = await session.scalar(
    #             select(User).where(User.id == user_id)
    #         )
    #         response_user = UserResponse()
    #
    #         return result

    @staticmethod
    async def delete_user(user: User):
        async with async_session() as session:
            if user.is_superuser or user.is_staff:
                stmt = delete(User).where(User.id == user.id)
            await session.execute(stmt)
            await session.commit()

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


adm = AdminORM()
