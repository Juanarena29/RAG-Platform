from fastapi.testclient import TestClient

from app.main import app


# Test de health
def test_health_returns_ok() -> None:
    """Testea que el endpoint de health devuelve 200 OK."""
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
