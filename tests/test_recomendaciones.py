"""Pruebas unitarias para el catálogo de recomendaciones estructuradas y herramientas."""
import io

from fastapi.testclient import TestClient
from PIL import Image

from api.main import app
from ml.inference.traductor_plagas import generar_recomendaciones_agronomicas
from ml.knowledge.catalogo_fichas import (
    clasificar_patologia_por_nombre,
    obtener_ficha_follaje_sano,
    obtener_fichas_tecnicas,
)

client = TestClient(app)


def test_ficha_tecnica_follaje_saludable() -> None:
    """Verifica que la ficha de follaje sano contenga todas las categorías requeridas."""
    ficha = obtener_ficha_follaje_sano()

    assert ficha.patologia == "Follaje Saludable y Vigor Vegetativo Óptimo"
    assert len(ficha.accion_inmediata) > 0
    assert len(ficha.control_biologico) > 0
    assert len(ficha.control_quimico) > 0
    assert len(ficha.manejo_preventivo) > 0
    assert len(ficha.herramientas_sugeridas) > 0
    assert any("Lupa" in h or "registro" in h for h in ficha.herramientas_sugeridas)


def test_catalogo_fichas_tizon_temprano() -> None:
    """Valida la generación de ficha técnica y herramientas para tizón temprano."""
    fichas = obtener_fichas_tecnicas(["tomato early blight leaf"])

    assert len(fichas) == 1
    ficha = fichas[0]
    assert "Tizón Temprano" in ficha.patologia
    assert any("Oxicloruro de Cobre" in q for q in ficha.control_quimico)
    assert any("Trichoderma" in b for b in ficha.control_biologico)
    assert any("Tijeras" in h for h in ficha.herramientas_sugeridas)
    assert any("Pulverizador" in h or "mochila" in h for h in ficha.herramientas_sugeridas)


def test_catalogo_fichas_deduplicacion() -> None:
    """Verifica que múltiples detecciones de la misma patología no dupliquen la ficha."""
    clases = [
        "tomato early blight leaf",
        "potato leaf early blight",
        "tomato early blight leaf",
    ]
    fichas = obtener_fichas_tecnicas(clases)
    assert len(fichas) == 1


def test_catalogo_fichas_multiples_patologias() -> None:
    """Verifica la generación de fichas distintas cuando hay varias enfermedades presentes."""
    clases = [
        "tomato early blight leaf",
        "tomato two spotted spider mites leaf",
        "squash powdery mildew leaf",
    ]
    fichas = obtener_fichas_tecnicas(clases)

    assert len(fichas) == 3
    patologias = [f.patologia for f in fichas]
    assert any("Tizón Temprano" in p for p in patologias)
    assert any("Ácaros" in p or "Arañita" in p for p in patologias)
    assert any("Oídio" in p or "Mildiu" in p for p in patologias)


def test_clasificacion_todas_las_patologias() -> None:
    """Verifica que el clasificador mapee correctamente los diferentes patrones."""
    assert clasificar_patologia_por_nombre("apple rust leaf") == "roya"
    assert clasificar_patologia_por_nombre("potato leaf late blight") == "tizon_tardio"
    assert clasificar_patologia_por_nombre("tomato leaf mosaic virus") == "virosis"
    assert clasificar_patologia_por_nombre("grape leaf black rot") == "afeccion_fungica_compleja"
    assert clasificar_patologia_por_nombre("bell_pepper leaf spot") == "mancha_foliar"


def test_generar_recomendaciones_integracion() -> None:
    """Verifica la tupla completa retornada por generar_recomendaciones_agronomicas."""
    estado, salud, recomendaciones, fichas = generar_recomendaciones_agronomicas(
        ["tomato late blight leaf"]
    )

    assert estado == "ALERTA"
    assert salud <= 80.0
    assert len(recomendaciones) > 0
    assert len(fichas) == 1
    assert "Tizón Tardío" in fichas[0].patologia
    assert len(fichas[0].herramientas_sugeridas) > 0


def test_endpoint_imagen_retorna_fichas_tecnicas_y_herramientas() -> None:
    """Verifica que el endpoint HTTP responda con el esquema enriquecido."""
    imagen = Image.new("RGB", (640, 640), color=(50, 160, 50))
    buffer = io.BytesIO()
    imagen.save(buffer, format="JPEG")
    buffer.seek(0)

    archivos = {"archivo": ("muestra_cultivo.jpg", buffer.getvalue(), "image/jpeg")}
    response = client.post("/api/v1/diagnosticos/analizar-imagen", files=archivos)

    assert response.status_code == 200
    datos = response.json()

    assert "fichas_tecnicas" in datos
    assert isinstance(datos["fichas_tecnicas"], list)
    assert len(datos["fichas_tecnicas"]) >= 1

    primera_ficha = datos["fichas_tecnicas"][0]
    assert "patologia" in primera_ficha
    assert "accion_inmediata" in primera_ficha
    assert "control_biologico" in primera_ficha
    assert "control_quimico" in primera_ficha
    assert "manejo_preventivo" in primera_ficha
    assert "herramientas_sugeridas" in primera_ficha
    assert len(primera_ficha["herramientas_sugeridas"]) > 0
