import unittest
import os
import json
import tempfile
import sys 
from Modulo_Miembros import Miembro, MiembrosManager

class TestMiembro(unittest.TestCase):
    """Pruebas unitarias para la clase Miembro"""
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        self.miembro = Miembro(1, "Juan Perez", "juan@test.com", "12345678")
    
    def test_creacion_miembro(self):
        """Prueba la creación de un miembro"""
        self.assertEqual(self.miembro.id, 1)
        self.assertEqual(self.miembro.nombre, "Juan Perez")
        self.assertEqual(self.miembro.email, "juan@test.com")
        self.assertEqual(self.miembro.telefono, "12345678")
        self.assertIsNotNone(self.miembro.fecha_registro)
    
    def test_to_dict(self):
        """Prueba la conversión a diccionario"""
        data = self.miembro.to_dict()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["nombre"], "Juan Perez")
        self.assertEqual(data["email"], "juan@test.com")
        self.assertEqual(data["telefono"], "12345678")
        self.assertIn("fecha_registro", data)
    
    def test_from_dict(self):
        """Prueba la creación desde diccionario"""
        data = {
            "id": 2,
            "nombre": "Maria Lopez",
            "email": "maria@test.com",
            "telefono": "87654321",
            "fecha_registro": "2026-01-01 10:00:00"
        }
        miembro = Miembro.from_dict(data)
        self.assertEqual(miembro.id, 2)
        self.assertEqual(miembro.nombre, "Maria Lopez")
        self.assertEqual(miembro.fecha_registro, "2026-01-01 10:00:00")
    
    def test_str(self):
        """Prueba la representación en string"""
        self.assertIn("Juan Perez", str(self.miembro))
        self.assertIn("1", str(self.miembro))


class TestMiembrosManager(unittest.TestCase):
    """Pruebas unitarias para MiembrosManager"""
    
    def setUp(self):
        """Crea un archivo temporal para pruebas"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.archivo_temp = self.temp_file.name
        self.manager = MiembrosManager(self.archivo_temp)
    
    def tearDown(self):
        """Limpia el archivo temporal después de cada prueba"""
        if os.path.exists(self.archivo_temp):
            os.unlink(self.archivo_temp)
    
    def test_agregar_miembro(self):
        """Prueba agregar un miembro"""
        resultado = self.manager.agregar_miembro("Test User", "test@test.com", "99999999")
        self.assertIsNotNone(resultado)
        self.assertEqual(len(self.manager.miembros), 1)
        self.assertEqual(self.manager.miembros[0].nombre, "Test User")
    
    def test_agregar_miembro_email_duplicado(self):
        """Prueba que no se puedan duplicar emails"""
        self.manager.agregar_miembro("User Uno", "duplicate@test.com", "11111111")
        resultado = self.manager.agregar_miembro("User Dos", "duplicate@test.com", "22222222")
        self.assertIsNone(resultado)
        self.assertEqual(len(self.manager.miembros), 1)
    
    def test_agregar_miembro_email_invalido(self):
        """Prueba que el email debe ser válido"""
        resultado = self.manager.agregar_miembro("User", "email-invalido", "12345678")
        self.assertIsNone(resultado)
        self.assertEqual(len(self.manager.miembros), 0)
    
    def test_agregar_miembro_nombre_vacio(self):
        """Prueba que el nombre no puede estar vacío"""
        resultado = self.manager.agregar_miembro("", "test@test.com", "12345678")
        self.assertIsNone(resultado)
        self.assertEqual(len(self.manager.miembros), 0)
    
    def test_buscar_miembro_por_nombre(self):
        """Prueba búsqueda por nombre"""
        self.manager.agregar_miembro("Carlos Ruiz", "carlos@test.com", "11111111")
        self.manager.agregar_miembro("Ana Ruiz", "ana@test.com", "22222222")
        
        resultados = self.manager.buscar_miembro("Carlos")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].nombre, "Carlos Ruiz")
    
    def test_buscar_miembro_por_email(self):
        """Prueba búsqueda por email"""
        self.manager.agregar_miembro("Test User", "buscar@test.com", "33333333")
        
        resultados = self.manager.buscar_miembro("buscar@test.com")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].email, "buscar@test.com")
    
    def test_buscar_miembro_por_id(self):
        """Prueba búsqueda por ID"""
        miembro = self.manager.agregar_miembro("ID User", "id@test.com", "44444444")
        
        resultados = self.manager.buscar_miembro(str(miembro.id))
        self.assertEqual(len(resultados), 1)
    
    def test_obtener_miembro_por_id(self):
        """Prueba obtener miembro por ID"""
        self.manager.agregar_miembro("User A", "a@test.com", "55555555")
        miembro = self.manager.agregar_miembro("User B", "b@test.com", "66666666")
        
        encontrado = self.manager.obtener_miembro_por_id(miembro.id)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombre, "User B")
        
        no_encontrado = self.manager.obtener_miembro_por_id(999)
        self.assertIsNone(no_encontrado)
    
    def test_actualizar_miembro(self):
        """Prueba actualizar un miembro"""
        self.manager.agregar_miembro("Original", "original@test.com", "77777777")
        miembro = self.manager.miembros[0]
        
        resultado = self.manager.actualizar_miembro(miembro.id, nombre="Actualizado", email="nuevo@test.com")
        self.assertTrue(resultado)
        self.assertEqual(self.manager.miembros[0].nombre, "Actualizado")
        self.assertEqual(self.manager.miembros[0].email, "nuevo@test.com")
    
    def test_actualizar_miembro_no_existente(self):
        """Prueba actualizar un miembro que no existe"""
        resultado = self.manager.actualizar_miembro(999, nombre="Nuevo")
        self.assertFalse(resultado)
    
    def test_eliminar_miembro(self):
        """Prueba eliminar un miembro"""
        self.manager.agregar_miembro("Para Eliminar", "eliminar@test.com", "88888888")
        miembro = self.manager.miembros[0]
        
        self.assertEqual(len(self.manager.miembros), 1)
        resultado = self.manager.eliminar_miembro(miembro.id)
        self.assertTrue(resultado)
        self.assertEqual(len(self.manager.miembros), 0)
    
    def test_eliminar_miembro_no_existente(self):
        """Prueba eliminar un miembro que no existe"""
        resultado = self.manager.eliminar_miembro(999)
        self.assertFalse(resultado)
    
    def test_obtener_siguiente_id(self):
        """Prueba obtener el siguiente ID disponible"""
        self.assertEqual(self.manager.obtener_siguiente_id(), 1)
        
        self.manager.agregar_miembro("User Uno", "u1@test.com", "11111111")
        self.manager.agregar_miembro("User Dos", "u2@test.com", "22222222")
        
        self.assertEqual(self.manager.obtener_siguiente_id(), 3)
    
    def test_agregar_miembro_nombre_invalido(self):
        """Prueba que el nombre no puede contener números o caracteres especiales"""
        resultado = self.manager.agregar_miembro("User123", "test@test.com", "12345678")
        self.assertIsNone(resultado)
        resultado2 = self.manager.agregar_miembro("User#", "test@test.com", "12345678")
        self.assertIsNone(resultado2)

    def test_agregar_miembro_telefono_invalido(self):
        """Prueba que el teléfono debe tener formato válido (solo dígitos, espacios, guiones y longitud 6-15)"""
        # Contiene letras
        resultado = self.manager.agregar_miembro("Test User", "test@test.com", "123-abc")
        self.assertIsNone(resultado)
        # Muy corto
        resultado2 = self.manager.agregar_miembro("Test User", "test@test.com", "123")
        self.assertIsNone(resultado2)
        # Muy largo
        resultado3 = self.manager.agregar_miembro("Test User", "test@test.com", "1" * 16)
        self.assertIsNone(resultado3)

    def test_agregar_miembro_email_formato_invalido(self):
        """Prueba que el email debe cumplir un formato real (ej: usuario@dominio.com)"""
        # Sin extensión de dominio
        resultado = self.manager.agregar_miembro("Test User", "test@test", "12345678")
        self.assertIsNone(resultado)
        # Sin @ ni punto
        resultado2 = self.manager.agregar_miembro("Test User", "testdomaincom", "12345678")
        self.assertIsNone(resultado2)

    def test_persistencia_json(self):
        """Prueba que los datos se guarden correctamente en JSON"""
        self.manager.agregar_miembro("Persistente", "persist@test.com", "99999999")
        
        # Crear un nuevo manager con el mismo archivo
        nuevo_manager = MiembrosManager(self.archivo_temp)
        self.assertEqual(len(nuevo_manager.miembros), 1)
        self.assertEqual(nuevo_manager.miembros[0].nombre, "Persistente")


if __name__ == "__main__":
    unittest.main()