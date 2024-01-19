import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.auth.router import router as auth_router
from src.ordering.router import router as order_router
from src.users.router import router as users_router
from src.config import VERSION, redis
from src.database import Database, orders

app = FastAPI(
    title='API Telegram bots',
    version='1.0.0',
    docs_url=f'/api/{VERSION}/docs',
    openapi_url=f'/api/{VERSION}/openapi.json',
    redoc_url=None
)

app.include_router(
    auth_router
)

app.include_router(
    users_router
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
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    orders.update(await Database.get_all_order_id())


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=7000)
