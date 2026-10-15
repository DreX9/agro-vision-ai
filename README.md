# Agro Vision AI - Microservicio de Detección de Plagas y Enfermedades

Microservicio de visión por computadora e inferencia agronómica construido con FastAPI, YOLOv8 y PyTorch para el diagnóstico temprano de plagas y enfermedades foliares en cultivos agrícolas.

---

## Características Principales

* **Detección Fitosanitaria en Tiempo Real**: Identificación multiclase de 29 patologías y hojas sanas en 13 tipos de cultivos (tomate, papa, maíz, manzana, uva, pimiento, entre otros).
* **Traducción y Recomendaciones Agronómicas Canónicas**: Respuestas estructuradas en español con severidad estimada, recomendaciones de manejo integrado y medidas correctivas.
* **Soporte Multiplataforma**: Compatible con clientes Web y dispositivos móviles Android con orientación EXIF automática.
* **Inferencia Asíncrona**: Procesamiento optimizado de imágenes individuales y muestreo de flujos de video por lotes.

---

## Requisitos Previos

* Python 3.10 o superior (recomendado Python 3.12).
* Tarjeta gráfica compatible con CUDA (opcional, opera automáticamente en CPU si no está disponible).

---

## Instalación y Configuración

1. Clonar el repositorio y posicionarse en la carpeta:
```bash
git clone <url-del-repositorio>
cd agro-vision-ai
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
```

---

## Descarga de Pesos del Modelo

Los pesos entrenados del modelo YOLOv8n (`yolov8n_plagas.pt`) se encuentran alojados en el repositorio de Hugging Face:

* **Repositorio:** [DreX09/yolov8n-agrovision-plagas](https://huggingface.co/DreX09/yolov8n-agrovision-plagas)

Para descargarlos directamente a la carpeta del proyecto:

```bash
# Windows (PowerShell) o Linux/macOS:
curl -L -o ml/models/yolov8n_plagas.pt https://huggingface.co/DreX09/yolov8n-agrovision-plagas/resolve/main/yolov8n_plagas.pt
```

---

## Ejecución del Servicio

Iniciar el servidor de desarrollo FastAPI:

```bash
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

La documentación Swagger interactiva estará disponible en:
* `http://localhost:8000/docs`
* `http://localhost:8000/redoc`

---

## Pruebas Automatizadas

Ejecutar la suite de pruebas unitarias:

```bash
pytest tests/
```
