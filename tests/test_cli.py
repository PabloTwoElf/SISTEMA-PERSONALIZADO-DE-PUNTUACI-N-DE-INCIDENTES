"""Pruebas de la interfaz de consola sin I/O real."""
import unittest

from incident_priority.cli import run


class TestCLI(unittest.TestCase):
    def test_run_muestra_resultado_esperado(self):
        answers = iter(["4", "5", "2", "5", "5"])
        output = []

        def fake_input(prompt: str) -> str:
            output.append(prompt)
            return next(answers)

        def fake_print(*args):
            output.append(" ".join(str(arg) for arg in args))

        run(input_fn=fake_input, output_fn=fake_print)

        joined = "\n".join(output)
        self.assertIn("SISTEMA DE PUNTUACIÓN DE INCIDENTES", joined)
        self.assertIn("PUNTAJE TOTAL: 21 / 25", joined)
        self.assertIn("PRIORIDAD:     Crítica (P1)", joined)


if __name__ == "__main__":
    unittest.main()