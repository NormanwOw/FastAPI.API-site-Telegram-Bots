from sqlalchemy import select, delete

from src.session import async_session
from src.auth.models import User
from src.auth.schemas import UserResponse


class AdminORM:

    @staticmethod
    async def get_user(user_id: int, user: User) -> UserResponse:

        async with async_session() as session:
            result = await session.scalar(
                select(User).where(User.id == user_id)
            )
            response_user = UserResponse()

            return result

    @staticmethod
    async def delete_user(user: User):
        async with async_session() as session:
            if user.is_superuser or user.is_staff:
                stmt = delete(User).where(User.id == user.id)
            await session.execute(stmt)
            await session.commit()
