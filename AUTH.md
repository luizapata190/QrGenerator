# Guía de Autenticación y Seguridad

Esta API utiliza un sistema de seguridad basado en **API Keys** y **Logging Estructurado**.

## 🔑 Autenticación con API Key

Para acceder a los endpoints protegidos (como la creación de usuarios), debes incluir tu API Key en los headers de la petición.

### Header Requerido
```http
X-API-Key: <tu-clave-secreta>
```

### Configuración
La clave se configura en el archivo `.env` (no incluido en el repositorio):
```ini
API_KEY=tu-clave-secreta-min-32-chars
```

### Ejemplos de Uso

#### cURL
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-clave-secreta" \
  -d '{"cedula":"123","nombre":"Test","email":"test@test.com"}'
```

#### Python (Requests)
```python
import requests

url = "http://localhost:8000/users/"
headers = {
    "X-API-Key": "tu-clave-secreta",
    "Content-Type": "application/json"
}
data = {
    "cedula": "123",
    "nombre": "Test",
    "email": "test@test.com"
}

response = requests.post(url, json=data, headers=headers)
print(response.status_code)
```

#### Swagger UI
1. Ve a http://localhost:8000/docs
2. Haz clic en el botón **Authorize** (candado verde)
3. Ingresa tu API Key en el campo `value`
4. Haz clic en **Authorize** y luego **Close**
5. Ahora puedes ejecutar endpoints protegidos

---

## 📊 Logging Estructurado

El sistema genera logs en formato JSON para facilitar su integración con sistemas de monitoreo (como Datadog, CloudWatch, ELK).

### Formato del Log
```json
{
  "timestamp": "2025-11-25T17:00:00.123",
  "level": "INFO",
  "message": "Incoming request",
  "module": "logging_middleware",
  "method": "POST",
  "path": "/users/",
  "client": "127.0.0.1"
}
```

### Configuración
En el archivo `.env`:
```ini
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT=json # json o text
```
