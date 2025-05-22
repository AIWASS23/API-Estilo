from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    barcode = Column(String, unique=True, index=True, nullable=False)
    section = Column(String, nullable=False)
    stock = Column(Integer, default=0)
    valid_until = Column(Date, nullable=True)
    available = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)
