from datetime import datetime

from sqlalchemy import BigInteger, Integer, String, TIMESTAMP, Column, ForeignKey

from src.session import Base


class Order(Base):
    __tablename__ = 'order'

    id: int = Column(BigInteger, primary_key=True)
    order_id: int = Column(Integer, nullable=False)
    phone_number: str = Column(String, nullable=False)
    bot_shop: int = Column(Integer, nullable=False)
    admin_panel: int = Column(Integer, nullable=False)
    database: int = Column(Integer, nullable=False)
    total_price: int = Column(Integer, nullable=False)
    date: TIMESTAMP = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    status: str = Column(String, nullable=False, default='Оформлен')
    user_id: int = Column(BigInteger, ForeignKey('user.id'), nullable=False)


class Product(Base):
    __tablename__ = 'product'

    id: int = Column(BigInteger, primary_key=True)
    name: str = Column(String, nullable=False)
    price: int = Column(Integer, nullable=False)
    title: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True, default='...')
