import unittest
import sys
import os
import tempfile

#esto es para que el test pueda importar los modulos desde el directorio principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Modulo_Inscripciones import InscripcionesManager
from Modulo_Miembros import MiembrosManager
import Modulo_Clases

class TestInscripciones(unittest.TestCase):
    def setUp(self):
        # Asegurar que las clases esten cargadas
        Modulo_Clases.cargar_clases()

        # Crear archivo temporal para miembros
        self.tmp_miembros = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp_miembros.close()
        
        # Crear archivo temporal para inscripciones
        tmp_insc = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        tmp_insc.close()
        self.tmp_inscripciones = tmp_insc.name

        # Inicializar MiembrosManager con archivo temporal
        self.miembros_mgr = MiembrosManager(archivo=self.tmp_miembros.name)
        self.miembros_mgr.agregar_miembro("Test User", "test@example.com", "1234567890")
        
        # Inicializar InscripcionesManager con MiembrosManager
        InscripcionesManager.ARCHIVO = self.tmp_inscripciones
        self.mgr = InscripcionesManager(miembros_manager=self.miembros_mgr)

    def tearDown(self):
        try:
            os.remove(self.tmp_miembros.name)
        except Exception:
            pass
        try:
            os.remove(self.tmp_inscripciones)
        except Exception:
            pass

    def test_agregar_inscribir_cancelar(self):
        # Obtener miembro creado en setUp
        miembros = self.miembros_mgr.listar_miembros()
        self.assertEqual(len(miembros), 1)
        miembro = miembros[0]

        # Asegurar que existe al menos una clase
        clases = Modulo_Clases.obtener_todas_las_clases()
        self.assertTrue(len(clases) > 0)

        # Inscribir al miembro en la primera clase
        self.mgr.inscribir(miembro.id, 0)
        self.assertIn(0, self.mgr.inscripciones.get(miembro.id, []))
        self.assertIn(miembro.id, clases[0].inscritos)

        # Cancelar la inscripción
        self.mgr.cancelar(miembro.id, 0)
        self.assertNotIn(0, self.mgr.inscripciones.get(miembro.id, []))
        self.assertNotIn(miembro.id, clases[0].inscritos)

if __name__ == '__main__':
    unittest.main()
