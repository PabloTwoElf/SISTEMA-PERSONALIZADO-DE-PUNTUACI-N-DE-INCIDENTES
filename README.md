# Sistema de Puntuación de Incidentes

Implementación funcional del sistema descrito en el informe del Grupo 5
(ISWZ-3208 · Calidad de Software): clasifica incidentes en categorías de
prioridad según su impacto (preguntas 1–3) y urgencia (preguntas 4–5).

## Requisitos

Python 3.10+. Sin dependencias externas.

## Ejecución en VS Code

1. Abrir la carpeta `sistema-puntuacion-incidentes` en VS Code.
2. Presionar `F5` (configuración incluida en `.vscode/launch.json`), o en la terminal:

```bash
python main.py
```

Responde las 5 preguntas con valores 1–5; el programa muestra el puntaje
total (5–25), la prioridad (Crítica/Alta/Media/Baja) y el tiempo de respuesta.

## Tests

Reproducen la validación del informe (los 3 incidentes simulados) más casos
de borde y validación de entradas:

```bash
python -m unittest discover -v
```

## Arquitectura

```
incident_priority/
├── domain.py    # Preguntas, criterios y categorías (fuente única de verdad)
├── scoring.py   # Cálculo puro: validación + puntaje + categoría
└── cli.py       # Presentación por consola (sin reglas de negocio)
main.py          # Punto de entrada
tests/           # Validación automatizada
```

Decisiones: el dominio es inmutable (`dataclass(frozen=True)`) y declarativo —
agregar o recalibrar una pregunta no toca la lógica de cálculo (Open/Closed);
`scoring.py` es puro y sin I/O, lo que permite testearlo sin mocks; la CLI solo
formatea e interactúa (Single Responsibility).
