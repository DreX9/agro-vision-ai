"""Pruebas unitarias para la API de Agro Vision AI."""
import io
from pathlib import Path
from PIL import Image
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_salud_endpoint() -> None:
    """Verifica que el endpoint de salud responda 200 y estado OPERATIVO."""
    response = client.get("/api/v1/salud")
    assert response.status_code == 200
    assert response.json()["estado"] == "OPERATIVO"


def test_analizar_imagen_hoja_saludable() -> None:
    """Verifica que una hoja sin anomalías retorne estado OPTIMO."""
    imagen = Image.new("RGB", (640, 640), color=(34, 139, 34))
    buffer = io.BytesIO()
    imagen.save(buffer, format="JPEG")
    buffer.seek(0)

    archivos = {"archivo": ("hoja_limpia.jpg", buffer.getvalue(), "image/jpeg")}
    response = client.post("/api/v1/diagnosticos/analizar-imagen", files=archivos)

    assert response.status_code == 200
    data = response.json()
    assert data["estado_general"] == "OPTIMO"
    assert data["salud_porcentaje"] >= 90.0
    assert isinstance(data["detecciones"], list)
    assert len(data["recomendaciones"]) > 0


def test_analizar_imagen_con_modelo_entrenado() -> None:
    """Verifica la inferencia con una imagen del dataset de validación si está disponible."""
    ruta_val = Path("ml/datasets/plantdoc_yolo/val/images")
    imagenes_val = list(ruta_val.glob("*.jpg")) if ruta_val.exists() else []

    if not imagenes_val:
        return

    primera_foto = imagenes_val[0]
    with open(primera_foto, "rb") as f:
        archivos = {"archivo": (primera_foto.name, f.read(), "image/jpeg")}
        response = client.post("/api/v1/diagnosticos/analizar-imagen", files=archivos)

    assert response.status_code == 200
    data = response.json()
    assert "estado_general" in data
    assert "salud_porcentaje" in data
    assert "tiempo_procesamiento_ms" in data
    assert data["tiempo_procesamiento_ms"] > 0