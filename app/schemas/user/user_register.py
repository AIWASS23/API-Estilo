from pydantic import BaseModel, EmailStr


class Register(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_admin: bool = False
