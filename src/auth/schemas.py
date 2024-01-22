from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class UserChangePass(BaseModel):
    current_password: str
    new_password: str

