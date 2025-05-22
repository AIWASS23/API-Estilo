from pydantic import BaseModel, EmailStr, constr


class ClientBase(BaseModel):
    name: str
    email: EmailStr
    cpf: constr(min_length=11, max_length=11, pattern=r'^\d{11}$')


class ClientCreate(ClientBase):
    pass


class ClientOut(ClientBase):
    id: int

    class Config:
        orm_mode = True


