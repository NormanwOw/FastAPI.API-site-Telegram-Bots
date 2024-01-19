from fastapi import HTTPException
from sqlalchemy import insert, select, or_, and_

from src.session import async_session
from src.auth.schemas import UserCreate, UserRead
from src.auth.models import User


class AuthORM:

    @staticmethod
    async def set_user(user: UserCreate):
        if user.password != user.confirm_password:
            raise HTTPException(
                status_code=403,
                detail='Password is not equal Confirm_password'
            )

        async with async_session() as session:
            query = select(User).where(
                or_(User.username == user.username, User.email == user.email)
            )
            res = await session.execute(query)
            exists_user = res.scalar()

            if exists_user:
                if exists_user.username == user.username:
                    raise HTTPException(
                        status_code=403,
                        detail='User with this Username already exists'
                    )

                if exists_user.email == user.email:
                    raise HTTPException(
                        status_code=403,
                        detail='User with this Email already exists'
                    )

            stmt = insert(User).values(
                **user.model_dump(exclude={'confirm_password'})
            ).returning(User)
            await session.execute(stmt)
            await session.commit()

            query = select(User).where(User.username == user.username)
            result_user = await session.execute(query)

            return result_user.scalar()

    @staticmethod
    async def validate_user(user: UserRead) -> User:
        async with async_session() as session:
            query = select(User).where(
                and_(User.username == user.username, User.password == user.password)
            )
            response_user = await session.execute(query)
            result_user = response_user.scalar()

            if not result_user:
                raise HTTPException(
                    status_code=403,
                    detail='Incorrect Username or Password'
                )

            return result_user

    @staticmethod
    async def get_user(user_id: int) -> User:
        async with async_session() as session:
            query = select(User).where(User.id == user_id)
            result_user = await session.execute(query)

            return result_user.scalar()


auth = AuthORM()
