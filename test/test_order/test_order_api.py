import pytest
from fastapi.testclient import TestClient
from main import app
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_product(db):
    product = Product(
        description="Produto Teste",
        price=10.0,
        barcode="1234567890123",
        section="Teste",
        stock=100,
        available=True
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@pytest.fixture
def sample_order(db, sample_product):
    order = Order(client="cliente@teste.com")
    db.add(order)
    db.commit()
    db.refresh(order)

    item = OrderItem(order_id=order.id, product_id=sample_product.id, quantity=5)
    db.add(item)
    db.commit()
    return order


def test_create_order_success(client, db, sample_product):
    data = {
        "client": "cliente@teste.com",
        "items": [
            {"product_id": sample_product.id, "quantity": 3}
        ]
    }
    response = client.post("/orders/", json=data)
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["client"] == data["client"]
    assert len(resp_json["items"]) == 1
    assert resp_json["items"][0]["product_id"] == sample_product.id

    db.refresh(sample_product)
    assert sample_product.stock == 97


def test_create_order_insufficient_stock(client, sample_product):
    data = {
        "client": "cliente@teste.com",
        "items": [
            {"product_id": sample_product.id, "quantity": 99999}
        ]
    }
    response = client.post("/orders/", json=data)
    assert response.status_code == 400
    assert "Estoque insuficiente" in response.json()["detail"]


def test_create_order_product_not_found(client):
    data = {
        "client": "cliente@teste.com",
        "items": [
            {"product_id": 999999, "quantity": 1}
        ]
    }
    response = client.post("/orders/", json=data)
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]


def test_list_orders(client, sample_order):
    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(order["id"] == sample_order.id for order in response.json())


def test_get_order_success(client, sample_order):
    response = client.get(f"/orders/{sample_order.id}")
    assert response.status_code == 200
    assert response.json()["id"] == sample_order.id


def test_get_order_not_found(client):
    response = client.get("/orders/9999999")
    assert response.status_code == 404


def test_update_order_status(client, sample_order):
    data = {"status": "completed"}
    response = client.put(f"/orders/{sample_order.id}", json=data)
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_update_order_not_found(client):
    data = {"status": "completed"}
    response = client.put("/orders/9999999", json=data)
    assert response.status_code == 404


def test_delete_order_success(client, sample_order, db):
    response = client.delete(f"/orders/{sample_order.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Pedido deletado com sucesso"}

    assert db.query(Order).filter(Order.id == sample_order.id).first() is None


def test_delete_order_not_found(client):
    response = client.delete("/orders/9999999")
    assert response.status_code == 404
