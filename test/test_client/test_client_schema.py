import pytest
from pydantic import ValidationError
from app.schemas.clients.client_base import ClientBase, ClientCreate, ClientOut
from app.schemas.clients.client_update import ClientUpdate


def test_client_base_valid():
    data = {
        "name": "Fulano da Silva",
        "email": "fulano@example.com",
        "cpf": "12345678901"
    }
    client = ClientBase(**data)
    assert client.name == "Fulano da Silva"
    assert client.email == "fulano@example.com"
    assert client.cpf == "12345678901"


@pytest.mark.parametrize("cpf", [
    "1234567890",      # 10 dígitos
    "123456789012",    # 12 dígitos
    "12345678abc",     # contém letras
    "12345@78901",     # contém símbolo
])
def test_client_base_invalid_cpf(cpf):
    with pytest.raises(ValidationError):
        ClientBase(name="Fulano", email="test@example.com", cpf=cpf)


def test_client_create_inherits_base():
    data = {
        "name": "Ciclano",
        "email": "ciclano@example.com",
        "cpf": "09876543210"
    }
    client = ClientCreate(**data)
    assert isinstance(client, ClientBase)


def test_client_out_valid():
    data = {
        "id": 1,
        "name": "Beltrano",
        "email": "beltrano@example.com",
        "cpf": "11122233344"
    }
    client = ClientOut(**data)
    assert client.id == 1
    assert client.name == "Beltrano"
    assert client.email == "beltrano@example.com"
    assert client.cpf == "11122233344"


def test_client_update_all_fields():
    data = {
        "name": "Nome Atualizado",
        "email": "atualizado@example.com",
        "cpf": "12345678901"
    }
    client_update = ClientUpdate(**data)
    assert client_update.name == "Nome Atualizado"
    assert client_update.email == "atualizado@example.com"
    assert client_update.cpf == "12345678901"


def test_client_update_partial_fields():
    data = {
        "email": "parcial@example.com"
    }
    client_update = ClientUpdate(**data)
    assert client_update.name is None
    assert client_update.email == "parcial@example.com"
    assert client_update.cpf is None


def test_client_update_empty():
    client_update = ClientUpdate()
    assert client_update.name is None
    assert client_update.email is None
    assert client_update.cpf is None


def test_client_update_invalid_email():
    with pytest.raises(ValidationError):
        ClientUpdate(email="invalid-email")

