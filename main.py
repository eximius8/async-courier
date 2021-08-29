import uvicorn
from fastapi import FastAPI

from typing import List

from db.config import async_session
from db.delivery_dal import DeliveryDAL
from db.models import Delivery



app = FastAPI()


@app.post("/deliveries")
async def create_delivery(status: str):
    async with async_session() as session:
        async with session.begin():
            delivery_dal = DeliveryDAL(session)
            return await delivery_dal.create_delivery(status)

@app.get("/deliveries")
async def get_all_deliveries() -> List[Delivery]:
    async with async_session() as session:
        async with session.begin():
            delivery_dal = DeliveryDAL(session)
            return await delivery_dal.get_all_deliveries()


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='127.0.0.1')