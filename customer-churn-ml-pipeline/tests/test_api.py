# Import TestClient
from fastapi.testclient import TestClient

from api.main import app


# Test API health endpoint
def test_health_endpoint():

    with TestClient(app) as client:

        response = client.get("/health")

        assert response.status_code == 200

        assert response.json()["status"] == "ok"