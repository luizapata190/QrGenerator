from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Qr Generator API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API para creación de Códigos QR"
    
    class Config:
        env_file = ".env"

settings = Settings()
