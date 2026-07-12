"""Lógica de cálculo de prioridad. Pura y sin I/O: fácil de testear."""
from collections.abc import Mapping
from dataclasses import dataclass

from .domain import (MAX_ANSWER, MIN_ANSWER, PRIORITY_CATEGORIES, QUESTIONS,
                     PriorityCategory)


@dataclass(frozen=True)
class Assessment:
    """Resultado inmutable de evaluar un incidente."""
    answers: dict[int, int]
    total: int
    category: PriorityCategory


def _validate_coverage(answers: Mapping[int, int]) -> None:
    expected = {q.id for q in QUESTIONS}
    received = set(answers)
    if received != expected:
        missing = sorted(expected - received)
        extra = sorted(received - expected)
        raise ValueError(
            f"Respuestas inválidas. Faltan preguntas {missing}, sobran {extra}.")


def _validate_ranges(answers: Mapping[int, int]) -> None:
    for qid, value in answers.items():
        if not isinstance(value, int) or not MIN_ANSWER <= value <= MAX_ANSWER:
            raise ValueError(
                f"Pregunta {qid}: el valor debe ser un entero entre "
                f"{MIN_ANSWER} y {MAX_ANSWER} (recibido: {value!r}).")


def validate_answers(answers: Mapping[int, int]) -> None:
    """Valida completitud y rango. Lanza ValueError con mensaje claro."""
    _validate_coverage(answers)
    _validate_ranges(answers)


def total_score(answers: Mapping[int, int]) -> int:
    """Suma los valores validados de un incidente."""
    return sum(answers.values())


def resolve_category(total: int) -> PriorityCategory:
    """Selecciona la categoría de prioridad que corresponde al puntaje."""
    return next(c for c in PRIORITY_CATEGORIES if c.contains(total))


def score_incident(answers: Mapping[int, int]) -> Assessment:
    """Calcula el puntaje total (5-25) y resuelve la categoría de prioridad.

    Regla del informe: ante un dato desconocido, el evaluador debe asignar
    el valor más conservador (el mayor) antes de llamar a esta función.
    """
    validate_answers(answers)
    total = total_score(answers)
    category = resolve_category(total)
    return Assessment(answers=dict(answers), total=total, category=category)
