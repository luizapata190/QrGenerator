# Decisiones de Diseño y Arquitectura - QR Generator API

## Tabla de Contenidos
1. [Visión General](#visión-general)
2. [Decisiones de Arquitectura](#decisiones-de-arquitectura)
3. [Decisiones de Tecnología](#decisiones-de-tecnología)
4. [Decisiones de Seguridad](#decisiones-de-seguridad)
5. [Decisiones de Base de Datos](#decisiones-de-base-de-datos)
6. [Decisiones de Despliegue](#decisiones-de-despliegue)
7. [Lecciones Aprendidas](#lecciones-aprendidas)

---

## Visión General

Este documento registra las decisiones técnicas importantes tomadas durante el desarrollo del proyecto QR Generator API, explicando el **por qué** detrás de cada elección y las alternativas consideradas.

---

## Decisiones de Arquitectura

### 1. Arquitectura en Capas

**Decisión:** Implementar una arquitectura de 3 capas (Presentación, Negocio, Datos).

**Razones:**
- ✅ **Separación de responsabilidades**: Cada capa tiene un propósito claro
- ✅ **Testeable**: Podemos probar servicios sin levantar el servidor HTTP
- ✅ **Reutilizable**: Los servicios pueden usarse desde CLI, workers, etc.
- ✅ **Mantenible**: Cambios en una capa no afectan a las demás

**Alternativas consideradas:**
- ❌ **Todo en routers**: Código difícil de mantener y probar
- ❌ **Arquitectura hexagonal**: Demasiado compleja para este proyecto

**Estructura implementada:**
```
app/
├── routers/    # Capa de Presentación (HTTP)
├── services/   # Capa de Negocio (Lógica)
├── models/     # Capa de Datos (ORM)
├── schemas/    # Validación (Pydantic)
└── core/       # Configuración compartida
```

### 2. Gestión del Ciclo de Vida con `lifespan`

**Decisión:** Usar el gestor de contexto `lifespan` para inicializar la base de datos.

**Razones:**
- ✅ **Evita ejecución al importar**: El código solo se ejecuta cuando la app arranca
- ✅ **Importante para tests**: Permite importar módulos sin efectos secundarios
- ✅ **Gestión de recursos**: Cierra conexiones correctamente al apagar

**Código:**
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    logger.info("Application shutting down")
```

**Alternativa rechazada:**
```python
# ❌ Esto se ejecuta al importar, causando problemas en tests
Base.metadata.create_all(bind=engine)
```

### 3. Dependency Injection para Base de Datos

**Decisión:** Usar `Depends(get_db)` para inyectar sesiones de base de datos.

**Razones:**
- ✅ **Gestión automática**: FastAPI cierra la sesión automáticamente
- ✅ **Testeable**: Podemos inyectar sesiones mock en tests
- ✅ **Thread-safe**: Cada request tiene su propia sesión

**Código:**
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)
```

---

## Decisiones de Tecnología

### 1. FastAPI vs Flask vs Django

**Decisión:** Usar **FastAPI**.

**Razones:**
- ✅ **Performance**: Basado en Starlette (ASGI), muy rápido
- ✅ **Documentación automática**: Swagger UI y ReDoc out-of-the-box
- ✅ **Validación**: Pydantic integrado para validación de datos
- ✅ **Type hints**: Aprovecha anotaciones de tipo de Python
- ✅ **Async nativo**: Soporte para operaciones asíncronas

**Comparación:**

| Característica | FastAPI | Flask | Django |
|----------------|---------|-------|--------|
| Performance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Documentación automática | ✅ | ❌ | ❌ |
| Validación de datos | ✅ (Pydantic) | ❌ | ✅ (Forms) |
| Curva de aprendizaje | Media | Baja | Alta |
| Async | ✅ Nativo | ⚠️ Limitado | ⚠️ Limitado |

### 2. SQLAlchemy vs Django ORM vs Raw SQL

**Decisión:** Usar **SQLAlchemy**.

**Razones:**
- ✅ **ORM maduro**: Ampliamente usado y probado
- ✅ **Flexibilidad**: Permite queries complejas cuando sea necesario
- ✅ **Independiente del framework**: No atado a Django
- ✅ **Migraciones**: Compatible con Alembic

**Ejemplo de ventaja:**
```python
# ✅ SQLAlchemy - Legible y seguro
users = db.query(User).filter(User.cedula == cedula).first()

# ❌ Raw SQL - Propenso a SQL injection
cursor.execute(f"SELECT * FROM users WHERE cedula = '{cedula}'")
```

### 3. Poetry vs pip vs conda

**Decisión:** Usar **Poetry**.

**Razones:**
- ✅ **Gestión de dependencias determinista**: `poetry.lock` asegura versiones exactas
- ✅ **Resolución de conflictos**: Detecta incompatibilidades antes de instalar
- ✅ **Publicación simplificada**: `poetry publish` para subir a PyPI
- ✅ **Entornos virtuales automáticos**: Crea y gestiona venvs

**Comparación:**

| Característica | Poetry | pip + venv | conda |
|----------------|--------|------------|-------|
| Lock file | ✅ | ❌ | ✅ |
| Resolución de dependencias | ✅ | ⚠️ | ✅ |
| Velocidad | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Ecosistema Python | ✅ | ✅ | ⚠️ (Anaconda) |

### 4. PostgreSQL vs MySQL vs MongoDB

**Decisión:** Usar **PostgreSQL**.

**Razones:**
- ✅ **ACID completo**: Transacciones confiables
- ✅ **Tipos de datos avanzados**: JSON, Arrays, UUID
- ✅ **Performance**: Excelente para lecturas y escrituras concurrentes
- ✅ **Extensiones**: PostGIS, pg_trgm, etc.
- ✅ **Open source**: Sin restricciones de licencia

**Caso de uso:**
```python
# PostgreSQL soporta tipos avanzados nativamente
class User(Base):
    metadata_json = Column(JSON)  # ✅ Tipo JSON nativo
    tags = Column(ARRAY(String))  # ✅ Arrays nativos
```

---

## Decisiones de Seguridad

### 1. API Key en Headers vs Query Params

**Decisión:** Usar **headers** (`X-API-Key`).

**Razones:**
- ✅ **No se registra en logs**: Los query params aparecen en logs de servidor
- ✅ **No se cachea**: Los headers no se guardan en caché del navegador
- ✅ **Estándar de la industria**: AWS, Stripe, etc. usan headers

**Ejemplo:**
```python
# ✅ Correcto
headers = {"X-API-Key": "mi_clave_secreta"}
response = requests.post(url, headers=headers)

# ❌ Incorrecto - La clave queda en logs
response = requests.post(f"{url}?api_key=mi_clave_secreta")
```

### 2. Pydantic Settings con `extra="ignore"`

**Decisión:** Permitir variables de entorno adicionales sin errores.

**Razones:**
- ✅ **Flexibilidad**: Permite variables para otros servicios (pgAdmin, Docker)
- ✅ **Evita errores**: No falla si hay variables no declaradas
- ✅ **Separación de concerns**: Cada servicio usa sus propias variables

**Problema resuelto:**
```python
# ❌ Sin extra="ignore"
# Error: ValidationError si .env tiene PGADMIN_DEFAULT_EMAIL

# ✅ Con extra="ignore"
model_config = SettingsConfigDict(env_file=".env", extra="ignore")
# Ignora variables no declaradas en Settings
```

### 3. SQLite en Tests vs PostgreSQL en Tests

**Decisión:** Usar **SQLite en memoria** para tests.

**Razones:**
- ✅ **Velocidad**: Tests 10x más rápidos
- ✅ **Aislamiento**: Cada test tiene su propia BD
- ✅ **Sin dependencias**: No requiere PostgreSQL corriendo
- ✅ **CI/CD**: Funciona en cualquier entorno

**Implementación:**
```python
@property
def SQLALCHEMY_DATABASE_URI(self) -> str:
    if os.getenv("PYTEST_CURRENT_TEST"):
        return "sqlite:///:memory:"  # Tests
    return f"postgresql://..."  # Producción
```

---

## Decisiones de Base de Datos

### 1. Índices en Columnas de Búsqueda

**Decisión:** Crear índices en `cedula` y `email`.

**Razones:**
- ✅ **Performance**: Búsquedas 100x más rápidas
- ✅ **Unicidad**: `unique=True` previene duplicados
- ✅ **Costo bajo**: Overhead mínimo en inserts

**Código:**
```python
class User(Base):
    cedula = Column(String, unique=True, index=True)  # ✅ Índice
    email = Column(String, unique=True, index=True)   # ✅ Índice
    nombre = Column(String)  # ❌ Sin índice (no se busca frecuentemente)
```

### 2. Pool de Conexiones con `pool_pre_ping`

**Decisión:** Activar `pool_pre_ping=True`.

**Razones:**
- ✅ **Resiliencia**: Detecta conexiones muertas antes de usarlas
- ✅ **Evita errores**: Previene "server has gone away"
- ✅ **Costo bajo**: Ping es muy rápido

**Código:**
```python
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True  # ✅ Verifica conexiones
)
```

### 3. Gestión de Sesiones con `try/finally`

**Decisión:** Usar `get_db()` con `yield` para gestionar sesiones.

**Razones:**
- ✅ **Garantiza cierre**: `finally` siempre se ejecuta
- ✅ **Evita leaks**: No deja conexiones abiertas
- ✅ **Automático**: FastAPI gestiona el ciclo de vida

**Código:**
```python
def get_db():
    db = SessionLocal()
    try:
        yield db  # ✅ Se ejecuta el endpoint
    finally:
        db.close()  # ✅ Siempre se cierra
```

---

## Decisiones de Despliegue

### 1. Docker Multistage Build

**Decisión:** Usar build de dos etapas (builder + runtime).

**Razones:**
- ✅ **Imagen ligera**: Runtime solo contiene lo necesario
- ✅ **Seguridad**: No incluye herramientas de compilación
- ✅ **Velocidad**: Caché de capas acelera rebuilds

**Comparación de tamaños:**
- ❌ Single-stage: ~1.2 GB
- ✅ Multi-stage: ~400 MB

**Dockerfile:**
```dockerfile
# Etapa 1: Builder (se descarta)
FROM python:3.12-slim as builder
RUN pip install poetry
RUN poetry install

# Etapa 2: Runtime (imagen final)
FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
```

### 2. Volúmenes para Persistencia de Datos

**Decisión:** Usar volúmenes Docker para PostgreSQL.

**Razones:**
- ✅ **Persistencia**: Datos sobreviven a reinicios de contenedores
- ✅ **Performance**: Mejor que bind mounts
- ✅ **Portabilidad**: Fácil de respaldar y migrar

**docker-compose.yml:**
```yaml
services:
  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data/  # ✅ Volumen nombrado

volumes:
  postgres_data:  # ✅ Declaración del volumen
```

### 3. Variables de Entorno con Valores por Defecto

**Decisión:** Usar `${VAR:-default}` en docker-compose.

**Razones:**
- ✅ **Flexibilidad**: Funciona sin `.env` (desarrollo rápido)
- ✅ **Documentación**: Los defaults muestran valores esperados
- ✅ **Seguridad**: Producción puede sobrescribir con valores seguros

**Ejemplo:**
```yaml
environment:
  - POSTGRES_USER=${POSTGRES_USER:-postgres}  # Default: postgres
  - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
```

---

## Lecciones Aprendidas

### 1. Problema: Tests Colgados

**Síntoma:** `poetry run pytest` se quedaba esperando indefinidamente.

**Causa:** `conftest.py` importaba `app.main`, que ejecutaba `Base.metadata.create_all()` al importar, intentando conectar a PostgreSQL.

**Solución:**
1. Mover creación de tablas a `lifespan` (solo se ejecuta al arrancar app)
2. Usar SQLite en memoria para tests (detectado con `PYTEST_CURRENT_TEST`)
3. Simplificar `conftest.py` para solo proveer `TestClient`

**Lección:** Evitar efectos secundarios al importar módulos.

### 2. Problema: Error de Validación de Pydantic

**Síntoma:** `ValidationError` al iniciar la app con mensaje sobre `PGADMIN_DEFAULT_EMAIL`.

**Causa:** `.env` contenía variables para pgAdmin que no estaban declaradas en `Settings`.

**Solución:** Agregar `extra="ignore"` en `SettingsConfigDict`.

**Lección:** Usar `extra="ignore"` cuando múltiples servicios comparten `.env`.

### 3. Problema: Conexión Rechazada en Docker

**Síntoma:** `connection to server at "localhost" (::1), port 5432 failed: Connection refused`.

**Causa:** La app dentro de Docker intentaba conectar a `localhost` en vez de al servicio `db`.

**Solución:**
1. Cambiar `POSTGRES_SERVER=localhost` a `POSTGRES_SERVER=db` en `.env`
2. Cambiar puerto de `5433` a `5432` (puerto interno de Docker)

**Lección:** Dentro de Docker, usar nombres de servicios, no `localhost`.

### 4. Problema: Credenciales Hardcodeadas

**Síntoma:** Valores de usuario/contraseña directamente en `docker-compose.yml`.

**Causa:** Configuración inicial usaba valores fijos en vez de interpolación.

**Solución:** Cambiar a `${POSTGRES_USER:-postgres}` para leer de `.env`.

**Lección:** Siempre usar variables de entorno, incluso para valores "por defecto".

### 5. Problema: Puerto Inconsistente

**Síntoma:** Algunos archivos usaban `5432`, otros `5433`.

**Causa:** Confusión entre puerto interno (5432) y externo (5433).

**Solución:**
1. Unificar a `5432` para conexiones internas (Docker)
2. Mantener `5433` solo para acceso externo (host → contenedor)

**Lección:** Documentar claramente puertos internos vs externos.

---

## Decisiones Futuras a Considerar

### 1. Migraciones de Base de Datos

**Situación actual:** `Base.metadata.create_all()` crea tablas automáticamente.

**Problema:** No gestiona cambios de esquema (agregar columnas, etc.).

**Solución propuesta:** Implementar Alembic para migraciones versionadas.

**Ventajas:**
- ✅ Control de versiones de esquema
- ✅ Rollback de cambios
- ✅ Historial de migraciones

### 2. Caché con Redis

**Situación actual:** Cada request consulta la base de datos.

**Problema:** Queries repetitivos (ej: `GET /users/123456`).

**Solución propuesta:** Implementar caché con Redis.

**Ventajas:**
- ✅ Reduce carga en PostgreSQL
- ✅ Mejora tiempo de respuesta
- ✅ Escalabilidad

### 3. Rate Limiting

**Situación actual:** Sin límite de requests por cliente.

**Problema:** Vulnerable a abuso (DoS).

**Solución propuesta:** Implementar rate limiting con `slowapi`.

**Ventajas:**
- ✅ Protección contra abuso
- ✅ Mejor distribución de recursos
- ✅ Fácil de implementar

### 4. Monitoreo y Métricas

**Situación actual:** Solo logs en stdout.

**Problema:** Difícil detectar problemas en producción.

**Solución propuesta:** Integrar Prometheus + Grafana.

**Ventajas:**
- ✅ Métricas en tiempo real
- ✅ Alertas automáticas
- ✅ Dashboards visuales

---

## Conclusión

Las decisiones documentadas en este archivo reflejan un balance entre:
- **Simplicidad**: No sobre-ingeniería
- **Escalabilidad**: Preparado para crecer
- **Mantenibilidad**: Fácil de entender y modificar
- **Seguridad**: Protección de datos sensibles

Cada decisión fue tomada considerando el contexto del proyecto y las mejores prácticas de la industria. Este documento debe actualizarse cuando se tomen nuevas decisiones arquitectónicas importantes.

---

## Referencias

- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy Best Practices](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
- [The Twelve-Factor App](https://12factor.net/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
