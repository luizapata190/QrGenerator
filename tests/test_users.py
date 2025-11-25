from app.core.config import settings

def test_create_user(client):
    response = client.post(
        "/users/",
        json={"cedula": "123456789", "nombre": "Test User", "email": "test@example.com"},
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["cedula"] == "123456789"
    assert data["nombre"] == "Test User"
    assert "id" in data

def test_create_user_duplicate_cedula(client):
    # Intentar crear el mismo usuario de nuevo
    response = client.post(
        "/users/",
        json={"cedula": "123456789", "nombre": "Test User 2", "email": "test2@example.com"},
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "La cédula ya está registrada"

def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_read_user_by_cedula(client):
    response = client.get("/users/123456789")
    assert response.status_code == 200
    data = response.json()
    assert data["cedula"] == "123456789"
    assert data["nombre"] == "Test User"

def test_read_user_not_found(client):
    response = client.get("/users/999999999")
    assert response.status_code == 404
