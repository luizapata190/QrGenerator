from app.core.config import settings

def test_public_endpoint(client):
    # GET /users/ es público
    response = client.get("/users/")
    assert response.status_code == 200

def test_protected_endpoint_no_key(client):
    # POST /users/ está protegido
    response = client.post(
        "/users/",
        json={"cedula": "123", "nombre": "Test", "email": "test@test.com"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "API Key requerida. Incluir header: X-API-Key"

def test_protected_endpoint_invalid_key(client):
    response = client.post(
        "/users/",
        json={"cedula": "123", "nombre": "Test", "email": "test@test.com"},
        headers={"X-API-Key": "invalid-key"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "API Key inválida"

def test_protected_endpoint_valid_key(client):
    # Usamos una cédula única para evitar error 400
    # Si la autenticación pasa, deberíamos recibir 200 o 400 (si ya existe), pero NO 401/403
    response = client.post(
        "/users/",
        json={"cedula": "999999_auth_test", "nombre": "Test Auth", "email": "auth@test.com"},
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code in [200, 400]
