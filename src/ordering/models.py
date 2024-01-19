from datetime import datetime

from sqlalchemy import BigInteger, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.session import Base


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    bot_shop: Mapped[int] = mapped_column(Integer, nullable=False)
    admin_panel: Mapped[int] = mapped_column(Integer, nullable=False)
    database: Mapped[int] = mapped_column(Integer, nullable=False)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.utcnow
    )
    status: Mapped[str] = mapped_column(String, nullable=False, default='Оформлен')
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('user.id'), nullable=False
    )


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True, default='...')
