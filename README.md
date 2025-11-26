# QR Generator API

API REST desarrollada en Python con FastAPI para la generación de códigos QR y gestión de usuarios con PostgreSQL.

## Características

- Generación de códigos QR en formato imagen (PNG).
- Generación de códigos QR en formato Base64 (JSON).
- Descarga directa de archivos QR.
- Gestión de usuarios con base de datos PostgreSQL.
- Arquitectura modular y escalable.
- Configuración centralizada.
- Soporte para Docker y Docker Compose.
- Interfaz web de administración de base de datos (pgAdmin).

## Requisitos Previos

- Python 3.12+
- [Poetry](https://python-poetry.org/) (Gestor de dependencias)
- Docker y Docker Compose (Opcional, para despliegue en contenedores)

## Instalación y Ejecución Local

1.  **Clonar el repositorio** (si aplica) o navegar a la carpeta del proyecto.

2.  **Instalar dependencias con Poetry**:
    ```bash
    poetry install
    ```

3.  **Configurar variables de entorno**:
    Crea un archivo `.env` en la raíz del proyecto:
    ```ini
    PROJECT_NAME="Qr Generator API"
    VERSION="1.0.0"
    DESCRIPTION="API para creación de Códigos QR"
    POSTGRES_SERVER=localhost
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=qrdb
    POSTGRES_PORT=5432
    ```

4.  **Levantar solo la base de datos con Docker**:
    ```bash
    docker compose up db -d
    ```

5.  **Ejecutar el servidor de desarrollo**:
    ```bash
    poetry run uvicorn app.main:app --reload
    ```

6.  **Acceder a la documentación**:
    Abre tu navegador en [http://localhost:8000/docs](http://localhost:8000/docs) para ver Swagger UI.

## Despliegue con Docker (Recomendado)

### Levantar todos los servicios

```bash
docker compose up --build
```

Esto iniciará:
- **API (FastAPI)**: http://localhost:8000
- **PostgreSQL**: localhost:5433
- **pgAdmin**: http://localhost:5050

### Acceder a pgAdmin

1. Abre http://localhost:5050 en tu navegador
2. Inicia sesión:
   - **Email**: `admin@admin.com`
   - **Password**: `admin`

3. Registra el servidor de PostgreSQL:
   - Click derecho en "Servers" → "Register" → "Server..."
   - **General** → Name: `QR Generator DB`
   - **Connection**:
     - Host: `db`
     - Port: `5432`
     - Database: `qrdb`
     - Username: `postgres`
     - Password: `postgres`
     - ✅ Save password

## Ejecutar Pruebas

Para verificar que todo funciona correctamente, ejecuta los tests automatizados:

```bash
poetry run pytest
```

## Seguridad y Autenticación

El proyecto cuenta con seguridad mediante **API Key** y **Logging Estructurado**.

- Para detalles de implementación y uso, ver [AUTH.md](AUTH.md).
- Algunos endpoints (como `POST /users/`) requieren el header `X-API-Key`.

## Endpoints de la API

### Códigos QR

- `GET /GenerateQr/?data=<texto>` - Genera y devuelve imagen QR
- `GET /GenerateQrBase64/?data=<texto>` - Devuelve QR en formato Base64 (JSON)
- `GET /DownloadQr/?data=<texto>&filename=<nombre>` - Descarga QR como archivo PNG

### Usuarios

- `POST /users/` - Crear un nuevo usuario
- `GET /users/` - Listar todos los usuarios
- `GET /users/{cedula}` - Obtener usuario por cédula

## Estructura del Proyecto

```text
.
├── app/
│   ├── core/       # Configuración (config.py, database.py)
│   ├── models/     # Modelos de base de datos (SQLAlchemy)
│   ├── schemas/    # Esquemas de validación (Pydantic)
│   ├── routers/    # Endpoints de la API (qr.py, users.py)
│   ├── services/   # Lógica de negocio (qr_service.py, user_service.py)
│   └── main.py     # Punto de entrada de la aplicación
├── tests/          # Pruebas automatizadas
├── Dockerfile      # Definición de imagen Docker
├── docker-compose.yml # Orquestación de contenedores
├── pyproject.toml  # Dependencias y configuración del proyecto
├── README.md       # Este archivo
└── TUTORIAL.md     # Guía de aprendizaje paso a paso
```

## Puertos Utilizados

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| API (FastAPI) | 8000 | Documentación en /docs |
| PostgreSQL | 5433 | Base de datos (puerto externo) |
| pgAdmin | 5050 | Interfaz web de administración |

## Documentación del Proyecto

Este proyecto cuenta con documentación completa para facilitar el desarrollo y mantenimiento:

### 📚 Guías de Desarrollo
- **[DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)** - Guía paso a paso para crear la aplicación desde cero
  - Configuración inicial del proyecto
  - Implementación de cada fase
  - Mejores prácticas y comandos de referencia
  - Ideal para replicar el proyecto o crear aplicaciones similares

### 🏗️ Arquitectura y Diseño
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Diagramas y explicación de la arquitectura
  - Flujo de datos de la aplicación
  - Responsabilidades por capa
  - Ejemplos de secuencia

- **[DESIGN_DECISIONS.md](DESIGN_DECISIONS.md)** - Decisiones técnicas y lecciones aprendidas
  - Por qué se eligió cada tecnología
  - Problemas encontrados y soluciones
  - Decisiones de seguridad y despliegue

### 🔐 Seguridad
- **[AUTH.md](AUTH.md)** - Guía de autenticación y seguridad
  - Implementación de API Key
  - Generación de claves seguras
  - Ejemplos de uso

- **[SECURITY.md](SECURITY.md)** - Políticas de seguridad del proyecto

### 📖 Tutoriales
- **[TUTORIAL.md](TUTORIAL.md)** - Guía de aprendizaje conceptual
  - Explicación de conceptos clave
  - Cómo agregar nuevos módulos
  - Comandos útiles

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para interacción con base de datos
- **PostgreSQL**: Base de datos relacional
- **Pydantic**: Validación de datos
- **Docker**: Contenedorización
- **Poetry**: Gestión de dependencias
- **pytest**: Testing automatizado
