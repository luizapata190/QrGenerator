from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.routers import qr, users
from app.core.database import engine, Base
from app.core.logging_config import setup_logging
from app.middleware.logging_middleware import log_requests
import logging

# Configurar logging
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas al iniciar la aplicación
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}", exc_info=True)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION + "\n\n**Autenticación:** Algunos endpoints (como POST /users/) requieren API Key en header `X-API-Key`.",
    version=settings.VERSION,
    lifespan=lifespan
)

# Middleware de logging
app.middleware("http")(log_requests)

app.include_router(qr.router)
app.include_router(users.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)