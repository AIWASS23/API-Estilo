from pydantic import BaseModel, EmailStr


class ClientUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    cpf: str | None = None