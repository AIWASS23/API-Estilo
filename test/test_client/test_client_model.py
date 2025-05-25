import pytest
from app.models.client import Client
from sqlalchemy.exc import IntegrityError


def test_create_client_success(db):
    client = Client(name="João da Silva", email="joao@example.com", cpf="12345678900")
    db.add(client)
    db.commit()
    db.refresh(client)

    assert client.id is not None
    assert client.name == "João da Silva"
    assert client.email == "joao@example.com"
    assert client.cpf == "12345678900"


def test_unique_email_constraint(db):
    client1 = Client(name="Maria", email="maria@example.com", cpf="11122233344")
    client2 = Client(name="Joana", email="maria@example.com", cpf="99988877766")

    db.add(client1)
    db.commit()

    db.add(client2)
    with pytest.raises(IntegrityError):
        db.commit()


def test_unique_cpf_constraint(db):
    client1 = Client(name="Carlos", email="carlos@example.com", cpf="55544433322")
    client2 = Client(name="João", email="joao2@example.com", cpf="55544433322")  # mesmo CPF

    db.add(client1)
    db.commit()

    db.add(client2)
    with pytest.raises(IntegrityError):
        db.commit()


def test_missing_fields_should_fail(db):
    client = Client(name="Sem Email e CPF")

    db.add(client)
    with pytest.raises(IntegrityError):
        db.commit()
