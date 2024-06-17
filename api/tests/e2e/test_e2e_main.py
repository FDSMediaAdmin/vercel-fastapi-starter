import time

import pytest
from starlette.testclient import TestClient
from requests import Session

from api.app import app
from requests import Session
from api.config.config import settings



@pytest.fixture(scope="function")  # Create a fixture per test function
def app_and_session():
     """Creates a new FastAPI app instance, a TestClient, and a Session object for each test."""
     with TestClient(app) as test_client:
        session = Session()
        yield test_client, session


# Tear down (optional):
    #  - Close connections
    #  - Clean up resources specific to the app instance

    # Tear down (optional):
    #  - Close connections
    #  - Clean up resources specific to the app instance


def test_main_create_e2e(app_and_session):
    app, session = app_and_session  # Unpack fixture values
    time.sleep(60)

    response = session.post(f"{settings.API_V1_PREFIX}/main/create")

    assert response.status_code == 200
    assert response.json() == {"message": "main_create: Message sent"}


def test_main_read_e2e(app_and_session):
    app, session = app_and_session
    response = session.get(f"{settings.API_V1_PREFIX}/main/read")
    assert response.status_code == 200
    assert response.json() == {"message": "main_read: Message sent"}


def test_external_service_e2e(app_and_session):
    app, session = app_and_session
    assert settings.integrations.sentry.dsn is not None  # Assert external service config
