from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = None
    ECHO_SQL: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_app_settings() -> Settings:
    return Settings()