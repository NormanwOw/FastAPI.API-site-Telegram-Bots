from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.auth.auth_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.ordering.router import router as order_router
from src.users.router import router as users_router
from src.config import VERSION, redis
from src.database import Database, orders

app = FastAPI(
    title='API Telegram bots',
    version='1.0.0',
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=f'/api/{VERSION}/auth',
    tags=['Auth'],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=f'/api/{VERSION}/auth',
    tags=['Auth'],
)

app.include_router(
    users_router
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix=f'/api/{VERSION}/users',
    tags=['Users'],
)

app.include_router(
    order_router
)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):

    details = exc.errors()[0]
    if details['type'] == 'string_pattern_mismatch':
        details['msg'] = "Phone should match '+7(9##)#######'"
        del details['ctx']
        del details['url']

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": details},
    )


@app.on_event('startup')
async def startup_event():
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    orders.update(await Database.get_all_order_id())
