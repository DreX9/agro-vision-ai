---
name: verify-before-commit
description: "Trigger: verificar python, pre-commit ai, test ai, lint python. Checklist de calidad antes de cerrar tareas en Agro Vision AI."
license: Apache-2.0
metadata:
  author: "agro-vision-team"
  version: "1.0"
---

# Checklist de Verificación de Calidad AI

## Pipeline de Validación
```bash
# 1. Linter y verificación de formato
ruff check .

# 2. Pruebas unitarias
pytest tests/
```

## Checklist de Reglas
- [ ] **Límite de 300 líneas:** Ningún archivo `.py` supera 300 líneas.
- [ ] **Type Hints:** No hay `Any` en firmas de funciones públicas.
- [ ] **Docstrings:** Docstrings presentes en clases y métodos principales.
- [ ] **Salida normalizada:** Las coordenadas de detección están normalizadas en rango 0.0 - 1.0.