# Guía Completa de Desarrollo - QR Generator API

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Fase 1: Configuración Inicial del Proyecto](#fase-1-configuración-inicial-del-proyecto)
3. [Fase 2: Estructura Base de FastAPI](#fase-2-estructura-base-de-fastapi)
4. [Fase 3: Integración con Base de Datos](#fase-3-integración-con-base-de-datos)
5. [Fase 4: Implementación de Funcionalidades](#fase-4-implementación-de-funcionalidades)
6. [Fase 5: Seguridad y Autenticación](#fase-5-seguridad-y-autenticación)
7. [Fase 6: Logging y Monitoreo](#fase-6-logging-y-monitoreo)
8. [Fase 7: Dockerización](#fase-7-dockerización)
9. [Fase 8: Testing](#fase-8-testing)
10. [Fase 9: Documentación](#fase-9-documentación)
11. [Mejores Prácticas](#mejores-prácticas)

---

## Introducción

Esta guía documenta el proceso completo de desarrollo de la aplicación **QR Generator API**, desde la configuración inicial hasta el despliegue en producción. Sigue estos pasos para replicar el proyecto o crear aplicaciones similares.

### Tecnologías Utilizadas
- **Python 3.12+**
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para base de datos
- **PostgreSQL** - Base de datos relacional
- **Pydantic** - Validación de datos
- **Poetry** - Gestión de dependencias
- **Docker** - Contenedorización
- **pytest** - Testing automatizado

---

## Fase 1: Configuración Inicial del Proyecto

### 1.1 Instalar Poetry

```powershell
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### 1.2 Crear el Proyecto

```powershell
# Crear directorio del proyecto
mkdir QrGenerator
cd QrGenerator

# Inicializar Poetry
poetry init

# Responder las preguntas interactivas:
# - Package name: qr-generator
# - Version: 1.0.0
# - Description: API para generación de códigos QR
# - Author: Tu Nombre
# - License: MIT
# - Compatible Python versions: ^3.12
```

### 1.3 Agregar Dependencias Principales

```powershell
# Framework web
poetry add fastapi uvicorn[standard]

# Base de datos
poetry add sqlalchemy psycopg2-binary

# Validación y configuración
poetry add pydantic pydantic-settings

# Generación de QR
poetry add qrcode[pil]

# Dependencias de desarrollo
poetry add --group dev pytest pytest-cov httpx
```

### 1.4 Crear Estructura de Carpetas

```powershell
# Crear estructura base
mkdir app
mkdir app\core
mkdir app\models
mkdir app\schemas
mkdir app\routers
mkdir app\services
mkdir app\middleware
mkdir tests

# Crear archivos __init__.py
New-Item app\__init__.py
New-Item app\core\__init__.py
New-Item app\models\__init__.py
New-Item app\schemas\__init__.py
New-Item app\routers\__init__.py
New-Item app\services\__init__.py
New-Item app\middleware\__init__.py
New-Item tests\__init__.py
```

### 1.5 Configurar .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Poetry
poetry.lock

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# Docker
*.log
```

---

## Fase 2: Estructura Base de FastAPI

### 2.1 Crear Configuración Central (`app/core/config.py`)

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "QR Generator API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API para creación de Códigos QR"
    
    # Database
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
        """Construye la URL de conexión a la base de datos."""
        if os.getenv("PYTEST_CURRENT_TEST"):
            return "sqlite:///:memory:"
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
```

**Puntos clave:**
- Usa `pydantic-settings` para cargar variables de entorno
- `extra="ignore"` permite variables adicionales en `.env` sin errores
- La propiedad `SQLALCHEMY_DATABASE_URI` construye la URL de conexión
- Detecta si se están ejecutando tests para usar SQLite en memoria

### 2.2 Crear Archivo de Entorno (`.env`)

```dotenv
# Configuración de la API
PROJECT_NAME=QR Generator API
VERSION=1.0.0
DESCRIPTION=API para creación de Códigos QR

# Configuración de PostgreSQL
POSTGRES_SERVER=db
POSTGRES_USER=qr_app_user
POSTGRES_PASSWORD=qr_app_password_2025
POSTGRES_DB=qrdb
POSTGRES_PORT=5432
POSTGRES_EXTERNAL_PORT=5433

# Configuración de pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin

# API Key Configuration
API_KEY=tu_api_key_segura_aqui

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### 2.3 Crear Aplicación Principal (`app/main.py`)

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import engine, Base
from app.core.logging_config import setup_logging
from app.middleware.logging_middleware import LoggingMiddleware

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación."""
    # Startup
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
    
    yield
    
    # Shutdown
    logger.info("Application shutting down")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan
)

# Agregar middleware
app.add_middleware(LoggingMiddleware)

# Incluir routers (se agregarán más adelante)
# from app.routers import qr, users
# app.include_router(qr.router)
# app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "QR Generator API", "version": settings.VERSION}
```

**Puntos clave:**
- `lifespan` gestiona eventos de inicio y cierre
- `Base.metadata.create_all()` crea las tablas automáticamente
- Middleware se agrega antes de los routers

---

## Fase 3: Integración con Base de Datos

### 3.1 Configurar Conexión a Base de Datos (`app/core/database.py`)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Crear engine de SQLAlchemy
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    echo=False  # Cambiar a True para debug SQL
)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

def get_db():
    """Dependency para obtener sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 3.2 Crear Modelo de Usuario (`app/models/user.py`)

```python
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
```

**Puntos clave:**
- Hereda de `Base` (definido en `database.py`)
- `__tablename__` define el nombre de la tabla en PostgreSQL
- `index=True` mejora el rendimiento de búsquedas
- `unique=True` garantiza que no haya duplicados

### 3.3 Crear Esquemas Pydantic (`app/schemas/user.py`)

```python
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """Campos comunes para User."""
    cedula: str
    nombre: str
    email: EmailStr

class UserCreate(UserBase):
    """Schema para crear usuario."""
    pass

class UserResponse(UserBase):
    """Schema para respuesta de usuario."""
    id: int

    model_config = {"from_attributes": True}
```

**Puntos clave:**
- `UserBase` contiene campos comunes
- `UserCreate` para datos de entrada (POST)
- `UserResponse` para datos de salida (GET)
- `from_attributes=True` permite convertir modelos SQLAlchemy a Pydantic

---

## Fase 4: Implementación de Funcionalidades

### 4.1 Crear Servicio de Usuarios (`app/services/user_service.py`)

```python
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
import logging

logger = logging.getLogger(__name__)

def get_user_by_cedula(db: Session, cedula: str):
    """Obtiene un usuario por cédula."""
    logger.info(f"Buscando usuario con cédula: {cedula}")
    return db.query(User).filter(User.cedula == cedula).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene lista de usuarios con paginación."""
    logger.info(f"Obteniendo usuarios (skip={skip}, limit={limit})")
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    """Crea un nuevo usuario."""
    logger.info(f"Creando usuario: {user.cedula}")
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"Usuario creado exitosamente: {db_user.id}")
    return db_user
```

**Puntos clave:**
- Funciones puras que solo trabajan con datos
- No conocen HTTP (no usan Request/Response)
- Logging estructurado para trazabilidad

### 4.2 Crear Router de Usuarios (`app/routers/users.py`)

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario."""
    db_user = user_service.get_user_by_cedula(db, cedula=user.cedula)
    if db_user:
        raise HTTPException(status_code=400, detail="Cédula ya registrada")
    return user_service.create_user(db=db, user=user)

@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtiene lista de usuarios."""
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{cedula}", response_model=UserResponse)
def read_user(cedula: str, db: Session = Depends(get_db)):
    """Obtiene un usuario por cédula."""
    db_user = user_service.get_user_by_cedula(db, cedula=cedula)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user
```

**Puntos clave:**
- `Depends(get_db)` inyecta la sesión de base de datos
- `response_model` valida y serializa la respuesta
- `HTTPException` para errores HTTP estándar

### 4.3 Crear Servicio de QR (`app/services/qr_service.py`)

```python
import qrcode
from io import BytesIO
import base64
import logging

logger = logging.getLogger(__name__)

def generate_qr_image(data: str) -> BytesIO:
    """Genera imagen QR y la devuelve como BytesIO."""
    logger.info(f"Generando QR para: {data[:50]}...")
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    logger.info("QR generado exitosamente")
    return buffer

def generate_qr_base64(data: str) -> str:
    """Genera QR y lo devuelve en formato Base64."""
    logger.info(f"Generando QR Base64 para: {data[:50]}...")
    buffer = generate_qr_image(data)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    logger.info("QR Base64 generado exitosamente")
    return img_base64
```

### 4.4 Crear Router de QR (`app/routers/qr.py`)

```python
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from app.services import qr_service

router = APIRouter(tags=["QR"])

@router.get("/GenerateQr/")
def generate_qr(data: str):
    """Genera y devuelve imagen QR."""
    qr_image = qr_service.generate_qr_image(data)
    return StreamingResponse(qr_image, media_type="image/png")

@router.get("/GenerateQrBase64/")
def generate_qr_base64(data: str):
    """Genera QR en formato Base64."""
    qr_base64 = qr_service.generate_qr_base64(data)
    return JSONResponse(content={"qr_code": qr_base64})

@router.get("/DownloadQr/")
def download_qr(data: str, filename: str = "qr_code.png"):
    """Descarga QR como archivo."""
    qr_image = qr_service.generate_qr_image(data)
    return StreamingResponse(
        qr_image,
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
```

### 4.5 Registrar Routers en `app/main.py`

```python
# Agregar después de crear la app
from app.routers import qr, users

app.include_router(qr.router)
app.include_router(users.router)
```

---

## Fase 5: Seguridad y Autenticación

### 5.1 Crear Módulo de Seguridad (`app/core/security.py`)

```python
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    """Verifica que el API Key sea válido."""
    if api_key is None:
        logger.warning("API Key no proporcionada")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key no proporcionada"
        )
    
    if api_key != settings.API_KEY:
        logger.warning(f"API Key inválida: {api_key[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida"
        )
    
    logger.info("API Key válida")
    return api_key
```

### 5.2 Proteger Endpoints

```python
# En app/routers/users.py
from app.core.security import verify_api_key

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)  # Agregar esta línea
):
    """Crea un nuevo usuario (requiere API Key)."""
    # ... resto del código
```

### 5.3 Generar API Keys Seguras (`generate_key.py`)

```python
import secrets
import base64

def generate_api_key(length: int = 32) -> str:
    """Genera un API Key seguro."""
    random_bytes = secrets.token_bytes(length)
    api_key = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    return api_key

if __name__ == "__main__":
    print("API Key generada:")
    print(generate_api_key())
```

---

## Fase 6: Logging y Monitoreo

### 6.1 Configurar Logging Estructurado (`app/core/logging_config.py`)

```python
import logging
import json
from datetime import datetime
from app.core.config import settings

class JsonFormatter(logging.Formatter):
    """Formateador de logs en JSON."""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3],
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "taskName": getattr(record, "taskName", "N/A")
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

def setup_logging():
    """Configura el sistema de logging."""
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    handler = logging.StreamHandler()
    
    if settings.LOG_FORMAT == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
    
    logger.addHandler(handler)
```

### 6.2 Crear Middleware de Logging (`app/middleware/logging_middleware.py`)

```python
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging
import time

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para logging de requests HTTP."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        logger.info(
            "Incoming request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host
            }
        )
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": f"{process_time:.3f}s"
            }
        )
        
        return response
```

---

## Fase 7: Dockerización

### 7.1 Crear Dockerfile

```dockerfile
# Etapa 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install "poetry==2.0.0"

# Copiar archivos de dependencias
COPY pyproject.toml poetry.lock ./

# Instalar dependencias
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Etapa 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Copiar dependencias instaladas
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Puntos clave:**
- Multistage build reduce el tamaño de la imagen
- Builder instala dependencias
- Runtime solo contiene lo necesario para ejecutar

### 7.2 Crear docker-compose.yml

```yaml
services:
  qr-generator:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    env_file:
      - .env
    environment:
      - PROJECT_NAME=${PROJECT_NAME:-Qr Generator API (Docker)}
      - POSTGRES_SERVER=${POSTGRES_SERVER:-db}
      - POSTGRES_USER=${POSTGRES_USER:-postgres}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
      - POSTGRES_DB=${POSTGRES_DB:-qrdb}
      - POSTGRES_PORT=${POSTGRES_PORT:-5432}
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env
    environment:
      - POSTGRES_USER=${POSTGRES_USER:-postgres}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
      - POSTGRES_DB=${POSTGRES_DB:-qrdb}
    ports:
      - "${POSTGRES_EXTERNAL_PORT:-5433}:5432"

  pgadmin:
    image: dpage/pgadmin4
    env_file:
      - .env
    environment:
      - PGADMIN_DEFAULT_EMAIL=${PGADMIN_DEFAULT_EMAIL:-admin@admin.com}
      - PGADMIN_DEFAULT_PASSWORD=${PGADMIN_DEFAULT_PASSWORD:-admin}
    ports:
      - "5050:80"
    depends_on:
      - db

volumes:
  postgres_data:
```

**Puntos clave:**
- `depends_on` asegura que PostgreSQL inicie primero
- Volúmenes persisten datos entre reinicios
- Variables de entorno con valores por defecto

---

## Fase 8: Testing

### 8.1 Configurar Tests (`tests/conftest.py`)

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Fixture que proporciona un cliente de prueba."""
    return TestClient(app)
```

**Puntos clave:**
- `conftest.py` contiene fixtures compartidas
- `TestClient` simula peticiones HTTP sin levantar servidor
- SQLite en memoria (configurado en `config.py`) evita dependencia de PostgreSQL

### 8.2 Crear Tests de API Key (`tests/test_api_key.py`)

```python
from app.core.config import settings

def test_endpoint_sin_api_key(client):
    """Verifica que endpoint protegido rechace sin API Key."""
    response = client.post("/users/", json={
        "cedula": "123456",
        "nombre": "Test",
        "email": "test@test.com"
    })
    assert response.status_code == 401

def test_endpoint_con_api_key_invalida(client):
    """Verifica que endpoint protegido rechace API Key inválida."""
    response = client.post(
        "/users/",
        json={"cedula": "123456", "nombre": "Test", "email": "test@test.com"},
        headers={"X-API-Key": "clave_incorrecta"}
    )
    assert response.status_code == 403

def test_endpoint_con_api_key_valida(client):
    """Verifica que endpoint protegido acepte API Key válida."""
    response = client.post(
        "/users/",
        json={"cedula": "123456", "nombre": "Test", "email": "test@test.com"},
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 201
```

### 8.3 Crear Tests de Usuarios (`tests/test_users.py`)

```python
from app.core.config import settings

def test_create_user(client):
    """Prueba creación de usuario."""
    response = client.post(
        "/users/",
        json={"cedula": "987654", "nombre": "Juan", "email": "juan@test.com"},
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["cedula"] == "987654"
    assert data["nombre"] == "Juan"

def test_get_users(client):
    """Prueba obtención de lista de usuarios."""
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_not_found(client):
    """Prueba obtención de usuario inexistente."""
    response = client.get("/users/999999")
    assert response.status_code == 404
```

### 8.4 Ejecutar Tests

```powershell
# Ejecutar todos los tests
poetry run pytest

# Con cobertura
poetry run pytest --cov=app --cov-report=html

# Solo un archivo
poetry run pytest tests/test_users.py -v
```

---

## Fase 9: Documentación

### 9.1 Crear README.md

Ver archivo `README.md` del proyecto para estructura completa.

**Debe incluir:**
- Descripción del proyecto
- Características principales
- Requisitos previos
- Instalación paso a paso
- Uso de la API
- Estructura del proyecto
- Tecnologías utilizadas

### 9.2 Crear ARCHITECTURE.md

Ver archivo `ARCHITECTURE.md` del proyecto.

**Debe incluir:**
- Diagrama de arquitectura (Mermaid)
- Flujo de datos
- Responsabilidades por capa
- Ejemplos de secuencia

### 9.3 Crear AUTH.md

Ver archivo `AUTH.md` del proyecto.

**Debe incluir:**
- Cómo funciona la autenticación
- Generación de API Keys
- Ejemplos de uso
- Mejores prácticas de seguridad

### 9.4 Documentación Automática

FastAPI genera automáticamente:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Mejores Prácticas

### 1. Seguridad

✅ **Hacer:**
- Usar variables de entorno para credenciales
- Nunca commitear `.env` al repositorio
- Generar API Keys seguras con `secrets`
- Validar todos los inputs con Pydantic
- Usar HTTPS en producción

❌ **Evitar:**
- Hardcodear contraseñas en el código
- Usar API Keys débiles o predecibles
- Exponer información sensible en logs
- Deshabilitar validación de SSL

### 2. Base de Datos

✅ **Hacer:**
- Usar migraciones (Alembic) en producción
- Crear índices en columnas de búsqueda frecuente
- Usar `pool_pre_ping=True` para verificar conexiones
- Cerrar sesiones con `try/finally`

❌ **Evitar:**
- Modificar esquema directamente en producción
- Dejar sesiones abiertas
- Ejecutar queries sin límites (usar paginación)

### 3. Código

✅ **Hacer:**
- Separar responsabilidades (routers, services, models)
- Usar type hints en todas las funciones
- Documentar funciones con docstrings
- Escribir tests para funcionalidades críticas
- Usar logging estructurado

❌ **Evitar:**
- Poner lógica de negocio en routers
- Funciones de más de 50 líneas
- Código duplicado
- Imports circulares

### 4. Docker

✅ **Hacer:**
- Usar multistage builds
- Especificar versiones exactas de imágenes
- Usar volúmenes para datos persistentes
- Configurar health checks

❌ **Evitar:**
- Usar tag `latest` en producción
- Ejecutar como root dentro del contenedor
- Incluir archivos innecesarios (usar `.dockerignore`)

### 5. Testing

✅ **Hacer:**
- Probar casos exitosos y de error
- Usar fixtures para datos de prueba
- Mantener tests rápidos (usar SQLite en memoria)
- Alcanzar al menos 80% de cobertura

❌ **Evitar:**
- Tests que dependen de orden de ejecución
- Tests que modifican estado global
- Tests sin assertions claras

---

## Comandos de Referencia Rápida

```powershell
# Desarrollo local
poetry install                          # Instalar dependencias
poetry run uvicorn app.main:app --reload  # Ejecutar servidor

# Docker
docker compose up --build               # Construir y levantar
docker compose down                     # Detener servicios
docker compose logs qr-generator        # Ver logs

# Testing
poetry run pytest                       # Ejecutar tests
poetry run pytest -v                    # Modo verbose
poetry run pytest --cov=app             # Con cobertura

# Base de datos
docker exec -it qrgenerator-db-1 psql -U postgres -d qrdb  # Acceder a PostgreSQL

# Generar API Key
poetry run python generate_key.py       # Generar nueva API Key
```

---

## Próximos Pasos Recomendados

1. **Migraciones de Base de Datos**
   - Implementar Alembic para gestionar cambios de esquema
   - Crear migraciones versionadas

2. **CI/CD**
   - Configurar GitHub Actions para tests automáticos
   - Automatizar despliegue a producción

3. **Monitoreo**
   - Integrar Prometheus para métricas
   - Configurar alertas con Grafana

4. **Escalabilidad**
   - Implementar caché con Redis
   - Configurar balanceador de carga

5. **Documentación Adicional**
   - Crear guía de contribución (CONTRIBUTING.md)
   - Documentar API con ejemplos de uso

---

## Conclusión

Esta guía proporciona una base sólida para desarrollar aplicaciones FastAPI profesionales. Siguiendo estas prácticas y estructura, podrás crear aplicaciones escalables, mantenibles y seguras.

Para más información, consulta:
- [Documentación oficial de FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Documentation](https://docs.docker.com/)
