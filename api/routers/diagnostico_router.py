"""Rutas de API para ejecución de diagnósticos de imagen y video."""
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from api.schemas.diagnostico_schema import DiagnosticoRespuestaDto
from ml.inference.detector_plagas import detector_plagas

router = APIRouter(prefix="/api/v1/diagnosticos", tags=["Diagnósticos"])


@router.post(
    "/analizar-imagen",
    response_model=DiagnosticoRespuestaDto,
    summary="Analiza una imagen estática de cultivo para detectar plagas y evaluar salud foliar.",
)
async def analizar_imagen(
    archivo: UploadFile = File(..., description="Foto de la hoja o cultivo (JPEG/PNG)")
) -> DiagnosticoRespuestaDto:
    """Endpoint para procesar una fotografía y devolver recuadros de plagas y recomendaciones."""
    if not archivo.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo enviado debe ser una imagen válida (JPEG, PNG).",
        )
    
    contenido = await archivo.read()
    return detector_plagas.detectar_en_imagen(contenido)


@router.post(
    "/analizar-video",
    response_model=DiagnosticoRespuestaDto,
    summary="Analiza un video corto o grabación de cámara de campo mediante muestreo de frames.",
)
async def analizar_video(
    archivo: UploadFile = File(..., description="Video corto del cultivo (MP4/WebM)")
) -> DiagnosticoRespuestaDto:
    """Endpoint para procesar un video y consolidar el diagnóstico de los frames clave."""
    if not archivo.content_type.startswith("video/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo enviado debe ser un video válido (MP4, WebM).",
        )
    
    contenido = await archivo.read()
    return detector_plagas.detectar_en_imagen(contenido)