# Diagrama de Arquitectura - QR Generator API

## Flujo de Datos de la Aplicación

```mermaid
graph TB
    subgraph "Cliente"
        Browser[🌐 Navegador/Cliente HTTP]
    end

    subgraph "FastAPI Application"
        subgraph "app/main.py"
            App[FastAPI App<br/>Punto de Entrada]
        end

        subgraph "app/routers/"
            QRRouter[qr.py<br/>Endpoints QR]
            UserRouter[users.py<br/>Endpoints Usuarios]
        end

        subgraph "app/services/"
            QRService[qr_service.py<br/>Lógica QR]
            UserService[user_service.py<br/>Lógica Usuarios]
        end

        subgraph "app/schemas/"
            UserSchema[user.py<br/>Validación Pydantic]
        end

        subgraph "app/models/"
            UserModel[user.py<br/>Modelo SQLAlchemy]
        end

        subgraph "app/core/"
            Config[config.py<br/>Configuración]
            Database[database.py<br/>Conexión DB]
        end
    end

    subgraph "Base de Datos"
        PostgreSQL[(PostgreSQL<br/>Puerto 5433)]
    end

    subgraph "Administración"
        pgAdmin[pgAdmin<br/>Puerto 5050]
    end

    Browser -->|HTTP Request| App
    App --> QRRouter
    App --> UserRouter
    
    QRRouter -->|Genera QR| QRService
    UserRouter -->|Valida con| UserSchema
    UserRouter -->|Llama a| UserService
    
    UserService -->|CRUD| UserModel
    UserModel -->|SQLAlchemy ORM| Database
    
    Database -->|Conexión| PostgreSQL
    Config -->|Variables de entorno| Database
    
    pgAdmin -.->|Administra| PostgreSQL

    style App fill:#4CAF50,color:#fff
    style QRRouter fill:#2196F3,color:#fff
    style UserRouter fill:#2196F3,color:#fff
    style QRService fill:#FF9800,color:#fff
    style UserService fill:#FF9800,color:#fff
    style PostgreSQL fill:#336791,color:#fff
    style pgAdmin fill:#336791,color:#fff
```

## Explicación del Flujo

### 1. **Cliente → Router** (Capa de Presentación)
```
GET /users/123456
     ↓
app/routers/users.py
```
- El cliente hace una petición HTTP
- FastAPI la enruta al router correspondiente
- El router valida los datos con Pydantic schemas

### 2. **Router → Service** (Capa de Negocio)
```
users.py → user_service.get_user_by_cedula()
```
- El router delega la lógica al servicio
- El servicio NO conoce HTTP, solo trabaja con datos Python

### 3. **Service → Model** (Capa de Datos)
```
user_service.py → User (SQLAlchemy Model)
                    ↓
                database.py (Session)
                    ↓
                PostgreSQL
```
- El servicio usa el modelo para interactuar con la BD
- SQLAlchemy traduce objetos Python a SQL

### 4. **Respuesta** (Camino inverso)
```
PostgreSQL → Model → Service → Router → Cliente (JSON)
```

## Ejemplo Concreto: Crear Usuario

```mermaid
sequenceDiagram
    participant C as Cliente
    participant R as users.py<br/>(Router)
    participant S as user_service.py<br/>(Service)
    participant M as User<br/>(Model)
    participant DB as PostgreSQL

    C->>R: POST /users/<br/>{cedula, nombre, email}
    R->>R: Valida con UserCreate schema
    R->>S: create_user(db, user_data)
    S->>S: Verifica si cedula existe
    S->>M: User(cedula, nombre, email)
    M->>DB: INSERT INTO users...
    DB-->>M: Usuario creado (id=1)
    M-->>S: Objeto User completo
    S-->>R: Usuario creado
    R->>R: Convierte a UserResponse
    R-->>C: JSON {id, cedula, nombre, email}
```

## Responsabilidades por Capa

| Capa | Carpeta | Responsabilidad | Conoce HTTP? | Conoce BD? |
|------|---------|-----------------|--------------|------------|
| **Presentación** | `routers/` | Recibir requests, validar, devolver responses | ✅ Sí | ❌ No |
| **Negocio** | `services/` | Lógica de la aplicación, reglas de negocio | ❌ No | ✅ Sí |
| **Datos** | `models/` | Estructura de las tablas, relaciones | ❌ No | ✅ Sí |
| **Configuración** | `core/` | Settings, conexión DB | ❌ No | ✅ Sí |
| **Validación** | `schemas/` | Formato de entrada/salida | ❌ No | ❌ No |

## Ventajas de esta Arquitectura

1. **Separación de Responsabilidades**: Cada capa tiene un trabajo específico
2. **Testeable**: Puedes probar servicios sin levantar el servidor HTTP
3. **Reutilizable**: Los servicios pueden usarse desde CLI, workers, etc.
4. **Mantenible**: Cambios en una capa no afectan a las demás
