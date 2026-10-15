"""Módulo de inferencia para detección de plagas y salud foliar usando YOLO."""
import io
import time
from pathlib import Path
from typing import List, Optional
from PIL import Image, ImageOps
from api.core.config import settings
from api.schemas.diagnostico_schema import (
    BoundingBoxDto,
    DeteccionPlagaDto,
    DiagnosticoRespuestaDto,
)
from ml.inference.traductor_plagas import (
    traducir_clase_a_espanol,
    generar_recomendaciones_agronomicas,
)


class DetectorPlagas:
    """Clase para ejecutar inferencia de visión computacional sobre imágenes."""

    def __init__(self, ruta_modelo: str = settings.MODELO_YOLO_PATH) -> None:
        """Inicializa el detector con la ruta configurada en entorno."""
        self.ruta_modelo = ruta_modelo
        self._modelo: Optional[object] = None

    def _descargar_modelo_remoto(self, destino: Path) -> bool:
        """Descarga los pesos preentrenados del modelo desde Hugging Face si no existen localmente.

        Args:
            destino: Ruta de almacenamiento local para los pesos del modelo.

        Returns:
            bool: True si la descarga fue exitosa o ya existía, False en caso de error.
        """
        if destino.exists():
            return True

        url_remota = getattr(settings, "URL_MODELO_HUGGINGFACE", "")
        if not url_remota:
            return False

        try:
            destino.parent.mkdir(parents=True, exist_ok=True)
            import urllib.request

            urllib.request.urlretrieve(url_remota, str(destino))
            return destino.exists()
        except Exception:
            return False

    def cargar_modelo(self) -> None:
        """Carga perezosa del modelo YOLOv8 para optimizar memoria."""
        if self._modelo is not None:
            return

        try:
            from ultralytics import YOLO

            ruta = Path(self.ruta_modelo)
            if not ruta.exists():
                self._descargar_modelo_remoto(ruta)

            if ruta.exists():
                self._modelo = YOLO(str(ruta))
            else:
                self._modelo = YOLO("yolov8n.pt")
        except Exception:
            self._modelo = None

    def detectar_en_imagen(self, imagen_bytes: bytes) -> DiagnosticoRespuestaDto:
        """Ejecuta la inferencia sobre una imagen y retorna el diagnóstico completo traducido.

        Args:
            imagen_bytes: Bytes en formato JPEG/PNG de la imagen enviada.

        Returns:
            DiagnosticoRespuestaDto: Diagnóstico estructurado en español con recuadros y recomendaciones.
        """
        inicio = time.time()
        self.cargar_modelo()

        detecciones: List[DeteccionPlagaDto] = []
        clases_originales: List[str] = []

        try:
            imagen_raw = Image.open(io.BytesIO(imagen_bytes))
            imagen = ImageOps.exif_transpose(imagen_raw).convert("RGB")

            # Guardar último escaneo recibido para depuración
            try:
                imagen.save("ml/last_scan.jpg", quality=90)
            except Exception:
                pass

            if self._modelo is not None:
                resultados = self._modelo(imagen, conf=settings.UMBRAL_CONFIANZA, verbose=False)
                if resultados and len(resultados) > 0:
                    cajas = resultados[0].boxes
                    if cajas is not None and len(cajas) > 0:
                        for box in cajas:
                            coords = box.xyxyn[0].tolist()
                            conf = float(box.conf[0])
                            clase_id = int(box.cls[0])
                            nombre_original = (
                                self._modelo.names.get(clase_id, "anomalia_foliar")
                                if hasattr(self._modelo, "names")
                                else "plaga_detectada"
                            )
                            clases_originales.append(nombre_original)
                            nombre_traducido = traducir_clase_a_espanol(nombre_original)

                            detecciones.append(
                                DeteccionPlagaDto(
                                    clase=nombre_traducido,
                                    confianza=round(conf, 3),
                                    caja=BoundingBoxDto(
                                        x_min=round(float(coords[0]), 4),
                                        y_min=round(float(coords[1]), 4),
                                        x_max=round(float(coords[2]), 4),
                                        y_max=round(float(coords[3]), 4),
                                    ),
                                )
                            )
        except Exception:
            pass

        # Generar recomendaciones agronómicas contextualizadas y cálculo de salud foliar
        estado_general, salud_porcentaje, recomendaciones = generar_recomendaciones_agronomicas(
            clases_originales
        )

        tiempo_ms = round((time.time() - inicio) * 1000, 2)

        return DiagnosticoRespuestaDto(
            estado_general=estado_general,
            salud_porcentaje=round(salud_porcentaje, 1),
            total_plagas_detectadas=len(detecciones),
            detecciones=detecciones,
            recomendaciones=recomendaciones,
            tiempo_procesamiento_ms=tiempo_ms,
        )


detector_plagas = DetectorPlagas()