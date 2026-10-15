"""Punto de entrada del microservicio Agro Vision AI con FastAPI."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.core.config import settings
from api.routers import diagnostico_router, salud_router
from ml.inference.detector_plagas import detector_plagas


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Ciclo de vida de la aplicación: inicialización de modelos al arrancar."""
    detector_plagas.cargar_modelo()
    yield


app = FastAPI(
    title="Agro Vision AI - API de Visión Computacional",
    description="Microservicio de inferencia para detección de plagas, análisis foliar y procesamiento de video.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diagnostico_router.router)
app.include_router(salud_router.router)