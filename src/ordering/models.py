from sqlalchemy import Integer, String, TIMESTAMP, Boolean, Column

from ..database import Base


class Order(Base):
    __tablename__ = 'order'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, nullable=False)
    phone_number: str = Column(String, nullable=False)
    bot_shop: bool = Column(Boolean, nullable=False)
    admin_panel: bool = Column(Boolean, nullable=False)
    database: bool = Column(Boolean, nullable=False)
    total_price: int = Column(Integer, nullable=False)
    date: TIMESTAMP = Column(TIMESTAMP, nullable=False)
