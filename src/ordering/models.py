from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP, Column, ForeignKey

from src.session import Base


class Order(Base):
    __tablename__ = 'order'

    id: int = Column(Integer, primary_key=True)
    order_id: int = Column(Integer, nullable=False)
    user_id: int = Column(Integer, ForeignKey('user.id'), nullable=False)
    phone_number: str = Column(String, nullable=False)
    bot_shop: int = Column(Integer, nullable=False)
    admin_panel: int = Column(Integer, nullable=False)
    database: int = Column(Integer, nullable=False)
    total_price: int = Column(Integer, nullable=False)
    date: TIMESTAMP = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)


class Product(Base):
    __tablename__ = 'product'

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String, nullable=False)
    product: str = Column(String, nullable=False)
    price: int = Column(Integer, nullable=False)
    description: str = Column(String, nullable=True, default='...')
