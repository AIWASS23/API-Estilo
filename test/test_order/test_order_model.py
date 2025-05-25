import pytest
from app.models.product import Product
from app.models.order import Order, OrderItem, OrderStatus


def test_create_order_with_items(db):
    product = Product(
        description="Produto Teste",
        price=99.99,
        barcode="1234567890123",
        section="Geral",
        stock=10
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    order = Order(client="cliente@example.com", status=OrderStatus.pending)
    db.add(order)
    db.commit()
    db.refresh(order)

    item = OrderItem(order_id=order.id, product_id=product.id, quantity=2)
    db.add(item)
    db.commit()
    db.refresh(item)

    assert order.id is not None
    assert item.id is not None
    assert item.order_id == order.id
    assert item.product_id == product.id
    assert item.quantity == 2

    assert order.items[0].product.description == "Produto Teste"


def test_order_status_enum(db):
    order = Order(client="cliente@teste.com", status=OrderStatus.processing)
    db.add(order)
    db.commit()
    db.refresh(order)

    assert order.status == OrderStatus.processing


def test_order_created_at_autoset(db):
    order = Order(client="data@teste.com")
    db.add(order)
    db.commit()
    db.refresh(order)

    assert order.created_at is not None
