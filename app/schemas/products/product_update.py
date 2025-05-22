from pydantic import BaseModel
from datetime import date
from typing import Optional


class ProductUpdate(BaseModel):
    description: Optional[str] = None
    price: Optional[float] = None
    section: Optional[str] = None
    stock: Optional[int] = None
    valid_until: Optional[date] = None
    available: Optional[bool] = None

