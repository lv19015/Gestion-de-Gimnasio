import unittest
import sys
import os
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Modulo_Inscripciones import InscripcionesManager
import Modulo_Clases


class TestInscripciones(unittest.TestCase):
    def setUp(self):
        # Asegurar que las clases esten cargadas
        Modulo_Clases.cargar_clases()

        # Crear archivo temporal para no tocar el real
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.close()
        self.tmpfile = tmp.name
        InscripcionesManager.ARCHIVO = self.tmpfile

        # Inicializar con estructura valida
        with open(self.tmpfile, 'w', encoding='utf-8') as f:
            f.write('{"miembros": []}')

        self.mgr = InscripcionesManager()

    def tearDown(self):
        try:
            os.remove(self.tmpfile)
        except Exception:
            pass

    def test_agregar_inscribir_cancelar(self):
        # Agregar miembro
        self.mgr.agregar_miembro("Test User")
        self.assertEqual(len(self.mgr.miembros), 1)
        self.assertEqual(self.mgr.miembros[0]["nombre"], "Test User")

        # Asegurar que existe al menos una clase
        clases = Modulo_Clases.obtener_todas_las_clases()
        self.assertTrue(len(clases) > 0)

        # Inscribir al miembro en la primera clase
        self.mgr.inscribir(0, 0)
        self.assertIn(0, self.mgr.miembros[0]["inscritos"])
        self.assertIn(0, clases[0].inscritos)

        # Cancelar la inscripción
        self.mgr.cancelar(0, 0)
        self.assertNotIn(0, self.mgr.miembros[0]["inscritos"])
        self.assertNotIn(0, clases[0].inscritos)


if __name__ == '__main__':
    unittest.main()
