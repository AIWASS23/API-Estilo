from pydantic import BaseModel, conint
from typing import List


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: conint(gt=0)


class OrderCreate(BaseModel):
    client: str
    items: List[OrderItemCreate]


class OrderItemOut(OrderItemCreate):
    id: int
