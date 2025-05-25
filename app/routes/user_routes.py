from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user.token import Token
from app.schemas.user.user_login import UserLogin
from app.schemas.user.user_register import Register
from app.config import settings
from app.services.service import register_user, login_user
from app.utils.utils import create_refresh_token, create_access_token, verify_password
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordRequestForm


user_router = APIRouter(prefix="/auth", tags=["Auth"])


@user_router.post("/token", response_model=Token)
def login_oauth(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access = create_access_token({"sub": user.email})
    refresh = create_refresh_token({"sub": user.email})
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }

@user_router.post("/register", response_model=dict)
def register(data: Register, db: Session = Depends(get_db)):
    user = register_user(db, data)
    return {"message": f"Usuário {user.email} criado com sucesso."}


@user_router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, data)


@user_router.post("/refresh-token", response_model=Token)
def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise JWTError()
        access = create_access_token({"sub": email})
        new_refresh = create_refresh_token({"sub": email})
        return {"access_token": access, "refresh_token": new_refresh, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido ou expirado.")
