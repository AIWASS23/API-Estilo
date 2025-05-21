from sqlalchemy import Column, Integer, String, UniqueConstraint
from app.database import Base


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("email", name="uq_client_email"),
        UniqueConstraint("cpf", name="uq_client_cpf"),
    )
