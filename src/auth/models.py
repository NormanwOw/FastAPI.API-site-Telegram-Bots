from sqlalchemy import BigInteger, String, TIMESTAMP, Boolean
from sqlalchemy.orm import mapped_column, Mapped
from src.session import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    last_login: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
