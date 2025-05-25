import pytest
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.database import Base


def test_create_user(db):
    user = User(
        name="Test User",
        email="testuser@example.com",
        hashed_password="hashed123",
        is_admin=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.name == "Test User"
    assert user.email == "testuser@example.com"
    assert user.hashed_password == "hashed123"
    assert user.is_admin is True


def test_unique_email_constraint(db):
    user1 = User(
        name="User One",
        email="unique@example.com",
        hashed_password="pass1"
    )
    db.add(user1)
    db.commit()

    user2 = User(
        name="User Two",
        email="unique@example.com",
        hashed_password="pass2"
    )
    db.add(user2)
    with pytest.raises(IntegrityError):
        db.commit()
