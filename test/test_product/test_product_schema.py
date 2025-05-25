import pytest
from datetime import date
from pydantic import ValidationError
from app.schemas.products.product_base import ProductBase, ProductCreate, ProductOut
from app.schemas.products.product_update import ProductUpdate


def test_product_base_valid():
    product = ProductBase(
        description="Produto Teste",
        price=49.90,
        barcode="1234567890123",
        section="Promoção",
        stock=100,
        valid_until=date(2025, 12, 31),
        available=False
    )
    assert product.description == "Produto Teste"
    assert product.price == 49.90
    assert product.barcode == "1234567890123"
    assert product.section == "Promoção"
    assert product.stock == 100
    assert product.valid_until == date(2025, 12, 31)
    assert product.available is False


@pytest.mark.parametrize("barcode", [
    "12345678901",         # 11 dígitos
    "123456789012345",     # 15 dígitos
    "ABCDEFGHIJKLM",       # letras
    "12345abc90123",       # alfanumérico
])
def test_product_base_invalid_barcode(barcode):
    with pytest.raises(ValidationError):
        ProductBase(
            description="Produto",
            price=10.0,
            barcode=barcode,
            section="Testes",
            stock=5
        )


def test_product_create_inherits_product_base():
    product = ProductCreate(
        description="Produto A",
        price=15.00,
        barcode="3213213213210",
        section="Utilidades",
        stock=20
    )
    assert isinstance(product, ProductBase)


def test_product_out_valid():
    product = ProductOut(
        id=1,
        description="Produto Completo",
        price=100.0,
        barcode="1112223334445",
        section="Vendas",
        stock=50,
        available=True,
        valid_until=None,
        image_url="http://example.com/image.png"
    )
    assert product.id == 1
    assert product.image_url == "http://example.com/image.png"


def test_product_update_all_fields():
    update = ProductUpdate(
        description="Novo nome",
        price=199.99,
        section="Atualizada",
        stock=30,
        valid_until=date(2025, 1, 1),
        available=False
    )
    assert update.description == "Novo nome"
    assert update.price == 199.99
    assert update.section == "Atualizada"
    assert update.stock == 30
    assert update.valid_until == date(2025, 1, 1)
    assert update.available is False


def test_product_update_partial_fields():
    update = ProductUpdate(price=79.90)
    assert update.price == 79.90
    assert update.description is None
    assert update.stock is None


@pytest.mark.parametrize("field,value", [
    ("price", "not-a-float"),
    ("stock", "abc"),
    ("valid_until", "not-a-date"),
    ("available", "yes")
])
def test_product_update_invalid_types(field, value):
    with pytest.raises(ValidationError):
        ProductUpdate(**{field: value})

