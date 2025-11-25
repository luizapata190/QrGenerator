from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Qr Generator API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API para creación de Códigos QR"
    
    # Valores por defecto (se sobrescriben con .env)
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "qrdb"
    POSTGRES_PORT: str = "5432"

    # API Key
    API_KEY: str = "dev-key-change-in-production"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Return the DB URI.
        When the tests are running (detected via the PYTEST_CURRENT_TEST env var),
        we fall back to an in‑memory SQLite database to avoid trying to reach the
        external PostgreSQL container.
        """
        if os.getenv("PYTEST_CURRENT_TEST"):
            return "sqlite:///:memory:"
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Allow extra env vars (e.g., pgadmin) without raising validation errors
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
