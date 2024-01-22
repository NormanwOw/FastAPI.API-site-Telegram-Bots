from datetime import datetime
from typing import Union

from pydantic import BaseModel, EmailStr


class AdmUserUpdate(BaseModel):
    username: str
    email: EmailStr
    first_name: Union[str, None]
    last_name: Union[str, None]
    is_superuser: bool
    is_staff: bool
    is_active: bool


class AdmUserResponse(AdmUserUpdate):
    id: int
    last_login: Union[datetime, None]
    date_joined: datetime
