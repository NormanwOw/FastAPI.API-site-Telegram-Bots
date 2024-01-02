from datetime import datetime
from enum import Enum

from sqlalchemy import Integer, Boolean, String, \
    TIMESTAMP, Column, ForeignKey, Enum as SQLAlchemyEnum

from src.session import Base


class OrderStatus(Enum):
    ordered = 'Оформлен'
    in_progress = 'В работе'
    completed = 'Исполнен'


class Order(Base):
    __tablename__ = 'order'

    id: int = Column(Integer, primary_key=True)
    order_id: int = Column(Integer, nullable=False)
    user_id: int = Column(Integer, ForeignKey('user.id'), nullable=False)
    phone_number: str = Column(String, nullable=False)
    bot_shop: int = Column(Boolean, nullable=False)
    admin_panel: int = Column(Boolean, nullable=False)
    database: int = Column(Boolean, nullable=False)
    total_price: int = Column(Integer, nullable=False)
    date: TIMESTAMP = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    status = Column(
        SQLAlchemyEnum(OrderStatus),
        default=OrderStatus.ordered
    )


class Product(Base):
    __tablename__ = 'product'

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String, nullable=False)
    product: str = Column(String, nullable=False)
    price: int = Column(Integer, nullable=False)
    description: str = Column(String, nullable=True, default='...')
