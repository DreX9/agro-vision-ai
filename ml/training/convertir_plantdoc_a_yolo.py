"""Módulo para convertir las anotaciones de PlantDoc al formato estándar de YOLO."""
import csv
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple
from PIL import Image


def extraer_clases_desde_csv(ruta_csv: Path) -> List[str]:
    """Extrae la lista de clases únicas presentes en un archivo CSV de PlantDoc.

    Args:
        ruta_csv: Ruta al archivo train_labels.csv.

    Returns:
        List[str]: Lista de nombres de clases ordenadas alfabéticamente.
    """
    clases_set = set()
    with open(ruta_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clase = row.get("class", "").strip()
            if clase:
                clases_set.add(clase)
    return sorted(list(clases_set))


def convertir_csv_a_yolo(
    ruta_csv: Path,
    dir_imagenes_origen: Path,
    dir_destino_split: Path,
    mapa_clases: Dict[str, int],
) -> int:
    """Convierte un archivo CSV de anotaciones de PlantDoc al formato de texto YOLO.

    Args:
        ruta_csv: Archivo CSV con columnas [filename, width, height, class, xmin, ymin, xmax, ymax].
        dir_imagenes_origen: Carpeta con las imágenes JPEG.
        dir_destino_split: Carpeta de destino del split (train o val).
        mapa_clases: Diccionario {nombre_clase: id_numerico}.

    Returns:
        int: Total de imágenes procesadas.
    """
    dir_images = dir_destino_split / "images"
    dir_labels = dir_destino_split / "labels"
    dir_images.mkdir(parents=True, exist_ok=True)
    dir_labels.mkdir(parents=True, exist_ok=True)

    anotaciones_por_imagen: Dict[str, List[str]] = {}

    with open(ruta_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row["filename"]
            clase = row["class"].strip()
            if clase not in mapa_clases:
                continue

            clase_id = mapa_clases[clase]
            ancho_img = float(row["width"])
            alto_img = float(row["height"])
            xmin = float(row["xmin"])
            ymin = float(row["ymin"])
            xmax = float(row["xmax"])
            ymax = float(row["ymax"])

            # Si el CSV tiene ancho o alto 0, obtener dimensiones reales de la foto
            if ancho_img <= 0 or alto_img <= 0:
                src_temp = dir_imagenes_origen / filename
                if src_temp.exists():
                    try:
                        with Image.open(src_temp) as img:
                            ancho_img, alto_img = float(img.width), float(img.height)
                    except Exception:
                        continue
                else:
                    continue

            if ancho_img <= 0 or alto_img <= 0:
                continue

            # Normalización a coordenadas YOLO (centro, ancho, alto entre 0.0 y 1.0)
            x_center = max(0.0, min(1.0, ((xmin + xmax) / 2.0) / ancho_img))
            y_center = max(0.0, min(1.0, ((ymin + ymax) / 2.0) / alto_img))
            w = max(0.001, min(1.0, (xmax - xmin) / ancho_img))
            h = max(0.001, min(1.0, (ymax - ymin) / alto_img))

            linea = f"{clase_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}"
            anotaciones_por_imagen.setdefault(filename, []).append(linea)

    total = 0
    split_nombre = dir_destino_split.name
    for idx, (filename, lineas) in enumerate(anotaciones_por_imagen.items()):
        src_img = dir_imagenes_origen / filename
        if not src_img.exists():
            continue

        sufijo = Path(filename).suffix.lower()
        if not sufijo or len(sufijo) > 5:
            sufijo = ".jpg"

        # Nombre limpio y corto para evitar límites de ruta en Windows
        clean_stem = f"{split_nombre}_{idx:05d}"
        dst_img = dir_images / f"{clean_stem}{sufijo}"
        if not dst_img.exists():
            shutil.copy(src_img, dst_img)

        # Escribir archivo de etiquetas YOLO (.txt)
        dst_txt = dir_labels / f"{clean_stem}.txt"
        dst_txt.write_text("\n".join(lineas), encoding="utf-8")
        total += 1

    return total


def procesar_dataset_plantdoc(ruta_raw: Path, ruta_salida_yolo: Path) -> Path:
    """Orquesta la conversión de PlantDoc desde el repositorio crudo a formato YOLOv8.

    Args:
        ruta_raw: Directorio donde fue clonado el dataset.
        ruta_salida_yolo: Directorio donde se generará la estructura final de YOLO.

    Returns:
        Path: Ruta del descriptor data.yaml generado.
    """
    csv_train = ruta_raw / "train_labels.csv"
    csv_test = ruta_raw / "test_labels.csv"

    if not csv_train.exists():
        raise FileNotFoundError(f"No se encontró {csv_train}")

    # Determinar catálogo de clases
    clases = extraer_clases_desde_csv(csv_train)
    mapa_clases = {nombre: idx for idx, nombre in enumerate(clases)}

    print(f"Detectadas {len(clases)} clases agronómicas en PlantDoc:")
    for idx, c in enumerate(clases):
        print(f"  [{idx}] {c}")

    # Procesar split de entrenamiento y validación
    total_train = convertir_csv_a_yolo(csv_train, ruta_raw / "TRAIN", ruta_salida_yolo / "train", mapa_clases)
    total_val = convertir_csv_a_yolo(csv_test, ruta_raw / "TEST", ruta_salida_yolo / "val", mapa_clases)

    print(f"Imágenes convertidas exitosamente: {total_train} (train), {total_val} (val)")

    # Generar data.yaml oficial
    data_yaml = ruta_salida_yolo / "data.yaml"
    lineas_yaml = [
        f"path: {ruta_salida_yolo.as_posix()}",
        "train: train/images",
        "val: val/images",
        f"nc: {len(clases)}",
        "names:",
    ]
    for idx, c in enumerate(clases):
        lineas_yaml.append(f"  {idx}: '{c}'")

    data_yaml.write_text("\n".join(lineas_yaml), encoding="utf-8")
    print(f"Descriptor generado en: {data_yaml}")
    return data_yaml


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent.parent.parent
    raw = raiz / "ml" / "datasets" / "plantdoc_raw"
    salida = raiz / "ml" / "datasets" / "plantdoc_yolo"
    procesar_dataset_plantdoc(raw, salida)
