import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    ECHO_SQL: bool = os.getenv("ECHO_SQL")
    REDIS_URL: str = f"{os.getenv('REDIS_URL')}/0"
    CELERY_REDIS_URL: str = f"{os.getenv('REDIS_URL')}/1"
    API_KEYS: list[str] = os.getenv("API_KEYS")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


class EmailSettings(BaseSettings):
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
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


def get_email_configuration() -> EmailSettings:
    return EmailSettings()


def get_email_connection_config() -> ConnectionConfig:
    email_settings_config = EmailSettings()
    return ConnectionConfig(
        MAIL_USERNAME=email_settings_config.MAIL_USERNAME,
        MAIL_PASSWORD=email_settings_config.MAIL_PASSWORD,
        MAIL_FROM=email_settings_config.MAIL_FROM,
        MAIL_PORT=email_settings_config.MAIL_PORT,
        MAIL_SERVER=email_settings_config.MAIL_SERVER,
        MAIL_STARTTLS=email_settings_config.MAIL_STARTTLS,
        MAIL_SSL_TLS=email_settings_config.MAIL_SSL_TLS
    )


settings = get_app_settings()
email_settings = get_email_configuration()
conf = get_email_connection_config()
