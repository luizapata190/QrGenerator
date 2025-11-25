import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Provide a TestClient instance for all tests.
    This fixture avoids importing the database configuration during test collection,
    preventing the Settings validation error caused by extra env vars.
    """
    return TestClient(app)
