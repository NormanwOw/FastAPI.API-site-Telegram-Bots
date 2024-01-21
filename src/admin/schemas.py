from datetime import datetime
from typing import Union

from pydantic import BaseModel, EmailStr


class AdmUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: Union[str, None]
    last_name: Union[str, None]
    is_superuser: bool
    is_staff: bool
    is_active: bool
    last_login: Union[datetime, None]
