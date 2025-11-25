# Guía de Aprendizaje: Construyendo una API Profesional con FastAPI

Esta guía documenta el paso a paso de cómo transformamos un script básico en una API profesional, escalable y conectada a base de datos. Úsala como referencia para tus futuros proyectos.

## Fase 1: Estructura y Configuración Profesional

### 1. Gestión de Dependencias (Poetry)
En lugar de `pip` y `requirements.txt`, usamos **Poetry**.
- **¿Por qué?**: Maneja versiones, conflictos y entornos virtuales automáticamente.
- **Comando clave**: `poetry init` (crear proyecto), `poetry add fastapi` (instalar librería).

### 2. Estructura de Carpetas
No pongas todo en `main.py`. Divide y vencerás:
```text
app/
├── core/       # Lo que no cambia (Configuración, Base de Datos)
├── models/     # Cómo se ven los datos en la BD (Tablas)
├── schemas/    # Cómo se ven los datos en la API (JSON Pydantic)
├── routers/    # Las URLs de tu API (@router.get)
├── services/   # La lógica pesada (Cálculos, Guardar en BD)
└── main.py     # El pegamento que une todo
```

### 3. Configuración Segura (Pydantic Settings)
Nunca escribas claves o contraseñas en el código.
- **Herramienta**: `pydantic-settings`.
- **Cómo funciona**: Lee un archivo `.env` (que nunca subes a Git) y lo convierte en variables de Python con tipos validados.

---

## Fase 2: Base de Datos (SQLAlchemy y Docker)

### 1. El Contenedor (Docker)
En lugar de instalar PostgreSQL en tu Windows, usamos Docker.
- **Archivo**: `docker-compose.yml`.
- **Ventaja**: "Infraestructura como Código". Con un comando (`docker compose up`) tienes la base de datos lista, idéntica para todos los desarrolladores.

### 2. El ORM (SQLAlchemy)
No escribimos SQL a mano (`SELECT * FROM...`). Usamos objetos Python.
- **Modelos (`models/user.py`)**: Clases que representan tablas.
- **Sesión (`core/database.py`)**: El gestor que mantiene la conexión abierta y segura.

### 3. Esquemas (Pydantic)
FastAPI necesita saber qué datos esperar y qué devolver.
- **Schema (`schemas/user.py`)**: Define qué campos entran (`UserCreate`) y cuáles salen (`UserResponse`). Esto filtra datos sensibles automáticamente.

### 4. Herramientas de Administración (pgAdmin)
Para ejecutar queries SQL y administrar la base de datos visualmente:
- **Servicio**: Agregado en `docker-compose.yml`.
- **Acceso**: http://localhost:5050
- **Configuración**: Host `db`, Puerto `5432` (interno de Docker).

---

## Fase 3: Creando un Nuevo Módulo (Ej: Usuarios)

Si quieres agregar otra funcionalidad (ej: "Productos"), sigue estos pasos:

1.  **Modelo**: Crea `app/models/producto.py`. Define la tabla.
2.  **Esquema**: Crea `app/schemas/producto.py`. Define el JSON.
3.  **Servicio**: Crea `app/services/producto_service.py`. Haz las funciones `crear_producto`, `obtener_producto`.
4.  **Router**: Crea `app/routers/productos.py`. Define los endpoints HTTP (`POST /productos`, `GET /productos`) y llama al servicio.
5.  **Registro**: Ve a `app/main.py` y agrega `app.include_router(productos.router)`.

---

## Fase 4: Despliegue y Pruebas

### 1. Docker Multistage
En el `Dockerfile`, usamos dos etapas:
1.  **Builder**: Instala todo y compila.
2.  **Runtime**: Copia solo lo necesario.
**Resultado**: Una imagen muy ligera y segura para producción.

### 2. Pruebas Automatizadas
Usamos `pytest`.
- Crea archivos `test_*.py` en la carpeta `tests/`.
- Usa `TestClient` de FastAPI para simular peticiones reales sin levantar el servidor.

---

## Conceptos Clave Explicados

### ¿Qué es `lifespan`?
Es un gestor de eventos del ciclo de vida de FastAPI:
- **Startup**: Código que se ejecuta cuando la app arranca (ej: crear tablas).
- **Shutdown**: Código que se ejecuta cuando la app se apaga (ej: cerrar conexiones).

**Ventaja**: Evita que el código se ejecute al importar el módulo (importante para tests).

### Puertos en Docker
- **Puerto externo**: El que usas desde tu máquina (`localhost:5433`).
- **Puerto interno**: El que usan los contenedores entre sí (`db:5432`).

**Ejemplo**: `5433:5432` significa "mapea el puerto 5433 de mi PC al puerto 5432 del contenedor".

---

## Resumen de Comandos Útiles

| Acción | Comando |
| :--- | :--- |
| Instalar todo | `poetry install` |
| Levantar BD y App | `docker compose up --build` |
| Correr Tests | `poetry run pytest` |
| Agregar librería | `poetry add nombre_libreria` |
| Acceder a PostgreSQL | `docker exec -it qrgenerator-db-1 psql -U postgres -d qrdb` |
| Ver logs de contenedor | `docker logs qrgenerator-qr-generator-1` |

---

## Próximos Pasos Profesionales

1. **Migraciones con Alembic**: Para manejar cambios en la base de datos de forma controlada.
2. **Autenticación JWT**: Para proteger endpoints con tokens.
3. **CI/CD**: Automatizar tests y despliegues con GitHub Actions.
4. **Monitoreo**: Agregar logs estructurados y métricas.
