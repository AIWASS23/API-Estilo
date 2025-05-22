from pydantic import BaseModel, constr
from datetime import date
from typing import Optional


class ProductBase(BaseModel):
    description: str
    price: float
    barcode: constr(min_length=13, max_length=13, pattern=r'^\d{13}$')
    section: str
    stock: int
    valid_until: Optional[date] = None
    available: Optional[bool] = True


class ProductOut(ProductBase):
    id: int
    image_url: Optional[str] = None

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass

