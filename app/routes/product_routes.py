import os
from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.products.product_base import ProductOut
from app.schemas.products.product_update import ProductUpdate
from app.services.service import get_current_user, admin_required

product_router = APIRouter(prefix="/products", tags=["Products"])


@product_router.get("/", response_model=List[ProductOut])
def list_products(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
        section: Optional[str] = None,
        available: Optional[bool] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        current_user: User = Depends(get_current_user)
):
    query = db.query(Product)
    if section:
        query = query.filter(Product.section.ilike(f"%{section}%"))
    if available is not None:
        query = query.filter(Product.available == available)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    return query.offset(skip).limit(limit).all()


@product_router.post("/", response_model=ProductOut)
def create_product(
        description: str = Form(..., example="Tênis Esportivo"),
        price: float = Form(..., example=199.99),
        barcode: str = Form(..., example="7896543219870"),
        section: str = Form(..., example="Calçados"),
        stock: int = Form(..., example=50),
        valid_until: str = Form(None, example="2025-12-31"),
        image: UploadFile = File(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)

):
    if db.query(Product).filter_by(barcode=barcode).first():
        raise HTTPException(status_code=400, detail="Código de barras já existe.")

    image_url = None
    if image:
        file_ext = image.filename.split('.')[-1]
        filename = f"{uuid4().hex}.{file_ext}"
        file_path = os.path.join("static", "images", filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as buffer:
            buffer.write(image.file.read())
        image_url = f"/static/images/{filename}"

    new_product = Product(
        description=description,
        price=price,
        barcode=barcode,
        section=section,
        stock=stock,
        valid_until=datetime.strptime(valid_until, "%Y-%m-%d").date() if valid_until else None,
        image_url=image_url
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@product_router.get("/{id}", response_model=ProductOut)
def get_product(
        id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    product = db.query(Product).get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return product


@product_router.put("/{id}", response_model=ProductOut)
def update_product(
        id: int, updates:
        ProductUpdate, db: Session = Depends(get_db),
        current_user: User = Depends(admin_required)
):
    product = db.query(Product).get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    for attr, value in updates.dict(exclude_unset=True).items():
        setattr(product, attr, value)

    db.commit()
    db.refresh(product)
    return product


@product_router.delete("/{id}")
def delete_product(
        id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(admin_required)
):
    product = db.query(Product).get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    db.delete(product)
    db.commit()
    return {"message": "Produto deletado com sucesso"}
