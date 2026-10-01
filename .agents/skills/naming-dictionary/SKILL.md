---
name: naming-dictionary
description: "Trigger: naming python, clases plagas, nombres endpoints ai, nomenclatura ai. Diccionario de nomenclatura para Agro Vision AI."
license: Apache-2.0
metadata:
  author: "agro-vision-team"
  version: "1.0"
---

# Diccionario de Nomenclatura AI

## Reglas Inviolables
* **Endpoints:** Nombres en español técnico (`/api/v1/diagnosticos/analizar-imagen`, `/api/v1/diagnosticos/analizar-video`, `/api/v1/salud`).
* **Esquemas Pydantic:** Sufijo `Dto` o `Schema` en PascalCase (`DiagnosticoRespuestaDto`, `DeteccionPlagaDto`, `CoordenadasBboxDto`).
* **Clases de Plagas:** snake_case en español canónico (`hoja_saludable`, `gusano_cogollero`, `pulgones`, `mancha_foliar`, `roya`, `mosca_blanca`).
* **Archivos Python:** snake_case descriptivo (`detector_plagas.py`, `clasificador_hojas.py`, `procesador_video.py`).