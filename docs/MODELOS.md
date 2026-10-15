# Catálogo de Modelos y Optimización

## 1. Modelos Disponibles

| Modelo | Arquitectura | Entrada | Propósito | Latencia CPU | Latencia GPU |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `yolov8n_plagas.pt` | YOLOv8 Nano | 640x640 | Detección en tiempo real en video | ~45 ms | ~8 ms |
| `yolov11n_plagas.pt`| YOLOv11 Nano| 640x640 | Detección de alta precisión y bajo peso | ~40 ms | ~7 ms |
| `mobilenet_v3_enfermedades.onnx` | MobileNetV3 Small | 224x224 | Clasificación de tipo de enfermedad | ~15 ms | ~3 ms |

---

## 2. Exportación a ONNX para Inferencia Ultrarrápida

Para desplegar en servidores sin dependencias pesadas de PyTorch, exportar los modelos a **ONNX Runtime**:

```python
from ultralytics import YOLO

modelo = YOLO("ml/models/yolov8n_plagas.pt")
modelo.export(format="onnx", dynamic=True, simplify=True)
```

---

## 3. Repositorio de Pesos (Hugging Face)

Los pesos preentrenados del modelo YOLOv8n están almacenados en el repositorio oficial de Hugging Face:
* **Repositorio:** `https://huggingface.co/DreX09/yolov8n-agrovision-plagas`
* **Ubicación local esperada:** `ml/models/yolov8n_plagas.pt`

Para descargar los pesos y colocarlos en el entorno local:
```bash
# Descarga directa y colocación en el directorio de modelos
curl -L -o ml/models/yolov8n_plagas.pt https://huggingface.co/DreX09/yolov8n-agrovision-plagas/resolve/main/yolov8n_plagas.pt
```