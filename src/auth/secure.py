from datetime import datetime, timedelta

import jose
from jose import jwt
from fastapi import Response, Request, HTTPException

from src.auth.models import User
from src.auth.orm import auth
from src.config import SITE_NAME, ALGORITHM, SECRET_AUTH

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(user_id: int) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {'exp': expires_delta, 'sub': str(user_id)}
    encoded_jwt = jwt.encode(to_encode, SECRET_AUTH, ALGORITHM)

    return encoded_jwt


class Secure(User):

    async def __call__(self, request: Request, response: Response) -> User:
        auth_exception = HTTPException(status_code=403, detail='Not authorized')

        if SITE_NAME not in request.cookies:
            raise auth_exception
        try:
            token = request.cookies.get(SITE_NAME)
            decoded_token = jwt.decode(token, SECRET_AUTH, algorithms=ALGORITHM)
            user_id = int(decoded_token.get('sub'))
            user = await auth.get_user(user_id)
            return user

        except jose.ExpiredSignatureError:
            response.delete_cookie(SITE_NAME)
            raise auth_exception


get_current_user = Secure()
