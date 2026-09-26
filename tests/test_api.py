from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_latest_market_data():
    response = client.get("/api/v1/market/latest")
    assert response.status_code == 200
    assert isinstance(response.json(), list)