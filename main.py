from logging import debug
from typing import List
from sqlalchemy.sql.expression import join
from fastapi.encoders import jsonable_encoder

import uvicorn

import databases
import sqlalchemy
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

deliveries = sqlalchemy.Table(
    "deliveries",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("status", sqlalchemy.String),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)



class DeliveryIn(BaseModel):
    status: str


class Delivery(BaseModel):
    id: int
    status: str
    

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/deliveries/", response_model=List[Delivery])
async def read_deliveries():
    query = deliveries.select()
    return await database.fetch_all(query)


@app.post("/deliveries/", response_model=Delivery)
async def create_note(delivery: DeliveryIn):
    allowed_statuses = ['обрабатывается', 'выполняется', 'доставлено']
    if delivery.status in allowed_statuses:
        query = deliveries.insert().values(status=delivery.status)
        last_record_id = await database.execute(query)
        return {**delivery.dict(), "id": last_record_id}
    raise HTTPException(status_code=404, detail="Неверный статус, статус может быть: " 
                                                + ", ".join(allowed_statuses))
 

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='127.0.0.1', debug=True)
