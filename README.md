# QR Generator API

API REST desarrollada en Python con FastAPI para la generación de códigos QR.

## Características

- Generación de códigos QR en formato imagen (PNG).
- Generación de códigos QR en formato Base64 (JSON).
- Descarga directa de archivos QR.
- Arquitectura modular y escalable.
- Configuración centralizada.
- Soporte para Docker y Docker Compose.

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
    Crea un archivo `.env` en la raíz del proyecto (puedes copiar `.env.example` si existe, o usar los valores por defecto):
    ```ini
    PROJECT_NAME="Qr Generator API"
    VERSION="1.0.0"
    DESCRIPTION="API para creación de Códigos QR"
    ```

4.  **Ejecutar el servidor de desarrollo**:
    ```bash
    poetry run uvicorn app.main:app --reload
    ```

5.  **Acceder a la documentación**:
    Abre tu navegador en [http://localhost:8000/docs](http://localhost:8000/docs) para ver Swagger UI.

## Despliegue con Docker

### Opción 1: Docker Compose (Recomendado para desarrollo/local)

1.  **Construir y levantar el servicio**:
    ```bash
    docker compose up --build
    ```
    El servicio estará disponible en `http://localhost:8000`.

### Opción 2: Docker Manual (Producción)

1.  **Construir la imagen**:
    ```bash
    docker build -t qr-generator-api .
    ```

2.  **Ejecutar el contenedor**:
    ```bash
    docker run -d -p 8000:8000 --name qr-api qr-generator-api
    ```

## Ejecutar Pruebas

Para verificar que todo funciona correctamente, ejecuta los tests automatizados:

```bash
poetry run pytest
```

## Estructura del Proyecto

```text
.
├── app/
│   ├── core/       # Configuración (config.py)
│   ├── routers/    # Endpoints de la API (qr.py)
│   ├── services/   # Lógica de negocio (qr_service.py)
│   └── main.py     # Punto de entrada de la aplicación
├── tests/          # Pruebas automatizadas
├── Dockerfile      # Definición de imagen Docker
├── docker-compose.yml # Orquestación de contenedores
└── pyproject.toml  # Dependencias y configuración del proyecto
```
