import pytest
from pydantic import ValidationError
from app.schemas.user.token import Token
from app.schemas.user.user_login import UserLogin
from app.schemas.user.user_register import Register


def test_token_model_success():
    data = {
        "access_token": "abc123",
        "refresh_token": "def456",
    }
    token = Token(**data)
    assert token.access_token == "abc123"
    assert token.refresh_token == "def456"
    assert token.token_type == "bearer"


def test_token_model_with_token_type():
    data = {
        "access_token": "abc123",
        "refresh_token": "def456",
        "token_type": "custom"
    }
    token = Token(**data)
    assert token.token_type == "custom"


def test_token_model_missing_fields():
    with pytest.raises(ValidationError):
        Token(refresh_token="refresh_only")

    with pytest.raises(ValidationError):
        Token(access_token="access_only")


def test_user_login_valid():
    data = {
        "email": "user@example.com",
        "password": "mypassword"
    }
    user_login = UserLogin(**data)
    assert user_login.email == "user@example.com"
    assert user_login.password == "mypassword"


def test_user_login_invalid_email():
    data = {
        "email": "invalid-email",
        "password": "mypassword"
    }
    with pytest.raises(ValidationError):
        UserLogin(**data)


def test_user_login_missing_password():
    data = {
        "email": "user@example.com"
    }
    with pytest.raises(ValidationError):
        UserLogin(**data)


def test_user_login_missing_email():
    data = {
        "password": "mypassword"
    }
    with pytest.raises(ValidationError):
        UserLogin(**data)


def test_register_valid():
    data = {
        "name": "João",
        "email": "joao@example.com",
        "password": "strongpassword"
    }
    register = Register(**data)
    assert register.name == "João"
    assert register.email == "joao@example.com"
    assert register.password == "strongpassword"
    assert register.is_admin is False


def test_register_with_is_admin_true():
    data = {
        "name": "Admin",
        "email": "admin@example.com",
        "password": "adminpass",
        "is_admin": True
    }
    register = Register(**data)
    assert register.is_admin is True


def test_register_invalid_email():
    data = {
        "name": "Maria",
        "email": "invalid-email",
        "password": "password123"
    }
    with pytest.raises(ValidationError):
        Register(**data)


def test_register_missing_fields():
    with pytest.raises(ValidationError):
        Register(email="user@example.com", password="pass")

    with pytest.raises(ValidationError):
        Register(name="User", password="pass")

    with pytest.raises(ValidationError):
        Register(name="User", email="user@example.com")


