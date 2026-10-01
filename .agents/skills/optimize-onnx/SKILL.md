---
name: optimize-onnx
description: "Trigger: exportar onnx, optimizar modelo, acelerar inferencia, onnx runtime. Guía para exportar y optimizar modelos para producción."
license: Apache-2.0
metadata:
  author: "agro-vision-team"
  version: "1.0"
---

# Procedimiento: Optimización y Exportación a ONNX

## Pasos de Ejecución
1. Cargar el modelo entrenado con Ultralytics.
2. Exportar con dimensión dinámica de batch:
   ```python
   from ultralytics import YOLO
   modelo = YOLO("ml/models/yolov8n_plagas.pt")
   modelo.export(format="onnx", dynamic=True, simplify=True)
   ```
3. Validar la inferencia con `onnxruntime` para asegurar que las salidas coincidan con el modelo original.
4. Ubicar el archivo `.onnx` en `ml/models/`.