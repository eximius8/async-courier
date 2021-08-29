from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db.models import Delivery

class DeliveryDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_delivery(self, status: str):
        new_delivery = Delivery(status=status)
        self.db_session.add(new_delivery)
        await self.db_session.flush()

    async def get_all_deliveries(self) -> List[Delivery]:
        q = await self.db_session.execute(select(Delivery).order_by(Delivery.id))
        return q.scalars().all()

    async def update_delivery(self, delivery_id: int, status: Optional[str]):
        q = update(Delivery).where(Delivery.id == delivery_id)
        if status and status in ['processed', 'inprogress', 'delivered']:
            q = q.values(status=status)
        q.execution_options(synchronize_session="fetch")
        await  self.db_session.execute(q)
