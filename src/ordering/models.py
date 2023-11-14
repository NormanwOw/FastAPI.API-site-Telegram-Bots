from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP, Boolean, Column

from src.database import Base


class Order(Base):
    __tablename__ = 'order'

    id: int = Column(Integer, primary_key=True)
    order_id: int = Column(Integer, nullable=False)
    email: str = Column(String, nullable=False)
    phone_number: str = Column(String, nullable=False)
    bot_shop: bool = Column(Boolean, nullable=False, default=True)
    admin_panel: bool = Column(Boolean, nullable=False)
    database: bool = Column(Boolean, nullable=False)
    total_price: int = Column(Integer, nullable=False)
    date: TIMESTAMP = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
