from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.client import Client
from app.models.user import User
from app.schemas.clients.client_base import ClientCreate, ClientOut
from app.schemas.clients.client_update import ClientUpdate
from app.services.service import get_current_user, admin_required

client_router = APIRouter(prefix="/clients", tags=["Clients"])


@client_router.get("/", response_model=List[ClientOut])
def list_clients(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    email: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    query = db.query(Client)
    if name:
        query = query.filter(Client.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Client.email.ilike(f"%{email}%"))
    return query.offset(skip).limit(limit).all()


@client_router.post("/", response_model=ClientOut)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if db.query(Client).filter_by(email=client.email).first():
        raise HTTPException(status_code=400, detail="Email já existe.")
    if db.query(Client).filter_by(cpf=client.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já existe.")

    new_client = Client(**client.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


@client_router.get("/{id}", response_model=ClientOut)
def get_client(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).get(id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return client


@client_router.put("/{id}", response_model=ClientOut)
def update_client(
    id: int,
    updates: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    client = db.query(Client).get(id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    if updates.email and updates.email != client.email:
        if db.query(Client).filter_by(email=updates.email).first():
            raise HTTPException(status_code=400, detail="Email já existe.")
    if updates.cpf and updates.cpf != client.cpf:
        if db.query(Client).filter_by(cpf=updates.cpf).first():
            raise HTTPException(status_code=400, detail="CPF já existe.")

    for attr, value in updates.dict(exclude_unset=True).items():
        setattr(client, attr, value)

    db.commit()
    db.refresh(client)
    return client

@client_router.delete("/{id}")
def delete_client(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    client = db.query(Client).get(id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    db.delete(client)
    db.commit()
    return {"message": "Cliente deletado com sucesso"}

