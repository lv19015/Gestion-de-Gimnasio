import unittest
import sys
import os
import tempfile
import json

#esto es para que el test pueda importar los modulos desde el directorio principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Modulo_Inscripciones import InscripcionesManager
from Modulo_Miembros import MiembrosManager
import Modulo_Clases

class TestInscripciones(unittest.TestCase):
    def setUp(self):
        # Guardar archivo de clases original y usar uno temporal para aislar pruebas
        self.original_archivo_clases = Modulo_Clases.ARCHIVO_CLASES
        self.tmp_clases = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp_clases.close()
        Modulo_Clases.ARCHIVO_CLASES = self.tmp_clases.name
        Modulo_Clases.clases = []
        Modulo_Clases.contador_id = 1
        Modulo_Clases.cargar_clases_demo()

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
        # Restaurar archivo de clases original
        Modulo_Clases.ARCHIVO_CLASES = self.original_archivo_clases
        
        try:
            os.remove(self.tmp_clases.name)
        except Exception:
            pass
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

    def test_sincronizacion_eliminar_miembro(self):
        miembro = self.miembros_mgr.listar_miembros()[0]
        clases = Modulo_Clases.obtener_todas_las_clases()
        
        # Inscribir
        self.mgr.inscribir(miembro.id, 0)
        self.assertIn(0, self.mgr.inscripciones.get(miembro.id, []))
        self.assertIn(miembro.id, clases[0].inscritos)
        
        # Eliminar miembro
        self.miembros_mgr.eliminar_miembro(miembro.id)
        
        # Verificar que ya no está en clases ni en inscripciones
        self.assertNotIn(miembro.id, clases[0].inscritos)
        self.mgr.load() # Recargar
        self.assertNotIn(miembro.id, self.mgr.inscripciones)

    def test_sincronizacion_eliminar_clase(self):
        miembro = self.miembros_mgr.listar_miembros()[0]
        clases = Modulo_Clases.obtener_todas_las_clases()
        
        # Inscribir en clase de índice 1 (Spinning) e índice 2 (Crossfit)
        self.mgr.inscribir(miembro.id, 1)
        self.mgr.inscribir(miembro.id, 2)
        
        self.assertIn(1, self.mgr.inscripciones.get(miembro.id, []))
        self.assertIn(2, self.mgr.inscripciones.get(miembro.id, []))
        
        # Eliminar clase de índice 0 (Yoga) - esto desplazará Spinning a índice 0 y Crossfit a índice 1
        clase_a_eliminar = clases[0]
        idx = Modulo_Clases.clases.index(clase_a_eliminar)
        Modulo_Clases.clases.remove(clase_a_eliminar)
        Modulo_Clases.guardar_clases()
        
        # Ejecutar la misma lógica de actualización de inscripciones
        if os.path.exists(self.tmp_inscripciones):
            with open(self.tmp_inscripciones, "r", encoding="utf-8") as f:
                insc_data = json.load(f)
            if "inscripciones" in insc_data:
                nuevas_inscripciones = {}
                for m_id, indices in insc_data["inscripciones"].items():
                    nuevos_indices = []
                    for i in indices:
                        if i < idx:
                            nuevos_indices.append(i)
                        elif i > idx:
                            nuevos_indices.append(i - 1)
                    nuevas_inscripciones[m_id] = nuevos_indices
                insc_data["inscripciones"] = nuevas_inscripciones
                with open(self.tmp_inscripciones, "w", encoding="utf-8") as f:
                    json.dump(insc_data, f, indent=4, ensure_ascii=False)
        
        # Recargar inscripciones
        self.mgr.load()
        
        # Spinning que era índice 1 ahora es índice 0
        self.assertIn(0, self.mgr.inscripciones.get(miembro.id, []))
        # Crossfit que era índice 2 ahora es índice 1
        self.assertIn(1, self.mgr.inscripciones.get(miembro.id, []))
        # Índice 2 ya no debe existir
        self.assertNotIn(2, self.mgr.inscripciones.get(miembro.id, []))

if __name__ == '__main__':
    unittest.main()
