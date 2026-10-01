# Arquitectura del Sistema - Agro Vision AI

## 1. Visión General
* **Microservicio:** Motor de Visión Computacional e Inferencia de Modelos Agrícolas.
* **Framework Web:** FastAPI (Asíncrono, OpenAPI Swagger interactivo en `/docs`).
* **Modelos de Visión:**
  * **Detección en Video y Cámara:** YOLOv8 / YOLOv11 (Ultralytics) para localización espacial de plagas y anomalías con *bounding boxes*.
  * **Clasificación de Hojas:** MobileNetV3 / EfficientNet para categorización de salud foliar y patógenos.
* **Aceleración de Inferencia:** PyTorch / ONNX Runtime (CPU y GPU CUDA).

---

## 2. Estructura de Directorios

```text
agro-vision-ai/
├── api/                              # Capa de Servicio API REST (FastAPI)
│   ├── core/                         # Configuración central (Settings, logging)
│   │   ├── config.py
│   │   └── logging.py
│   ├── routers/                      # Controladores / Endpoints REST
│   │   ├── diagnostico_router.py     # /api/v1/diagnosticos/analizar-imagen & analizar-video
│   │   ├── deteccion_router.py       # /api/v1/detecciones/plagas
│   │   └── salud_router.py           # /api/v1/salud (Health check)
│   ├── schemas/                      # Modelos de datos Pydantic v2
│   │   └── diagnostico_schema.py     # Request/Response DTOs
│   └── main.py                       # Instancia de FastAPI y ciclo de vida (Lifespan)
├── ml/                               # Núcleo de Inteligencia Artificial y Visión
│   ├── inference/                    # Pipelines de preprocesamiento e inferencia
│   │   ├── detector_plagas.py        # Wrapper YOLO para detección de objetos
│   │   ├── clasificador_hojas.py     # Wrapper MobileNetV3 para clasificación foliar
│   │   └── procesador_video.py       # Extracción y muestreo inteligente de frames
│   ├── models/                       # Pesos de modelos (.pt, .onnx)
│   └── training/                     # Scripts de entrenamiento y aumentación
├── docs/                             # Documentación de ML y Datasets
│   ├── DATASET.md                    # Guía de etiquetado y clases
│   └── MODELOS.md                    # Métricas de precisión (mAP, F1) y exportación
├── tests/                            # Pruebas unitarias con Pytest
├── requirements.txt                  # Dependencias del proyecto
└── .env.example                      # Variables de entorno
```

---

## 3. Flujo de Datos y Pipeline de Inferencia

1. **Recepción:** FastAPI recibe una imagen (JPEG/PNG) o un video corto (MP4/WebM) vía multipart/form-data.
2. **Preprocesamiento (`ml/inference/`):**
   * Redimensionamiento adaptativo (`640x640` para YOLO).
   * Normalización de color y corrección de brillo/contraste si aplica.
   * Si es video: Extracción de frames clave a razón de 3 a 5 FPS para evitar procesamiento redundante.
3. **Inferencia:**
   * Ejecución del modelo YOLO para obtener recuadros, etiquetas y confianza.
   * Ejecución del clasificador MobileNet para determinar el diagnóstico general de la hoja.
4. **Postprocesamiento:**
   * Filtrado por umbral de confianza (*confidence threshold* >= 0.45).
   * Supresión de No Máximos (NMS) para eliminar recuadros duplicados.
   * Asociación con recomendaciones agronómicas.
5. **Respuesta:** Retorno de payload JSON estructurado consumible por `agro-vision-backend`.