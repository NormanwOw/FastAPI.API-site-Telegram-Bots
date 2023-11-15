from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.auth.models import User
from src.auth.auth_config import admin
from src.users.orm import UsersORM
from src.config import VERSION

router = APIRouter(
    prefix=f'/api/{VERSION}/users',
    tags=['Users']
)


@router.get('/')
async def get_users(limit: int, offset: int, user: User = Depends(admin)):
    result = await UsersORM.get_users(limit, offset)
    return JSONResponse(result, status_code=200)
