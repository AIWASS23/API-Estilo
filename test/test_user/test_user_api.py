import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def valid_register_data():
    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "strongpassword",
        "is_admin": False
    }


@pytest.fixture
def valid_login_data():
    return {
        "email": "testuser@example.com",
        "password": "strongpassword"
    }


def test_register_user(valid_register_data):
    response = client.post("/auth/register", json=valid_register_data)
    assert response.status_code == 200
    assert "Usuário" in response.json().get("message", "")


def test_login_user(valid_register_data, valid_login_data):
    client.post("/auth/register", json=valid_register_data)

    response = client.post("/auth/login", json=valid_login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token(valid_register_data, valid_login_data):
    client.post("/auth/register", json=valid_register_data)
    login_resp = client.post("/auth/login", json=valid_login_data)
    refresh_token = login_resp.json()["refresh_token"]

    response = client.post("/auth/refresh-token", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid():
    response = client.post("/auth/refresh-token", json={"refresh_token": "invalidtoken"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Token inválido ou expirado."
