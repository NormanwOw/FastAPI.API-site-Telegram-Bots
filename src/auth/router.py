from fastapi import APIRouter, Response, Depends

from src.auth.secure import create_access_token, validator, auth, get_current_user
from src.config import VERSION
from src.auth.schemas import UserRead, UserResponse, UserCreate
from src.config import SITE_NAME
from src import utils

router = APIRouter(
    prefix=f'/api/{VERSION}/auth',
    tags=['Auth']
)


@router.post('/login')
async def login(user: UserRead, response: Response):
    valid_user = await validator.validate_user(user)
    token = await create_access_token(valid_user.id)
    response.set_cookie(key=SITE_NAME, value=token)

    return utils.SUCCESS


@router.post('/logout', dependencies=[Depends(get_current_user)])
async def logout(response: Response):
    response.delete_cookie(SITE_NAME)

    return utils.SUCCESS


@router.post('/registration', response_model=UserResponse, status_code=201)
async def registration(user: UserCreate):
    response_user = await auth.set_user(user)

    return response_user
