from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from src.session import Base


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    def as_dict(self):
        return self.__dict__
