from fastapi.testclient import TestClient
from main import app

client = TestClient(app)  # server is up


def test_health_endpoint_is_public():
    response = client.get("/health")  # health endpoint added in main.py
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
