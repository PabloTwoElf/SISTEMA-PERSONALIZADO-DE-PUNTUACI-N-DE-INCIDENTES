"""Dominio del sistema de puntuación de incidentes (ISWZ-3208, Grupo 5).

Define las 5 preguntas con sus criterios medibles (escala 1-5) y las
categorías de prioridad. Es la única fuente de verdad del modelo:
la lógica de cálculo (scoring.py) y la presentación (cli.py) dependen
de este módulo y no al revés (Dependency Inversion).
"""
from dataclasses import dataclass
from enum import Enum


class Dimension(Enum):
    IMPACTO = "Impacto"
    URGENCIA = "Urgencia"


@dataclass(frozen=True)
class Question:
    id: int
    text: str
    dimension: Dimension
    # criteria[i] es el criterio medible para el valor i+1 (1..5)
    criteria: tuple[str, str, str, str, str]


@dataclass(frozen=True)
class PriorityCategory:
    code: str
    name: str
    min_score: int
    max_score: int
    response_time: str

    def contains(self, score: int) -> bool:
        return self.min_score <= score <= self.max_score


QUESTIONS: tuple[Question, ...] = (
    Question(
        id=1,
        text=("¿Qué porcentaje de los usuarios de la organización queda "
              "imposibilitado de realizar su trabajo a causa del incidente?"),
        dimension=Dimension.IMPACTO,
        criteria=(
            "Menos del 1% (un usuario aislado)",
            "Entre el 1% y el 10% (un equipo de trabajo)",
            "Entre el 11% y el 30% (un departamento o área)",
            "Entre el 31% y el 70% (varios departamentos o una sede completa)",
            "Más del 70% de la organización, o afecta a clientes externos",
        ),
    ),
    Question(
        id=2,
        text=("¿Qué nivel de criticidad tiene el servicio afectado según el "
              "catálogo de servicios del negocio?"),
        dimension=Dimension.IMPACTO,
        criteria=(
            "Servicio de apoyo interno; no detiene ningún proceso de negocio",
            "Servicio secundario con alternativa equivalente inmediata",
            "Servicio importante; alternativa parcial (solo funciones básicas)",
            "Servicio core con alternativa limitada",
            "Servicio core sin alternativa; detiene la generación de ingresos",
        ),
    ),
    Question(
        id=3,
        text=("¿Qué nivel de compromiso existe sobre la integridad, "
              "confidencialidad o disponibilidad de los datos?"),
        dimension=Dimension.IMPACTO,
        criteria=(
            "Ninguna evidencia de afectación a los datos",
            "Sospecha no confirmada (alerta de monitoreo sin verificar)",
            "Corrupción/pérdida de datos internos con respaldo verificado",
            "Exposición potencial de datos sensibles o credenciales",
            "Pérdida o exposición confirmada de datos personales o regulados",
        ),
    ),
    Question(
        id=4,
        text=("¿Cuánto tiempo y esfuerzo requiere aplicar una solución "
              "temporal (workaround) mientras se resuelve el incidente?"),
        dimension=Dimension.URGENCIA,
        criteria=(
            "Workaround documentado, aplicable por el usuario en <15 min",
            "Workaround aplicable por mesa de servicios en <1 hora",
            "Workaround parcial: cubre solo funciones básicas",
            "Workaround complejo: especialistas y más de 4 horas",
            "No existe workaround: caído hasta la solución definitiva",
        ),
    ),
    Question(
        id=5,
        text="¿Con qué velocidad aumenta el daño si el incidente no se atiende?",
        dimension=Dimension.URGENCIA,
        criteria=(
            "Estable: el impacto no crece con el tiempo",
            "Crece en semanas (acumulación lenta de retrabajo)",
            "Crece en días (retrasos que comprometen plazos)",
            "Crece en horas (pérdidas operativas/económicas por hora)",
            "Crece por minutos: daño inmediato y acumulativo",
        ),
    ),
)

PRIORITY_CATEGORIES: tuple[PriorityCategory, ...] = (
    PriorityCategory("P1", "Crítica", 21, 25,
                     "Inmediata (máx. 1 hora), escalamiento a dirección"),
    PriorityCategory("P2", "Alta", 16, 20, "Máximo 4 horas"),
    PriorityCategory("P3", "Media", 11, 15, "Máximo 1 día laborable"),
    PriorityCategory("P4", "Baja", 5, 10,
                     "Máximo 3 días laborables, atención planificada"),
)

MIN_ANSWER, MAX_ANSWER = 1, 5
