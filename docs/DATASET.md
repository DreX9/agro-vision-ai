# Guía de Datasets y Formatos de Etiquetado

## 1. Clases de Detección Agrícola (Plagas y Defectos)

| ID | Clase (Nombre Canónico) | Descripción | Tipo de Detección |
| :--- | :--- | :--- | :--- |
| `0` | `hoja_saludable` | Hoja sin presencia de plagas ni signos de necrosis o clorosis. | Bounding Box / Segmentación |
| `1` | `gusano_cogollero` | Larva de Spodoptera frugiperda o similar en hojas/tallos. | Bounding Box |
| `2` | `pulgones` | Colonias de áfidos en el envés de la hoja. | Bounding Box / Cluster |
| `3` | `mancha_foliar` | Lesiones necróticas por hongos o bacterias (Cercospora, etc.). | Bounding Box |
| `4` | `roya` | Pústulas de color anaranjado/amarillo en la superficie foliar. | Bounding Box |
| `5` | `mosca_blanca` | Insectos pequeños de color blanco o ninfas. | Bounding Box |

---

## 2. Estructura de Carpetas del Dataset (Formato YOLO)

```text
datasets/
├── plagas_yolo/
│   ├── data.yaml                     # Definición de clases y rutas
│   ├── train/
│   │   ├── images/                   # Fotos .jpg
│   │   └── labels/                   # Archivos .txt (formato: <class_id> <x_center> <y_center> <width> <height>)
│   ├── val/
│   │   ├── images/
│   │   └── labels/
│   └── test/
│       ├── images/
│       └── labels/
```

---

## 3. Aumentación de Datos Recomendada
* Rotación aleatoria (`+-15°`).
* Variación de brillo (`+-20%`) para simular condiciones de sol directo y sombra en campo.
* Desenfoque de movimiento suave para simular la vibración de la cámara del móvil en mano.
* Flip horizontal (espejo).