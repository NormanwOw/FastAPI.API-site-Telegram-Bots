from datetime import datetime

from sqlalchemy import BigInteger, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.session import Base
from src.ordering.models import Order


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    password: Mapped[str] = mapped_column(nullable=False)
    last_login: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_staff: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)

    order = relationship('Order', back_populates='user')

    def as_dict(self):
        return self.__dict__
