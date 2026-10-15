"""Mapeo y traducción canónica de plagas y recomendaciones agronómicas al español."""
from typing import Dict, List, Set, Tuple


# Mapeo canónico de las 29 clases del modelo a nombres agronómicos en español
DICCIONARIO_CLASES_ESPANOL: Dict[str, str] = {
    "apple scab leaf": "Hoja de manzano con sarna (roña)",
    "apple leaf": "Hoja sana de manzano",
    "apple rust leaf": "Hoja de manzano con roya",
    "bell_pepper leaf": "Hoja sana de pimiento",
    "bell_pepper leaf spot": "Hoja de pimiento con mancha foliar",
    "blueberry leaf": "Hoja sana de arándano",
    "cherry leaf": "Hoja sana de cerezo",
    "corn gray leaf spot": "Hoja de maíz con mancha foliar gris",
    "corn leaf blight": "Hoja de maíz con tizón foliar",
    "corn rust leaf": "Hoja de maíz con roya foliar",
    "peach leaf": "Hoja de melocotonero (durazno)",
    "potato leaf": "Hoja sana de papa",
    "potato leaf early blight": "Hoja de papa con tizón temprano",
    "potato leaf late blight": "Hoja de papa con tizón tardío",
    "raspberry leaf": "Hoja sana de frambuesa",
    "soyabean leaf": "Hoja sana de soja",
    "squash powdery mildew leaf": "Hoja de calabaza con oídio (mildiu)",
    "strawberry leaf": "Hoja sana de fresa",
    "tomato early blight leaf": "Hoja de tomate con tizón temprano",
    "tomato septoria leaf spot": "Hoja de tomate con mancha por Septoria",
    "tomato leaf": "Hoja sana de tomate",
    "tomato leaf bacterial spot": "Hoja de tomate con mancha bacteriana",
    "tomato leaf late blight": "Hoja de tomate con tizón tardío",
    "tomato leaf mosaic virus": "Hoja de tomate con virus del mosaico",
    "tomato leaf yellow virus": "Hoja de tomate con virus del rizado amarillo",
    "tomato mold leaf": "Hoja de tomate con moho foliar",
    "tomato two spotted spider mites leaf": "Hoja de tomate con arañita roja (ácaros)",
    "grape leaf": "Hoja sana de vid (uva)",
    "grape leaf black rot": "Hoja de vid con pudrición negra",
}

# Conjunto de clases correspondientes a hojas sanas
CLASES_HOJAS_SANAS: Set[str] = {
    "apple leaf",
    "bell_pepper leaf",
    "blueberry leaf",
    "cherry leaf",
    "peach leaf",
    "potato leaf",
    "raspberry leaf",
    "soyabean leaf",
    "strawberry leaf",
    "tomato leaf",
    "grape leaf",
}


def normalizar_clave_clase(nombre: str) -> str:
    """Normaliza el nombre de la clase para búsqueda insensible a mayúsculas y guiones.

    Args:
        nombre: Nombre de la clase en inglés.

    Returns:
        str: Cadena normalizada en minúsculas y espacios simples.
    """
    return nombre.strip().lower().replace("_", " ")


def traducir_clase_a_espanol(nombre_clase: str) -> str:
    """Traduce el nombre original de la clase a español agronómico comprensible.

    Args:
        nombre_clase: Nombre original en inglés generado por el modelo.

    Returns:
        str: Nombre formal en español.
    """
    clave = normalizar_clave_clase(nombre_clase)
    return DICCIONARIO_CLASES_ESPANOL.get(clave, nombre_clase.replace("_", " ").title())


def es_hoja_saludable(nombre_clase: str) -> bool:
    """Determina si la clase identificada corresponde a una hoja sin patologías.

    Args:
        nombre_clase: Nombre original de la clase.

    Returns:
        bool: True si la hoja no presenta signos de enfermedad.
    """
    clave = normalizar_clave_clase(nombre_clase)
    return clave in CLASES_HOJAS_SANAS


def generar_recomendaciones_agronomicas(clases_detectadas: List[str]) -> Tuple[str, float, List[str]]:
    """Genera el estado, porcentaje de salud y recomendaciones específicas en español.

    Args:
        clases_detectadas: Lista de nombres originales de clases detectadas.

    Returns:
        Tuple con (estado_general, salud_porcentaje, lista_de_recomendaciones).
    """
    if not clases_detectadas:
        return (
            "OPTIMO",
            98.0,
            [
                "No se observan anomalías o patógenos foliares en el encuadre.",
                "Mantener el plan de inspección y monitoreo periódico en campo.",
            ],
        )

    claves = [normalizar_clave_clase(c) for c in clases_detectadas]
    enfermedades = [c for c in claves if c not in CLASES_HOJAS_SANAS]

    # Si todas las detecciones son hojas sanas
    if not enfermedades:
        return (
            "OPTIMO",
            95.0,
            [
                "El follaje analizado presenta características de hoja sana y buen vigor vegetativo.",
                "Continuar con el programa preventivo de riego y nutrición foliar.",
            ],
        )

    # Diagnóstico con enfermedades activas
    recomendaciones: List[str] = []
    texto_acumulado = " ".join(enfermedades)

    if "early blight" in texto_acumulado:
        recomendaciones.append(
            "Tizón temprano (Alternaria solani): Evitar el riego por aspersión para no diseminar esporas."
        )
        recomendaciones.append(
            "Poda sanitaria de hojas basales afectadas y aplicación de fungicida cúprico o biofungicida (Trichoderma)."
        )

    if "late blight" in texto_acumulado:
        recomendaciones.append(
            "Alerta de Tizón tardío (Phytophthora infestans): Aislar inmediatamente los sectores afectados."
        )
        recomendaciones.append(
            "Aplicar tratamiento fungicida sistémico de choque y reducir la humedad relativa del dosel."
        )

    if "rust" in texto_acumulado:
        recomendaciones.append(
            "Roya foliar: Mejorar la circulación de aire entre hileras y aplicar producto a base de azufre o triazoles."
        )

    if "spider mites" in texto_acumulado:
        recomendaciones.append(
            "Arañita roja / Ácaros: Pulverizar agua con jabón potásico o aceite de neem en el envés foliar."
        )
        recomendaciones.append(
            "Aumentar ligeramente la humedad ambiental para frenar la proliferación del ácaro."
        )

    if "bacterial spot" in texto_acumulado or "septoria" in texto_acumulado or "leaf spot" in texto_acumulado:
        recomendaciones.append(
            "Manchas foliares (Bacterianas / Septoria): Desinfectar herramientas de poda y eliminar restos caídos del suelo."
        )

    if "powdery mildew" in texto_acumulado:
        recomendaciones.append(
            "Oídio / Mildiu: Aplicar bicarbonato potásico o azufre mojable en horarios de baja radiación solar."
        )

    if "virus" in texto_acumulado:
        recomendaciones.append(
            "Sospecha de virosis vegetal: Controlar vectores chupadores (pulgones, mosca blanca) y desinfectar manos."
        )

    if "black rot" in texto_acumulado or "scab" in texto_acumulado or "mold" in texto_acumulado:
        recomendaciones.append(
            "Afección fúngica avanzada (Roña / Moho / Pudrición): Retirar hojas severamente dañadas."
        )

    if not recomendaciones:
        recomendaciones.append(
            "Monitorear la evolución de las lesiones foliares en las próximas 48 horas para prevenir propagación."
        )

    total_lesiones = len(enfermedades)
    if total_lesiones == 1:
        estado = "ALERTA"
        salud = 80.0
    elif total_lesiones == 2:
        estado = "ALERTA"
        salud = 62.0
    else:
        estado = "CRITICO"
        salud = max(15.0, 50.0 - (total_lesiones * 10.0))

    return (estado, salud, recomendaciones)
