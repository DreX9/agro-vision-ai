---
name: train-model
description: "Trigger: entrenar modelo, fine-tuning yolo, entrenar plagas, dataset training, ml training. Procedimiento para entrenar y evaluar modelos YOLO en Agro Vision AI."
license: Apache-2.0
metadata:
  author: "agro-vision-team"
  version: "1.0"
---

# Procedimiento: Entrenar Modelo de Detección

## Pasos de Ejecución
1. Asegurar que el dataset esté organizado en `ml/datasets/plagas_yolo/` con su `data.yaml`.
2. Ejecutar el entrenamiento con Ultralytics:
   ```bash
   yolo detect train data=ml/datasets/plagas_yolo/data.yaml model=yolov8n.pt epochs=50 imgsz=640 batch=16
   ```
3. Evaluar métricas de rendimiento:
   * **mAP@0.5:** Debe superar el 85% para plagas frecuentes.
   * **Recall:** Priorizar alto recall para no omitir plagas críticas.
4. Mover los mejores pesos generados (`runs/detect/train/weights/best.pt`) a `ml/models/yolov8n_plagas.pt`.
5. Ejecutar la validación de inferencia con Pytest.