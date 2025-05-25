import pytest
from fastapi.testclient import TestClient
from main import app
from app.models.client import Client


@pytest.fixture
def client():
    return TestClient(app)


def test_create_client_success(client, db):
    data = {
        "name": "João Silva",
        "email": "joao@example.com",
        "cpf": "12345678900"
    }
    response = client.post("/clients/", json=data)
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["email"] == data["email"]
    assert json_resp["name"] == data["name"]
    assert "id" in json_resp


def test_create_client_duplicate_email(client, db):
    client_in_db = Client(name="Maria", email="maria@example.com", cpf="99999999999")
    db.add(client_in_db)
    db.commit()

    data = {
        "name": "Outro Cliente",
        "email": "maria@example.com",
        "cpf": "88888888888"
    }
    response = client.post("/clients/", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email já existe."


def test_list_clients(client, db):
    clients = [
        Client(name="Cliente1", email="c1@example.com", cpf="11111111111"),
        Client(name="Cliente2", email="c2@example.com", cpf="22222222222"),
    ]
    db.add_all(clients)
    db.commit()

    response = client.get("/clients/")
    assert response.status_code == 200
    json_resp = response.json()
    assert len(json_resp) == 2


def test_get_client(client, db):
    client_in_db = Client(name="Teste", email="teste@example.com", cpf="33333333333")
    db.add(client_in_db)
    db.commit()
    db.refresh(client_in_db)

    response = client.get(f"/clients/{client_in_db.id}")
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["email"] == "teste@example.com"


def test_update_client(client, db):
    client_in_db = Client(name="Teste", email="teste@example.com", cpf="33333333333")
    db.add(client_in_db)
    db.commit()
    db.refresh(client_in_db)

    update_data = {
        "name": "Teste Atualizado",
        "email": "novoemail@example.com",
        "cpf": "33333333333"
    }
    response = client.put(f"/clients/{client_in_db.id}", json=update_data)
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["name"] == "Teste Atualizado"
    assert json_resp["email"] == "novoemail@example.com"


def test_delete_client(client, db):
    client_in_db = Client(name="Teste", email="teste@example.com", cpf="33333333333")
    db.add(client_in_db)
    db.commit()
    db.refresh(client_in_db)

    response = client.delete(f"/clients/{client_in_db.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Cliente deletado com sucesso"}

    assert db.query(Client).filter_by(id=client_in_db.id).first() is None
