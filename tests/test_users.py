from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db

# Configuración de base de datos en memoria para pruebas (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        json={"cedula": "123456789", "nombre": "Test User", "email": "test@example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["cedula"] == "123456789"
    assert data["nombre"] == "Test User"
    assert "id" in data

def test_create_user_duplicate_cedula():
    # Intentar crear el mismo usuario de nuevo
    response = client.post(
        "/users/",
        json={"cedula": "123456789", "nombre": "Test User 2", "email": "test2@example.com"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "La cédula ya está registrada"

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_read_user_by_cedula():
    response = client.get("/users/123456789")
    assert response.status_code == 200
    data = response.json()
    assert data["cedula"] == "123456789"
    assert data["nombre"] == "Test User"

def test_read_user_not_found():
    response = client.get("/users/999999999")
    assert response.status_code == 404
