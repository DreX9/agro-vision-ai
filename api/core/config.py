"""Configuración central del microservicio Agro Vision AI."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Parámetros de configuración de la aplicación cargados desde entorno."""
    
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    ENVIRONMENT: str = "development"
    
    MODELO_YOLO_PATH: str = "ml/models/yolov8n_plagas.pt"
    MODELO_MOBILENET_PATH: str = "ml/models/mobilenet_v3_enfermedades.onnx"
    URL_MODELO_HUGGINGFACE: str = (
        "https://huggingface.co/DreX09/yolov8n-agrovision-plagas/resolve/main/yolov8n_plagas.pt"
    )
    UMBRAL_CONFIANZA: float = 0.35
    UMBRAL_IOU: float = 0.50
    DISPOSITIVO: str = "cpu"
    FPS_MUESTREO_VIDEO: int = 4

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()