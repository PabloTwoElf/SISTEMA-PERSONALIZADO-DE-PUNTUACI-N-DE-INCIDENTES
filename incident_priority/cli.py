"""Interfaz de consola: presenta las preguntas, lee respuestas y muestra
el resultado. No contiene reglas de negocio (separación de responsabilidades)."""
from collections.abc import Callable

from .domain import MAX_ANSWER, MIN_ANSWER, PRIORITY_CATEGORIES, QUESTIONS
from .scoring import score_incident

LINE = "─" * 72


def _ask_value(prompt: str, input_fn: Callable[[str], str], output_fn: Callable[..., None]) -> int:
    while True:
        raw = input_fn(prompt).strip()
        try:
            value = int(raw)
            if MIN_ANSWER <= value <= MAX_ANSWER:
                return value
        except ValueError:
            pass
        output_fn(f"  → Ingresa un entero entre {MIN_ANSWER} y {MAX_ANSWER}.")


def _render_question(output_fn: Callable[..., None], question_id: int, dimension: str,
                     text: str, criteria: tuple[str, str, str, str, str]) -> None:
    output_fn(f"\n[{dimension}] Pregunta {question_id}. {text}")
    for index, criterion in enumerate(criteria, start=1):
        output_fn(f"   {index}. {criterion}")


def _collect_answers(input_fn: Callable[[str], str], output_fn: Callable[..., None]) -> dict[int, int]:
    answers: dict[int, int] = {}
    for question in QUESTIONS:
        _render_question(output_fn, question.id, question.dimension.value, question.text, question.criteria)
        answers[question.id] = _ask_value("   Valor (1-5): ", input_fn, output_fn)
    return answers


def _render_result(output_fn: Callable[..., None], result) -> None:
    output_fn(f"\n{LINE}")
    output_fn(f"PUNTAJE TOTAL: {result.total} / 25")
    output_fn(f"PRIORIDAD:     {result.category.name} ({result.category.code})")
    output_fn(f"RESPUESTA:     {result.category.response_time}")
    output_fn(LINE)
    output_fn("Escala de referencia:")
    for category in PRIORITY_CATEGORIES:
        marker = "◄" if category is result.category else " "
        output_fn(f"  {category.min_score:>2}-{category.max_score:<2} {category.name:<8} ({category.code}) {marker}")


def run(input_fn: Callable[[str], str] = input, output_fn: Callable[..., None] = print) -> None:
    output_fn(LINE)
    output_fn("SISTEMA DE PUNTUACIÓN DE INCIDENTES — ISWZ-3208 · Equipo 5")
    output_fn("Responde cada pregunta con un valor de 1 a 5 según el criterio.")
    output_fn("Si un dato es desconocido, asigna el valor MÁS ALTO aplicable")
    output_fn("(regla conservadora) y reevalúa al confirmar la información.")
    output_fn(LINE)

    result = score_incident(_collect_answers(input_fn, output_fn))
    _render_result(output_fn, result)
