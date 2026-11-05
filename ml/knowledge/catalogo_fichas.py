"""Catálogo de fichas técnicas agronómicas categorizadas para plagas y patologías."""
from typing import Dict, List, Set

from api.schemas.diagnostico_schema import FichaTecnicaPatologiaDto

# Catálogo base de fichas técnicas especializadas
CATALOGO_PATOLOGIAS: Dict[str, FichaTecnicaPatologiaDto] = {
    "tizon_temprano": FichaTecnicaPatologiaDto(
        patologia="Tizón Temprano (Alternaria solani)",
        accion_inmediata=[
            "Poda sanitaria de hojas basales con más del 20% de superficie foliar necrosada.",
            "Retiro del material infectado en bolsas cerradas fuera del lote para evitar diseminación.",
        ],
        control_biologico=[
            "Aspersión foliar de biofungicida a base de Trichoderma harzianum o Bacillus subtilis.",
            "Aplicación de extracto botánico de cola de caballo (Equisetum arvense) como bioestimulante.",
        ],
        control_quimico=[
            "Fungicida protectante a base de Oxicloruro de Cobre (2.5 g/L).",
            "En ataques severos, fungicida sistémico (Difenoconazol) respetando periodo de carencia (7 días).",
        ],
        manejo_preventivo=[
            "Reemplazar riego por aspersión por goteo para evitar mojar el follaje.",
            "Deshoje de aireación en la base de la planta para reducir microclimas húmedos.",
        ],
        herramientas_sugeridas=[
            "Tijeras de podar de mano (bypass) con hojas desinfectadas.",
            "Pulverizador o mochila de espalda con boquilla de cono hueco.",
            "Alcohol al 70% o solución de lejía al 5% para desinfectar herramientas.",
            "Bolsas herméticas para disposición de restos vegetales enfermos.",
            "Guantes de nitrilo y mascarilla de protección N95/FFP2.",
        ],
    ),
    "tizon_tardio": FichaTecnicaPatologiaDto(
        patologia="Tizón Tardío (Phytophthora infestans)",
        accion_inmediata=[
            "Aislar de inmediato el sector afectado y restringir el tránsito de trabajadores por la hilera.",
            "Eliminar y enterrar a más de 50 cm los órganos severamente dañados.",
        ],
        control_biologico=[
            "Tratamiento preventivo con biofungicidas a base de extracto de cítricos y quitosano.",
            "Fomentar micorrizas y rizobacterias para fortalecer la resistencia sistémica de la planta.",
        ],
        control_quimico=[
            "Aplicación urgente de fungicida sistémico de choque (Metalaxil + Mancoceb o Cimoxanilo).",
            "Rotar grupos químicos para prevenir resistencia (respetar carencia de 14 días).",
        ],
        manejo_preventivo=[
            "Evitar el encharcamiento en surcos y mantener buen drenaje del suelo.",
            "Monitoreo diario si la humedad relativa supera el 90% y temperaturas entre 15-20°C.",
        ],
        herramientas_sugeridas=[
            "Tijeras de poda o navaja curva desinfectada.",
            "Mochila pulverizadora a motor o batería con filtro de presión constante.",
            "Overol de protección impermeable, botas de goma y guantes de nitrilo.",
            "Mascarilla con filtro para vapores y partículas orgánicas.",
            "Contenedor cerrado para transporte seguro de tejido vegetal infectado.",
        ],
    ),
    "roya": FichaTecnicaPatologiaDto(
        patologia="Roya Foliar (Puccinia spp. / Gymnosporangium spp.)",
        accion_inmediata=[
            "Eliminar brotes y hojas que presenten pústulas anaranjadas o marrones visibles.",
            "Desinfectar el calzado y herramientas al salir de la parcela infectada.",
        ],
        control_biologico=[
            "Uso de preparados de azufre elemental micronizado en dosis preventivas.",
            "Inoculación foliar de cepas antagonistas de Bacillus amyloliquefaciens.",
        ],
        control_quimico=[
            "Aplicación de triazoles específicos (Tebuconazol o Triadimefon) al advertir primeras pústulas.",
            "Fungicidas de contacto a base de Mancozeb como barrera protectora.",
        ],
        manejo_preventivo=[
            "Incrementar la distancia entre plantas para favorecer la circulación continua de aire.",
            "Evitar el exceso de fertilización nitrogenada que favorece tejido tierno susceptible.",
        ],
        herramientas_sugeridas=[
            "Tijera podadora de dos manos o podón según el porte del cultivo.",
            "Pulverizador con lanza telescópica para cobertura homogénea del envés foliar.",
            "Gafas de seguridad y mascarilla antipolvo.",
            "Solución desinfectante de hipoclorito de sodio al 5%.",
        ],
    ),
    "aranita_roja": FichaTecnicaPatologiaDto(
        patologia="Arañita Roja / Ácaros (Tetranychus urticae)",
        accion_inmediata=[
            "Lavar el follaje con agua a presión moderada para romper telarañas y bajar poblaciones.",
            "Retirar ramas o guías con enrollamiento severo y clorosis punteada.",
        ],
        control_biologico=[
            "Aplicación de jabón potásico (10-15 ml/L) combinado con aceite de neem al 1%.",
            "Liberación o fomento de ácaros depredadores benéficos (Phytoseiulus persimilis).",
        ],
        control_quimico=[
            "Acaricida ovicida o adulticida específico (Abamectina o Spiromesifen) focalizado en focos.",
            "Alternar modos de acción para no inducir tolerancia en poblaciones de ácaros.",
        ],
        manejo_preventivo=[
            "Mantener humedad ambiental adecuada y evitar sequedad prolongada en el entorno.",
            "Controlar malezas hospederas en las cabeceras de los campos.",
        ],
        herramientas_sugeridas=[
            "Lupa de bolsillo (10x - 20x) o lente cuentahilos para monitoreo en envés.",
            "Pulverizador manual con boquilla regulable de gota fina dirigida al envés foliar.",
            "Guantes de protección agrícola y gafas transparentes.",
        ],
    ),
    "mancha_foliar": FichaTecnicaPatologiaDto(
        patologia="Mancha Foliar y Bacteriosis (Septoria / Xanthomonas)",
        accion_inmediata=[
            "Retirar hojas basales caídas o con manchas circulares necróticas.",
            "No manipular las plantas mientras el follaje se encuentre húmedo o tras rocío.",
        ],
        control_biologico=[
            "Aplicación preventiva de extracto de semilla de cítricos o propóleo.",
            "Uso de biobactericidas formulados con Bacillus subtilis.",
        ],
        control_quimico=[
            "Tratamiento bactericida/fungicida con Sulfato de Cobre pentahidratado o Kasugamicina.",
            "Respetar las pautas de dosificación recomendadas por el fabricante técnico.",
        ],
        manejo_preventivo=[
            "Esterilizar semillas y utilizar plántulas certificadas libres de patógenos.",
            "Limpieza rigurosa de bancales y tutores al finalizar el ciclo de cultivo.",
        ],
        herramientas_sugeridas=[
            "Tijeras podadoras esterilizables por inmersión.",
            "Equipo de pulverización con boquilla de abanico plano.",
            "Frasco atomizador con alcohol al 70% para desinfección continua en campo.",
            "Guantes descartables de látex o nitrilo.",
        ],
    ),
    "oidio_mildiu": FichaTecnicaPatologiaDto(
        patologia="Oídio y Mildiu Polvoriento (Erysiphales)",
        accion_inmediata=[
            "Podar hojas apicales o intermedias cubiertas con el polvo blanquecino característico.",
            "Mejorar la luminosidad y exposición solar en el centro del dosel vegetal.",
        ],
        control_biologico=[
            "Foliar con bicarbonato de potasio (3-5 g/L) más jabón neutro como humectante.",
            "Aplicación de suero de leche diluido al 10% en agua como biofungicida de contacto.",
        ],
        control_quimico=[
            "Azufre mojable micronizado aplicado temprano por la mañana o al atardecer.",
            "Fungicidas específicos antioidío (Penconazol o Azoxistrobina).",
        ],
        manejo_preventivo=[
            "Evitar densidades excesivas de siembra y mejorar aireación lateral de invernaderos.",
            "Monitorear oscilaciones térmicas día-noche con alta humedad matutina.",
        ],
        herramientas_sugeridas=[
            "Mochila de aspersión con filtro y boquilla de cono regulable.",
            "Tijeras podadoras de bypass de precisión.",
            "Gafas de protección herméticas para aplicación de azufre.",
            "Guantes de goma resistentes a preparados minerales.",
        ],
    ),
    "virosis": FichaTecnicaPatologiaDto(
        patologia="Virosis Vegetal (Virus del Mosaico / Rizado Amarillo)",
        accion_inmediata=[
            "Arrancar de raíz las plantas que muestren deformación o amarillamiento acentuado.",
            "Eliminar la planta infectada en bolsa hermética para no soltar insectos vectores.",
        ],
        control_biologico=[
            "Instalar trampas cromáticas amarillas y azules para monitoreo y captura de vectores.",
            "Aplicación de extracto de ajo y neem para repeler pulgones y mosca blanca.",
        ],
        control_quimico=[
            "No existen antivirales curativos; el control se centra en el vector insecto transmisor.",
            "Aplicar insecticida sistémico selectivo (Acetamiprid o Flonicamid) contra chupadores.",
        ],
        manejo_preventivo=[
            "Uso estricto de mallas anti-áfidos en viveros e invernaderos.",
            "Desinfección de manos con leche descremada o fosfato trisódico al entresacar.",
        ],
        herramientas_sugeridas=[
            "Pala de mano o trasplantador para erradicación completa de raíz.",
            "Trampas adhesivas cromáticas (amarillas y azules).",
            "Bolsas gruesas de polietileno de alta resistencia para descarte.",
            "Guantes de protección descartables.",
        ],
    ),
    "afeccion_fungica_compleja": FichaTecnicaPatologiaDto(
        patologia="Afección Fúngica de Fruto/Follaje (Sarna, Pudrición o Moho)",
        accion_inmediata=[
            "Retirar frutos o tallos con lesiones deprimidas oscuras o fructificaciones fúngicas.",
            "Enterrar o compostar a alta temperatura el material descartado lejos de plantaciones.",
        ],
        control_biologico=[
            "Biofungicidas a base de Bacillus velezensis o extractos de gobernadora (Larrea tridentata).",
            "Refuerzo foliar con silicio y caldos minerales suaves.",
        ],
        control_quimico=[
            "Fungicida curativo a base de Folpet, Captan o Ditiocarbamatos según registro local.",
            "Rotar ingredientes activos para evitar cepas resistentes en el lote.",
        ],
        manejo_preventivo=[
            "Recolección total de restos de cosecha y hojas secas antes de la nueva campaña.",
            "Evitar heridas mecánicas en tallos y ramas durante labores culturales.",
        ],
        herramientas_sugeridas=[
            "Tijeras de podar de dos manos desinfectadas.",
            "Cuchilla o navaja de injerto para limpieza de chancros en ramas.",
            "Pasta cicatrizante para cortes de poda con fungicida cúprico incorporado.",
            "Mochila aspersora y equipo de protección personal completo.",
        ],
    ),
}


FICHA_FOLLAJE_SANO = FichaTecnicaPatologiaDto(
    patologia="Follaje Saludable y Vigor Vegetativo Óptimo",
    accion_inmediata=[
        "No se requieren intervenciones curativas ni podas de emergencia.",
        "Mantener el cronograma habitual de labores agronómicas.",
    ],
    control_biologico=[
        "Aplicación preventiva de bioestimulantes a base de algas marinas o aminoácidos libres.",
        "Conservar la fauna benéfica y polinizadores en el entorno del cultivo.",
    ],
    control_quimico=[
        "No aplicar productos agroquímicos de choque para no inducir estrés ni fitotoxicidad innecesaria.",
    ],
    manejo_preventivo=[
        "Monitoreo semanal rutinario inspeccionando el envés foliar y brotes nuevos.",
        "Gestionar el riego según la evapotranspiración de la zona para evitar estrés hídrico.",
    ],
    herramientas_sugeridas=[
        "Lupa de campo o lente cuentahilos para revisión preventiva periódica.",
        "Cuaderno de campo o aplicación móvil para registro de monitoreo agronómico.",
        "Medidor de humedad de suelo o tensiómetro para calibración de riego.",
    ],
)


def clasificar_patologia_por_nombre(nombre_original: str) -> str:
    """Clasifica una clase del modelo dentro de una de las patologías del catálogo.

    Args:
        nombre_original: Nombre de la clase devuelta por la inferencia en inglés.

    Returns:
        str: Clave identificadora en el catálogo de fichas técnicas.
    """
    texto = nombre_original.strip().lower().replace("_", " ")

    if "early blight" in texto:
        return "tizon_temprano"
    if "late blight" in texto:
        return "tizon_tardio"
    if "rust" in texto:
        return "roya"
    if "spider mites" in texto:
        return "aranita_roja"
    if any(k in texto for k in ["bacterial spot", "septoria", "leaf spot", "leaf blight"]):
        return "mancha_foliar"
    if "powdery mildew" in texto:
        return "oidio_mildiu"
    if "virus" in texto:
        return "virosis"
    if any(k in texto for k in ["scab", "black rot", "mold"]):
        return "afeccion_fungica_compleja"
    return "mancha_foliar"


def obtener_ficha_follaje_sano() -> FichaTecnicaPatologiaDto:
    """Retorna la ficha técnica orientada a mantenimiento y nutrición de hoja sana."""
    return FICHA_FOLLAJE_SANO


def obtener_fichas_tecnicas(clases_detectadas: List[str]) -> List[FichaTecnicaPatologiaDto]:
    """Genera las fichas técnicas agronómicas correspondientes a las plagas identificadas.

    Args:
        clases_detectadas: Lista de nombres de clases detectadas por el modelo.

    Returns:
        List[FichaTecnicaPatologiaDto]: Lista sin duplicados de fichas técnicas categorizadas.
    """
    if not clases_detectadas:
        return [FICHA_FOLLAJE_SANO]

    claves_procesadas: Set[str] = set()
    fichas: List[FichaTecnicaPatologiaDto] = []

    for clase in clases_detectadas:
        clave_cat = clasificar_patologia_por_nombre(clase)
        if clave_cat not in claves_procesadas and clave_cat in CATALOGO_PATOLOGIAS:
            claves_procesadas.add(clave_cat)
            fichas.append(CATALOGO_PATOLOGIAS[clave_cat])

    if not fichas:
        return [FICHA_FOLLAJE_SANO]

    return fichas
