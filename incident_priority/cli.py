"""Interfaz de consola: presenta las preguntas, lee respuestas y muestra
el resultado. No contiene reglas de negocio (separación de responsabilidades)."""
from .domain import MAX_ANSWER, MIN_ANSWER, PRIORITY_CATEGORIES, QUESTIONS
from .scoring import score_incident

LINE = "─" * 72


def _ask_value(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if MIN_ANSWER <= value <= MAX_ANSWER:
                return value
        except ValueError:
            pass
        print(f"  → Ingresa un entero entre {MIN_ANSWER} y {MAX_ANSWER}.")


def run() -> None:
    print(LINE)
    print("SISTEMA DE PUNTUACIÓN DE INCIDENTES — ISWZ-3208 · Equipo 5")
    print("Responde cada pregunta con un valor de 1 a 5 según el criterio.")
    print("Si un dato es desconocido, asigna el valor MÁS ALTO aplicable")
    print("(regla conservadora) y reevalúa al confirmar la información.")
    print(LINE)

    answers: dict[int, int] = {}
    for q in QUESTIONS:
        print(f"\n[{q.dimension.value}] Pregunta {q.id}. {q.text}")
        for i, criterion in enumerate(q.criteria, start=1):
            print(f"   {i}. {criterion}")
        answers[q.id] = _ask_value("   Valor (1-5): ")

    result = score_incident(answers)
    print(f"\n{LINE}")
    print(f"PUNTAJE TOTAL: {result.total} / 25")
    print(f"PRIORIDAD:     {result.category.name} ({result.category.code})")
    print(f"RESPUESTA:     {result.category.response_time}")
    print(LINE)
    print("Escala de referencia:")
    for c in PRIORITY_CATEGORIES:
        marker = "◄" if c is result.category else " "
        print(f"  {c.min_score:>2}-{c.max_score:<2} {c.name:<8} ({c.code}) {marker}")
