import hashlib
import math
import secrets
import base64
from datetime import datetime, timedelta
import string

import jose
from jose import jwt
from fastapi import Response, Request
from fastapi import HTTPException
from sqlalchemy import select, update, or_

from src.auth.schemas import UserRead
from src.config import SITE_NAME, ALGORITHM, SECRET_AUTH, ACCESS_TOKEN_EXPIRE_MINUTES
from src.session import async_session
from src.auth.schemas import UserCreate, UserResponse, UserChangePass
from src.auth.models import User


async def create_access_token(user_id: int) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {'exp': expires_delta, 'sub': str(user_id)}
    encoded_jwt = jwt.encode(to_encode, SECRET_AUTH, ALGORITHM)

    return encoded_jwt


class Validator:

    CHARS = string.digits + string.ascii_letters

    @staticmethod
    async def force_bytes(s: str, encoding: str = 'utf-8') -> bytes:
        return str(s).encode(encoding)

    async def pbkdf2(self, password: str, salt: str, iterations: int) -> bytes:
        password = await self.force_bytes(password)
        salt = await self.force_bytes(salt)

        return hashlib.pbkdf2_hmac(hashlib.sha256().name, password, salt, iterations)

    async def compare_passwords(self, password_1: str, password_2: str) -> bool:
        pass_1 = await self.force_bytes(password_1)
        pass_2 = await self.force_bytes(password_2)

        return secrets.compare_digest(pass_1, pass_2)

    async def salt(self) -> str:
        char_count = math.ceil(128 / math.log2(len(self.CHARS)))
        return ''.join(secrets.choice(self.CHARS) for _ in range(char_count))

    async def encode(self, password: str, salt: str = None) -> str:
        iterations = 720000
        salt = salt or await self.salt()
        hash = await self.pbkdf2(password, salt, iterations)
        hash = base64.b64encode(hash).decode('ascii').strip()

        return f'pbkdf2_sha256${iterations}${salt}${hash}'

    @staticmethod
    async def decode(encoded: str) -> dict:
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        return {
            'algorithm': algorithm,
            'hash': hash,
            'iterations': int(iterations),
            'salt': salt,
        }

    async def validate_user(self, user: UserRead) -> User:
        async with async_session() as session:
            query = select(User).where(User.username == user.username)
            result_user = await session.scalar(query)

            if not result_user:
                raise HTTPException(
                    status_code=404,
                    detail='Username does not exists'
                )

            decoded = await self.decode(result_user.password)
            encoded = await self.encode(user.password, decoded['salt'])
            compare = await self.compare_passwords(result_user.password, encoded)

            if not compare:
                raise HTTPException(
                    status_code=422,
                    detail='Incorrect Username or Password'
                )

            return result_user


class AuthORM(Validator):

    async def set_user(self, user: UserCreate) -> UserResponse:
        async with async_session() as session:
            query = select(User).where(
                or_(User.username == user.username, User.email == user.email)
            )
            exists_user = await session.scalar(query)

            if exists_user:
                if exists_user.username == user.username:
                    raise HTTPException(
                        status_code=422,
                        detail='User with this Username already exists'
                    )
                if exists_user.email == user.email:
                    raise HTTPException(
                        status_code=422,
                        detail='User with this Email already exists'
                    )

            user.password = await self.encode(user.password)
            result = User(
                **user.model_dump(exclude={'confirm_password'}),
                date_joined=datetime.utcnow()
            )
            session.add(result)
            await session.flush()
            response = UserResponse(**result.as_dict())
            await session.commit()

            return response

    @staticmethod
    async def get_user(user_id: int) -> User:
        async with async_session() as session:
            query = select(User).where(User.id == user_id)
            result_user = await session.scalar(query)

            if not result_user:
                raise HTTPException(
                    status_code=404,
                    detail='User does not exists'
                )

            return result_user

    async def change_password(
            self, data: UserChangePass, user: User
    ):

        decoded = await self.decode(user.password)
        encoded = await self.encode(data.current_password, decoded['salt'])
        compare = await self.compare_passwords(user.password, encoded)

        if not compare:
            raise HTTPException(
                status_code=422,
                detail='Incorrect Password'
            )
        encoded_new_password = await self.encode(data.new_password)
        async with async_session() as session:
            await session.execute(
                update(User).values(password=encoded_new_password).where(
                    User.id == user.id
                )
            )
            await session.commit()

    @staticmethod
    async def update_last_login(user: User):
        async with async_session() as session:
            await session.execute(
                update(User).values(last_login=datetime.utcnow()).where(
                    User.id == user.id
                )
            )
            await session.commit()


class Secure(User, AuthORM):

    def __init__(self, role: str = 'User'):
        self.role = role

    async def __call__(self, request: Request, response: Response) -> User:
        auth_exception = HTTPException(
            status_code=403,
            detail='Not authorized'
        )

        if SITE_NAME not in request.cookies:
            raise auth_exception
        try:
            token = request.cookies.get(SITE_NAME)
            decoded_token = jwt.decode(token, SECRET_AUTH, algorithms=ALGORITHM)
            user_id = int(decoded_token.get('sub'))
            user = await self.get_user(user_id)

            if self.role == 'Admin' and not user.is_superuser:
                raise HTTPException(
                    status_code=403,
                    detail='Not enough permissions'
                )

            return user

        except jose.ExpiredSignatureError:
            response.delete_cookie(SITE_NAME)
            raise auth_exception


get_current_user = Secure()
admin = Secure('Admin')
validator = Validator()
auth = AuthORM()

