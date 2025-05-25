from pydantic import BaseModel
from typing import List


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    client: str
    items: List[OrderItemCreate]


class OrderItemOut(OrderItemCreate):
    id: int
