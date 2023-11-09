from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP, Boolean, Column
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from ..database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    id: int = Column(Integer, primary_key=True)
    phone_number: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    registered = Column(TIMESTAMP, default=datetime.utcnow)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
