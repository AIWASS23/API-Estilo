import pytest
from sqlalchemy.exc import IntegrityError
from app.models.product import Product


def test_create_product_success(db):
    product = Product(
        description="Produto de teste",
        price=99.90,
        barcode="1234567890123",
        section="Eletrônicos",
        stock=10,
        available=True
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    assert product.id is not None
    assert product.description == "Produto de teste"
    assert product.barcode == "1234567890123"
    assert product.section == "Eletrônicos"
    assert product.stock == 10
    assert product.available is True


def test_product_unique_barcode(db):
    product1 = Product(
        description="Produto A",
        price=10.0,
        barcode="1111111111111",
        section="Testes",
        stock=5
    )
    product2 = Product(
        description="Produto B",
        price=20.0,
        barcode="1111111111111",
        section="Testes",
        stock=8
    )
    db.add(product1)
    db.commit()

    db.add(product2)
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_required_fields(db):
    product = Product(
        price=10.0,
        barcode="2222222222222",
        section="Testes"
    )
    db.add(product)
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()
