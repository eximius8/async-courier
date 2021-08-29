from sqlalchemy import Column, Integer, String

from db.config import Base

class Delivery(Base):
    __tablename__ = 'delivery'

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
