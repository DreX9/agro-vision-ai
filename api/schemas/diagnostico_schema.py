"""Esquemas Pydantic para intercambio de datos en diagnósticos agronómicos."""
from typing import List, Optional
from pydantic import BaseModel, Field


class BoundingBoxDto(BaseModel):
    """Coordenadas normalizadas [0.0 - 1.0] del recuadro delimitador."""
    x_min: float = Field(..., description="Límite izquierdo normalizado")
    y_min: float = Field(..., description="Límite superior normalizado")
    x_max: float = Field(..., description="Límite derecho normalizado")
    y_max: float = Field(..., description="Límite inferior normalizado")


class DeteccionPlagaDto(BaseModel):
    """Representa una plaga o anomalía detectada en la imagen/frame."""
    clase: str = Field(..., description="Nombre canónico de la plaga o anomalía")
    confianza: float = Field(..., description="Nivel de confianza de la predicción (0.0 a 1.0)")
    caja: BoundingBoxDto = Field(..., description="Ubicación espacial en el frame")


class DiagnosticoRespuestaDto(BaseModel):
    """Respuesta completa estructurada del diagnóstico para consumo por el backend."""
    estado_general: str = Field(..., description="Estado general de salud: 'OPTIMO', 'ALERTA' o 'CRITICO'")
    salud_porcentaje: float = Field(..., description="Índice estimado de salud foliar (0% - 100%)")
    total_plagas_detectadas: int = Field(..., description="Cantidad total de detecciones encontradas")
    detecciones: List[DeteccionPlagaDto] = Field(default_factory=list, description="Lista de plagas detectadas")
    recomendaciones: List[str] = Field(default_factory=list, description="Recomendaciones agronómicas inmediatas")
    tiempo_procesamiento_ms: float = Field(..., description="Tiempo transcurrido en inferencia")