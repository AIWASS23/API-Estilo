from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.orders.order import OrderOut, OrderUpdate
from app.schemas.orders.order_item import OrderCreate
from app.models.user import User
from app.services.service import get_current_user, admin_required

order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.get("/", response_model=List[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    section: Optional[str] = Query(None),
    id_order: Optional[int] = Query(None),
    status: Optional[OrderStatus] = Query(None),
    client: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Order)

    if id_order:
        query = query.filter(Order.id == id_order)
    if status:
        query = query.filter(Order.status == status)
    if client:
        query = query.filter(Order.client.ilike(f"%{client}%"))
    if start_date and end_date:
        query = query.filter(Order.created_at.between(start_date, end_date))

    orders = query.all()
    return orders


@order_router.post("/", response_model=OrderOut)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_order = Order(client=order.client)

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produto ID {item.product_id} não encontrado.")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para produto {product.description}.")

        product.stock -= item.quantity
        db.add(OrderItem(order=new_order, product_id=product.id, quantity=item.quantity))

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@order_router.get("/{id}", response_model=OrderOut)
def get_order(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return order


@order_router.put("/{id}", response_model=OrderOut)
def update_order(
    id: int,
    update_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    order.status = update_data.status
    db.commit()
    db.refresh(order)
    return order


@order_router.delete("/{id}")
def delete_order(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    db.delete(order)
    db.commit()
    return {"message": "Pedido deletado com sucesso"}
