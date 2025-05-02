import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig
from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = None
    ECHO_SQL: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


class EmailSettings(BaseSettings):
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: SecretStr = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: EmailStr = os.getenv("MAIL_FROM")
    MAIL_PORT: int = os.getenv("MAIL_PORT")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS")
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS")
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS")
    VALIDATE_CERTS: bool = os.getenv("VALIDATE_CERTS")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


def get_app_settings() -> Settings:
    return Settings()


def get_email_configuration() -> ConnectionConfig:
    email_settings = EmailSettings()

    return ConnectionConfig(
        MAIL_USERNAME=email_settings.MAIL_USERNAME,
        MAIL_PASSWORD=email_settings.MAIL_PASSWORD,
        MAIL_FROM=email_settings.MAIL_FROM,
        MAIL_PORT=email_settings.MAIL_PORT,
        MAIL_SERVER=email_settings.MAIL_SERVER,
        MAIL_STARTTLS=email_settings.MAIL_STARTTLS,
        MAIL_SSL_TLS=email_settings.MAIL_SSL_TLS,
    )
