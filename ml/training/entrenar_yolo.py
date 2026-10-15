"""Script para entrenar YOLOv8 con aceleración de GPU NVIDIA (RTX 2060)."""
import os
from pathlib import Path
from typing import Dict, Union


def verificar_dispositivo_cuda() -> str:
    """Verifica si CUDA está disponible para aprovechar la tarjeta gráfica RTX 2060.

    Returns:
        str: '0' si la GPU está disponible, o 'cpu' en caso contrario.
    """
    try:
        import torch
        if torch.cuda.is_available():
            nombre_gpu = torch.cuda.get_device_name(0)
            print(f"[GPU DETECTADA] Acelerando con: {nombre_gpu}")
            return "0"
        print("[AVISO] CUDA no disponible. Se utilizará la CPU.")
        return "cpu"
    except ImportError:
        print("[ERROR] PyTorch no encontrado.")
        return "cpu"


def ejecutar_entrenamiento(
    epocas: int = 50,
    tamaño_imagen: int = 640,
    tamaño_lote: int = 16,
) -> None:
    """Ejecuta el ciclo de fine-tuning de YOLOv8 Nano sobre el dataset PlantDoc.

    Args:
        epocas: Cantidad de iteraciones completas sobre el dataset.
        tamaño_imagen: Resolución de entrada en píxeles (default 640x640).
        tamaño_lote: Tamaño de lote adaptado a los 6GB VRAM de la RTX 2060.
    """
    try:
        from ultralytics import YOLO
    except ImportError:
        print("[ERROR] Ultralytics no instalado. Ejecuta: pip install ultralytics")
        return

    ruta_raiz = Path(__file__).resolve().parent.parent.parent
    ruta_yaml = ruta_raiz / "ml" / "datasets" / "plantdoc_yolo" / "data.yaml"

    if not ruta_yaml.exists():
        print(f"[ERROR] No se encontró el descriptor: {ruta_yaml}")
        print("Ejecuta primero: python ml/training/descargar_plantdoc.py")
        return

    dispositivo = verificar_dispositivo_cuda()

    # Cargar modelo base YOLOv8 Nano pre-entrenado
    modelo = YOLO("yolov8n.pt")

    # Iniciar entrenamiento con precisión mixta (half/fp16) ideal para RTX 2060
    print(f"[INICIANDO ENTRENAMIENTO] Épocas: {epocas} | Batch: {tamaño_lote} | Dispositivo: {dispositivo}")
    modelo.train(
        data=str(ruta_yaml),
        epochs=epocas,
        imgsz=tamaño_imagen,
        batch=tamaño_lote,
        device=dispositivo,
        workers=2,
        half=True if dispositivo != "cpu" else False,
        project=str(ruta_raiz / "runs" / "detect"),
        name="plantdoc_yolov8n",
        save=True,
        exist_ok=True,
    )

    # Copiar mejores pesos a ml/models/
    ruta_mejores_pesos = ruta_raiz / "runs" / "detect" / "plantdoc_yolov8n" / "weights" / "best.pt"
    ruta_destino = ruta_raiz / "ml" / "models" / "yolov8n_plagas.pt"

    if ruta_mejores_pesos.exists():
        import shutil
        shutil.copy(ruta_mejores_pesos, ruta_destino)
        print(f"[EXITO] Modelo entrenado copiado a: {ruta_destino}")


if __name__ == "__main__":
    import sys
    num_epocas = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    ejecutar_entrenamiento(epocas=num_epocas)
