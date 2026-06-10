# tests/test_clases.py
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Modulo_Clases import Clase, validar_horario


class TestClases(unittest.TestCase):

    def test_validar_horario_numero(self):
        self.assertTrue(validar_horario(8))
        self.assertTrue(validar_horario(24))
        self.assertFalse(validar_horario(0))
        self.assertFalse(validar_horario(25))

    def test_validar_horario_formato_hhmm(self):
        self.assertTrue(validar_horario("08:00"))
        self.assertTrue(validar_horario("14:30"))
        self.assertTrue(validar_horario("23:59"))
        self.assertFalse(validar_horario("24:00"))
        self.assertFalse(validar_horario("08:60"))
        self.assertFalse(validar_horario("8:00"))

    def test_crear_clase(self):
        clase = Clase(1, "Yoga", "Maria", 8, 5)
        self.assertEqual(clase.nombre, "Yoga")
        self.assertEqual(clase.entrenador, "Maria")
        self.assertEqual(clase.horario, 8)
        self.assertEqual(clase.cupo_maximo, 5)
        self.assertEqual(len(clase.inscritos), 0)

    def test_cupo_disponible(self):
        clase = Clase(1, "Yoga", "Maria", 8, 5)
        self.assertEqual(clase.cupo_disponible(), 5)
        clase.inscritos = [1, 2]
        self.assertEqual(clase.cupo_disponible(), 3)

    def test_inscribir_miembro(self):
        clase = Clase(1, "Yoga", "Maria", 8, 2)
        self.assertTrue(clase.inscribir_miembro(1))
        self.assertFalse(clase.inscribir_miembro(1))
        self.assertTrue(clase.inscribir_miembro(2))
        self.assertFalse(clase.inscribir_miembro(3))


if __name__ == "__main__":
    unittest.main()