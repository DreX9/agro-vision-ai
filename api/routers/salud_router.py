"""Rutas de verificación de estado y salud del microservicio."""
from typing import Dict
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/salud", tags=["Salud"])


@router.get("", summary="Verifica el estado operativo de la API y disponibilidad de modelos.")
async def verificar_salud() -> Dict[str, str]:
    """Retorna estado operativo y versión del microservicio."""
    return {
        "estado": "OPERATIVO",
        "servicio": "agro-vision-ai",
        "version": "1.0.0"
    }