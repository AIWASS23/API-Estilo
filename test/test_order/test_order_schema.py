import pytest
from datetime import datetime
from app.schemas.orders.order import OrderOut, OrderUpdate, OrderStatus
from app.schemas.orders.order_item import OrderItemOut, OrderItemCreate, OrderCreate


def test_order_out_schema_valid():
    order_data = {
        "id": 1,
        "client": "cliente@exemplo.com",
        "status": "pending",
        "created_at": datetime.utcnow(),
        "items": [
            {
                "id": 1,
                "order_id": 1,
                "product_id": 10,
                "quantity": 2
            }
        ]
    }

    order = OrderOut(**order_data)
    assert order.id == 1
    assert order.client == "cliente@exemplo.com"
    assert order.status == OrderStatus.pending
    assert isinstance(order.items, list)
    assert isinstance(order.items[0], OrderItemOut)


def test_order_out_schema_invalid_status():
    invalid_data = {
        "id": 1,
        "client": "cliente@exemplo.com",
        "status": "invalid_status",
        "created_at": datetime.utcnow(),
        "items": []
    }

    with pytest.raises(ValueError):
        OrderOut(**invalid_data)


def test_order_update_valid():
    data = {"status": "completed"}
    update = OrderUpdate(**data)
    assert update.status == OrderStatus.completed


def test_order_update_invalid():
    data = {"status": "unknown"}
    with pytest.raises(ValueError):
        OrderUpdate(**data)


def test_order_item_create_valid():
    data = {"product_id": 10, "quantity": 3}
    item = OrderItemCreate(**data)
    assert item.product_id == 10
    assert item.quantity == 3


def test_order_item_create_invalid_missing_field():
    data = {"quantity": 3}
    with pytest.raises(ValueError):
        OrderItemCreate(**data)


def test_order_item_create_invalid_quantity():
    data = {"product_id": 1, "quantity": -2}
    item = OrderItemCreate(**data)
    assert item.quantity == -2


def test_order_create_valid():
    data = {
        "client": "cliente@exemplo.com",
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 1}
        ]
    }
    order = OrderCreate(**data)
    assert order.client == "cliente@exemplo.com"
    assert len(order.items) == 2
    assert isinstance(order.items[0], OrderItemCreate)


def test_order_create_invalid_missing_items():
    data = {"client": "teste"}
    with pytest.raises(ValueError):
        OrderCreate(**data)


def test_order_item_out_valid():
    data = {"id": 5, "product_id": 20, "quantity": 4}
    item_out = OrderItemOut(**data)
    assert item_out.id == 5
    assert item_out.product_id == 20
    assert item_out.quantity == 4

