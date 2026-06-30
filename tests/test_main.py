from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_health_check() -> None:
    """Valida se o endpoint de health check está respondendo corretamente."""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}