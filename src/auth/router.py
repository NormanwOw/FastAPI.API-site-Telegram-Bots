from fastapi import APIRouter, Response, Depends

from src.auth.secure import create_access_token, validator, auth, get_current_user, Secure
from src.config import VERSION
from src.auth.schemas import UserRead, UserResponse, UserCreate, UserChangePass
from src.config import SITE_NAME
from src import utils

router = APIRouter(
    prefix=f'/api/{VERSION}/auth',
    tags=['Auth']
)


@router.post('/login', status_code=200)
async def login(user: UserRead, response: Response):
    valid_user = await validator.validate_user(user)
    token = await create_access_token(valid_user.id)
    await auth.update_last_login(valid_user)
    response.set_cookie(key=SITE_NAME, value=token)

    return utils.SUCCESS


@router.post('/logout', dependencies=[Depends(get_current_user)], status_code=200)
async def logout(response: Response):
    response.delete_cookie(SITE_NAME)
    return utils.SUCCESS


@router.post('/registration', response_model=UserResponse, status_code=201)
async def registration(user: UserCreate):
    response_user = await auth.set_user(user)
    return response_user


@router.post('/change-password', status_code=200)
async def change_password(
        data: UserChangePass,
        user: Secure = Depends(get_current_user)
):
    await auth.change_password(data, user)
    return utils.SUCCESS
