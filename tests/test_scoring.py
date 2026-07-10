"""Tests que reproducen la validación del informe (sección I.4):
los tres incidentes simulados deben clasificarse exactamente igual.
Ejecutar: python -m pytest -v  (o python -m unittest discover -v)
"""
import unittest

from incident_priority.scoring import score_incident


class TestIncidentesSimuladosDelInforme(unittest.TestCase):
    def test_incidente_1_caida_bd_facturacion_es_critica(self):
        r = score_incident({1: 4, 2: 5, 3: 2, 4: 5, 5: 5})
        self.assertEqual(r.total, 21)
        self.assertEqual(r.category.name, "Crítica")
        self.assertEqual(r.category.code, "P1")

    def test_incidente_2_impresora_contabilidad_es_baja(self):
        r = score_incident({1: 3, 2: 2, 3: 1, 4: 2, 5: 2})
        self.assertEqual(r.total, 10)
        self.assertEqual(r.category.name, "Baja")
        self.assertEqual(r.category.code, "P4")

    def test_incidente_3_phishing_credenciales_es_alta(self):
        r = score_incident({1: 1, 2: 3, 3: 5, 4: 4, 5: 5})
        self.assertEqual(r.total, 18)
        self.assertEqual(r.category.name, "Alta")
        self.assertEqual(r.category.code, "P2")


class TestLimitesYValidaciones(unittest.TestCase):
    def test_puntaje_minimo_es_baja(self):
        r = score_incident({1: 1, 2: 1, 3: 1, 4: 1, 5: 1})
        self.assertEqual((r.total, r.category.code), (5, "P4"))

    def test_puntaje_maximo_es_critica(self):
        r = score_incident({1: 5, 2: 5, 3: 5, 4: 5, 5: 5})
        self.assertEqual((r.total, r.category.code), (25, "P1"))

    def test_bordes_de_categorias(self):
        # 10→Baja, 11→Media, 15→Media, 16→Alta, 20→Alta, 21→Crítica
        casos = {10: "P4", 11: "P3", 15: "P3", 16: "P2", 20: "P2", 21: "P1"}
        for total, code in casos.items():
            base, resto = divmod(total - 5, 5)  # reparte total en 5 respuestas 1..5
            answers = {i: 1 + base + (1 if i <= resto else 0) for i in range(1, 6)}
            r = score_incident(answers)
            self.assertEqual(r.total, total)
            self.assertEqual(r.category.code, code, f"total={total}")

    def test_valor_fuera_de_rango_lanza_error(self):
        with self.assertRaises(ValueError):
            score_incident({1: 0, 2: 3, 3: 3, 4: 3, 5: 3})
        with self.assertRaises(ValueError):
            score_incident({1: 6, 2: 3, 3: 3, 4: 3, 5: 3})

    def test_respuestas_incompletas_lanza_error(self):
        with self.assertRaises(ValueError):
            score_incident({1: 3, 2: 3, 3: 3, 4: 3})


if __name__ == "__main__":
    unittest.main()
