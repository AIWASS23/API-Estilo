import pytest
from fastapi.testclient import TestClient
from app.models.product import Product
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_create_product_success(client, db):
    product = Product(
        description="Tênis de Corrida",
        price=249.90,
        barcode="1234567890123",
        section="Esporte",
        stock=100,
        valid_until="2025-12-31"
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.get(f"/products/{product.id}")
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["description"] == "Tênis de Corrida"
    assert json_resp["barcode"] == "1234567890123"


def test_create_product_duplicate_barcode(client, db):
    product = Product(
        description="Tênis de Corrida",
        price=249.90,
        barcode="1234567890123",
        section="Esporte",
        stock=100,
        valid_until="2025-12-31"
    )
    db.add(product)
    db.commit()

    data = {
        "description": "Outro Produto",
        "price": 199.90,
        "barcode": "1234567890123",
        "section": "Moda",
        "stock": 50,
        "valid_until": "2025-12-31"
    }
    response = client.post("/products/", data=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Código de barras já existe."


def test_list_products(client, db):
    db.add_all([
        Product(description="Prod 1", price=10.0, barcode="1111111111111", section="A", stock=5),
        Product(description="Prod 2", price=20.0, barcode="2222222222222", section="B", stock=10)
    ])
    db.commit()

    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2


def test_get_product(client, db):
    product = Product(description="Produto X", price=100.0, barcode="9999999999999", section="Eletrônicos", stock=10)
    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.get(f"/products/{product.id}")
    assert response.status_code == 200
    assert response.json()["id"] == product.id


def test_get_product_not_found(client):
    response = client.get("/products/999999")
    assert response.status_code == 404


def test_update_product(client, db):
    product = Product(description="Original", price=100.0, barcode="7777777777777", section="Outros", stock=5)
    db.add(product)
    db.commit()
    db.refresh(product)

    update_data = {"price": 199.99, "stock": 80}
    response = client.put(f"/products/{product.id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["price"] == 199.99
    assert response.json()["stock"] == 80


def test_delete_product(client, db):
    product = Product(description="Deletável", price=50.0, barcode="8888888888888", section="Velharias", stock=3)
    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.delete(f"/products/{product.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Produto deletado com sucesso"

    assert db.query(Product).filter_by(id=product.id).first() is None
