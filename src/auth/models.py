from sqlalchemy import BigInteger, String, TIMESTAMP, Boolean, Column

from src.session import Base


class User(Base):
    __tablename__ = 'user'

    id: int = Column(BigInteger, primary_key=True)
    password: str = Column(String, nullable=False)
    last_login: TIMESTAMP = Column(TIMESTAMP, nullable=True)
    is_superuser: bool = Column(Boolean, nullable=False, default=False)
    username: str = Column(String, unique=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    is_staff: bool = Column(Boolean, nullable=False, default=False)
    is_active: bool = Column(Boolean, nullable=False, default=True)
    first_name: str = Column(String, nullable=True)
    last_name: str = Column(String, nullable=True)
