from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user.token import Token
from app.schemas.user.user_login import UserLogin
from app.schemas.user.user_register import Register
from app.config import settings
from app.services.user_service import register_user, login_user
from app.utils.utils import create_refresh_token, create_access_token
from jose import JWTError, jwt

user_router = APIRouter(prefix="/auth", tags=["Auth"])

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
