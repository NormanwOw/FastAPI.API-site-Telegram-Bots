from fastapi import APIRouter, Depends, Response

from src.auth.secure import get_current_user, Secure
from src.config import VERSION, SITE_NAME
from src.auth.schemas import UserResponse
from src.users.orm import users
from src import utils

router = APIRouter(
    prefix=f'/api/{VERSION}/users',
    tags=['Users']
)


@router.get('/me', response_model=UserResponse)
async def me(user: Secure = Depends(get_current_user)):
    return user


@router.delete('/', status_code=204)
async def delete(response: Response, user: Secure = Depends(get_current_user)):
    await users.delete_user(user)
    response.delete_cookie(SITE_NAME)

    return utils.SUCCESS
