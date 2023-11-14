from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.auth.auth_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from .ordering.router import router as order_router

app = FastAPI(
    title='API Telegram bots'
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
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
