from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Banco de dados
    DATABASE_URL: str

    # WhatsApp
    WHATSAPP_API_URL: str = ""
    WHATSAPP_API_TOKEN: str = ""

    # sentry
    SENTRY_DSN: str


    class Config:
        env_file = ".env"


settings = Settings()