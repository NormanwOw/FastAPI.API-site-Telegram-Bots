from fastapi import APIRouter

from src.config import VERSION

router = APIRouter(
    prefix=f'/api/{VERSION}/users',
    tags=['Users']
)


