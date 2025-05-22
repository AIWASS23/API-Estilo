from sqlalchemy.orm import Session
from app.utils import utils
from app.models.user import User
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.database import get_db
from app.models.user import User
from app.config import settings


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



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(User).filter(User.name == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


def admin_required(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permissão de administrador necessária")
    return current_user

