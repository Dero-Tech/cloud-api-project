import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Cloud API is running"

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_info(client):
    response = client.get("/info")
    assert response.status_code == 200
    data = response.get_json()
    assert data["app"] == "Cloud Engineering Demo API"
    assert "tech_stack" in data
