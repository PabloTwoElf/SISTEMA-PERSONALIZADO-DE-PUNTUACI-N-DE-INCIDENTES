"""Pruebas estructurales del dominio del sistema de puntuación."""
import unittest

from incident_priority.domain import MAX_ANSWER, MIN_ANSWER, PRIORITY_CATEGORIES, QUESTIONS


class TestDomainStructure(unittest.TestCase):
    def test_hay_cinco_preguntas(self):
        self.assertEqual(len(QUESTIONS), 5)

    def test_cada_pregunta_tiene_cinco_criterios(self):
        self.assertTrue(all(len(question.criteria) == 5 for question in QUESTIONS))

    def test_las_categorias_cubren_todo_el_rango(self):
        expected_scores = list(range(5, 26))
        covered_scores = []
        for category in PRIORITY_CATEGORIES:
            covered_scores.extend(range(category.min_score, category.max_score + 1))

        self.assertEqual(sorted(covered_scores), expected_scores)

    def test_no_hay_huecos_entre_categorias(self):
        ordered = sorted(PRIORITY_CATEGORIES, key=lambda category: category.min_score)
        for previous, current in zip(ordered, ordered[1:]):
            self.assertEqual(previous.max_score + 1, current.min_score)

    def test_rango_de_respuestas_es_1_a_5(self):
        self.assertEqual((MIN_ANSWER, MAX_ANSWER), (1, 5))


if __name__ == "__main__":
    unittest.main()