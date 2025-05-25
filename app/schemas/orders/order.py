from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum
from app.schemas.orders.order_item import OrderItemOut


class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    cancelled = "cancelled"


class OrderOut(BaseModel):
    id: int
    client: str
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        orm_mode = True


class OrderUpdate(BaseModel):
    status: OrderStatus
