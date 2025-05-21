from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.utils import utils
from app.models.user import User


def register_user(db: Session, data):
    if db.query(User).filter_by(email=data.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    hashed_pw = utils.hash_password(data.password)
    user = User(name=data.name, email=data.email, hashed_password=hashed_pw, is_admin=data.is_admin)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, data):
    user = db.query(User).filter_by(email=data.email).first()
    if not user or not utils.verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access = utils.create_access_token({"sub": user.email})
    refresh = utils.create_refresh_token({"sub": user.email})
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}
