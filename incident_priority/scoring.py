"""Lógica de cálculo de prioridad. Pura y sin I/O: fácil de testear."""
from dataclasses import dataclass

from .domain import (MAX_ANSWER, MIN_ANSWER, PRIORITY_CATEGORIES, QUESTIONS,
                     PriorityCategory)


@dataclass(frozen=True)
class Assessment:
    """Resultado inmutable de evaluar un incidente."""
    answers: dict[int, int]
    total: int
    category: PriorityCategory


def validate_answers(answers: dict[int, int]) -> None:
    """Valida completitud y rango. Lanza ValueError con mensaje claro."""
    expected = {q.id for q in QUESTIONS}
    if set(answers) != expected:
        missing = sorted(expected - set(answers))
        extra = sorted(set(answers) - expected)
        raise ValueError(
            f"Respuestas inválidas. Faltan preguntas {missing}, sobran {extra}.")
    for qid, value in answers.items():
        if not isinstance(value, int) or not MIN_ANSWER <= value <= MAX_ANSWER:
            raise ValueError(
                f"Pregunta {qid}: el valor debe ser un entero entre "
                f"{MIN_ANSWER} y {MAX_ANSWER} (recibido: {value!r}).")


def score_incident(answers: dict[int, int]) -> Assessment:
    """Calcula el puntaje total (5-25) y resuelve la categoría de prioridad.

    Regla del informe: ante un dato desconocido, el evaluador debe asignar
    el valor más conservador (el mayor) antes de llamar a esta función.
    """
    validate_answers(answers)
    total = sum(answers.values())
    category = next(c for c in PRIORITY_CATEGORIES if c.contains(total))
    return Assessment(answers=dict(answers), total=total, category=category)
