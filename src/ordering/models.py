from datetime import datetime

from sqlalchemy import BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.session import Base


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    bot_shop: Mapped[int] = mapped_column(nullable=False)
    admin_panel: Mapped[int] = mapped_column(nullable=False)
    database: Mapped[int] = mapped_column(nullable=False)
    total_price: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.utcnow
    )
    status: Mapped[str] = mapped_column(nullable=False, default='Оформлен')
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('user.id'), nullable=False
    )

    user = relationship('User', back_populates='order')

    def as_dict(self):
        return self.__dict__


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True, default='...')
