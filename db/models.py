from sqlalchemy import Column, Integer, String

from db.config import Base, engine

class Delivery(Base):
    __tablename__ = 'delivery'

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

init_models()