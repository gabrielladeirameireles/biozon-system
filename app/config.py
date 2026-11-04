import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "BIOZON Purificadores"
    ENV: str = "development"
    SECRET_KEY: str = "SUA_CHAVE_SECRETA_SUPER_SEGURA_AQUI"
    DATABASE_URL: str = "sqlite:///./biozon.db"

    # Dados do Coordenador e Empresa
    COORDINATOR_NAME: str = "Getúlio"
    COORDINATOR_EMAIL: str = "getulio@biozon.com.br"
    COMPANY_PHONE: str = "5585987847784"
    COMPANY_EMAIL: str = "[EMAIL_RESERVADO_EMPRESA]"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

