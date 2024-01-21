from fastapi import APIRouter, Depends, Response

from src.auth.secure import get_current_user, Secure
from src.config import VERSION, SITE_NAME
from src.auth.schemas import UserResponse
from src.users.schemas import UserUpdate
from src.users.orm import users
from src import utils

router = APIRouter(
    prefix=f'/api/{VERSION}/users',
    tags=['Users']
)


@router.get('/me', response_model=UserResponse)
async def me(user: Secure = Depends(get_current_user)):
    return user


@router.patch('/')
async def update_me(data: UserUpdate, user: Secure = Depends(get_current_user)):
    await users.update_user(data, user)
    return utils.SUCCESS


@router.delete('/', status_code=204)
async def delete_me(response: Response, user: Secure = Depends(get_current_user)):
    await users.delete_user(user)
    response.delete_cookie(SITE_NAME)

    return utils.SUCCESS
