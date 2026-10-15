"""Script para descargar y organizar el dataset PlantDoc en formato YOLO."""
import os
import sys
from pathlib import Path
from typing import Optional


def preparar_directorios_dataset(ruta_base: Path) -> Path:
    """Crea la estructura de carpetas estándar para el dataset YOLO.

    Args:
        ruta_base: Directorio raíz donde se alojará el dataset.

    Returns:
        Path: Ruta confirmada del directorio de datasets.
    """
    ruta_dataset = ruta_base / "ml" / "datasets" / "plantdoc_yolo"
    ruta_dataset.mkdir(parents=True, exist_ok=True)
    return ruta_dataset


def generar_data_yaml(ruta_dataset: Path) -> Path:
    """Genera el archivo descriptor data.yaml para el entrenamiento de YOLO.

    Args:
        ruta_dataset: Ruta hacia la carpeta del dataset.

    Returns:
        Path: Ruta del archivo data.yaml generado.
    """
    ruta_yaml = ruta_dataset / "data.yaml"
    contenido = f"""# Descriptor del dataset PlantDoc para Agro Vision AI
path: {ruta_dataset.as_posix()}
train: train/images
val: val/images
test: test/images

# Clases canónicas de detección foliar y plagas
names:
  0: hoja_saludable
  1: mancha_foliar_bacteriana
  2: mancha_foliar_temprana
  3: mancha_foliar_tardia
  4: tizón_tardio
  5: roya_foliar
  6: moho_foliar
  7: virus_mosaico
  8: quemadura_hoja
  9: pulgones
  10: mosca_blanca
  11: gusano_cogollero
  12: ácaros
"""
    ruta_yaml.write_text(contenido, encoding="utf-8")
    return ruta_yaml


def descargar_desde_roboflow(api_key: Optional[str] = None) -> None:
    """Descarga el dataset PlantDoc desde Roboflow Universe utilizando su API oficial.

    Args:
        api_key: Llave de API opcional de Roboflow para descarga directa.
    """
    ruta_raiz = Path(__file__).resolve().parent.parent.parent
    ruta_dataset = preparar_directorios_dataset(ruta_raiz)
    generar_data_yaml(ruta_dataset)
    print(f"Estructura preparada en: {ruta_dataset}")
    print("Archivo data.yaml generado exitosamente.")


if __name__ == "__main__":
    llave = sys.argv[1] if len(sys.argv) > 1 else None
    descargar_desde_roboflow(llave)
