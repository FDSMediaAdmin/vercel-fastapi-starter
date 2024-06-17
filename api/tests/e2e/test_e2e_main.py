import time

import pytest

import subprocess
import time
import pytest
import requests
from api.config.config import settings



@pytest.fixture(scope="session", autouse=True)
def start_server():
    process = subprocess.Popen(["sh", "api/tests/helper/run_server.sh"])

    # Wait for the server to start
    time.sleep(5)

    # Ensure the server is running
    for _ in range(10):
        try:
            response = requests.get("http://localhost:8000")
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            time.sleep(1)


    yield

    process.terminate()



def test_main_create_e2e():
    response = requests.post(f"{settings.API_V1_PREFIX}/main/create")
    print('test_main_create_e2e: response', response)
    assert response.status_code == 200
    assert response.json() == {"message": "main_create: Message sent"}



def test_main_read_e2e():
    response = requests.get(f"{settings.API_V1_PREFIX}/main/read")
    assert response.status_code == 200
    assert response.json() == {"message": "main_read: Message sent"}
