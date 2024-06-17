import pytest
from unittest import mock
from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

# Mocking Sentry initialization
@pytest.fixture(autouse=True)
def mock_sentry_init():
    print('mock_sentry_init called')
    with mock.patch('sentry_sdk.init'):
        yield

@pytest.fixture(scope="module")
def test_app():
    """
    Fixture for setting up and tearing down the FastAPI application.
    """
    with TestClient(app) as test_client:
        yield test_client


def test_main_create(test_app):
    """
    Unit test for the /main/create endpoint.
    """
    response = test_app.post("/v1_0/main/create")
    assert response.status_code == 200
    assert response.json() == {"message": "main_create: Message sent"}


def test_main_read(test_app):
    """
    Unit test for the /main/read endpoint.
    """
    response = test_app.get("/v1_0/main/read")
    assert response.status_code == 200
    assert response.json() == {"message": "main_read: Message sent"}
