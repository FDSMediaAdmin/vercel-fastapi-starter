import pytest
from fastapi.testclient import TestClient
from api.app import app
from api.config.config import settings

client = TestClient(app)


@pytest.fixture(scope="module")
def test_app():
    """
    Fixture for setting up and tearing down the FastAPI application.
    """
    with TestClient(app) as test_client:
        yield test_client


def test_main_create_integration(test_app):
    response = test_app.post("/v1_0/main/create")
    assert response.status_code == 200
    assert response.json() == {"message": "main_create: Message sent"}
    # Add more integration tests as needed


def test_main_read_integration(test_app):
    response = test_app.get("/v1_0/main/read")
    assert response.status_code == 200
    assert response.json() == {"message": "main_read: Message sent"}
    # Add more integration tests as needed


def test_external_service_integration():
    # Example test interacting with external services (mocked or real)
    assert settings.integrations.sentry.dsn is not None
    # Add more tests for other external services or integrations
