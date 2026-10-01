"""Pruebas unitarias básicas para la API de Agro Vision AI."""
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_salud_endpoint() -> None:
    """Verifica que el endpoint de salud responda 200 y estado OPERATIVO."""
    response = client.get("/api/v1/salud")
    assert response.status_code == 200
    assert response.json()["estado"] == "OPERATIVO"