import json
import os
from datetime import datetime
from typing import List, Optional, Dict

class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

ARCHIVO_MIEMBROS = "miembros.json"

class Miembro:
    """Clase que representa a un miembro del gimnasio"""
    
    def __init__(self, id_miembro: int, nombre: str, email: str, telefono: str, fecha_registro: str = None):
        self.id = id_miembro
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.fecha_registro = fecha_registro or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict:
        """Convierte el objeto a diccionario para JSON"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "fecha_registro": self.fecha_registro
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Miembro':
        """Crea un objeto Miembro desde un diccionario"""
        return cls(
            id_miembro=data["id"],
            nombre=data["nombre"],
            email=data["email"],
            telefono=data["telefono"],
            fecha_registro=data.get("fecha_registro")
        )

    def __str__(self) -> str:
        return f"{self.nombre} (ID: {self.id}) - {self.email}"


class MiembrosManager:
    """Gestor de miembros del gimnasio"""
    
    def __init__(self, archivo: str = ARCHIVO_MIEMBROS):
        self.archivo = archivo
        self.miembros: List[Miembro] = []
        self.cargar_miembros()

    def cargar_miembros(self) -> bool:
        """Carga los miembros desde el archivo JSON"""
        try:
            if os.path.exists(self.archivo):
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read().strip()
                    if contenido:
                        # Manejar formato con múltiples objetos JSON (como en la imagen)
                        if contenido.startswith('['):
                            datos = json.loads(contenido)
                        else:
                            # Si son líneas separadas, envolver en array
                            lineas = [l.strip() for l in contenido.split('\n') if l.strip()]
                            datos = []
                            for linea in lineas:
                                if linea.endswith(','):
                                    linea = linea[:-1]
                                try:
                                    datos.append(json.loads(linea))
                                except:
                                    pass
                        self.miembros = [Miembro.from_dict(d) for d in datos]
                        print(Color.GREEN + f"[OK] Cargados {len(self.miembros)} miembros." + Color.RESET)
                        return True
            print(Color.YELLOW + "[Info] No se encontró archivo miembros.json. Se creará uno nuevo." + Color.RESET)
            self.miembros = []
            self._guardar()
            return True
        except Exception as e:
            print(Color.RED + f"[Error] No se pudo cargar miembros.json: {e}" + Color.RESET)
            self.miembros = []
            return False

    def _guardar(self) -> bool:
        """Guarda los miembros en el archivo JSON"""
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump([m.to_dict() for m in self.miembros], f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(Color.RED + f"[Error] No se pudo guardar: {e}" + Color.RESET)
            return False

    def obtener_siguiente_id(self) -> int:
        """Obtiene el siguiente ID disponible"""
        if not self.miembros:
            return 1
        return max(m.id for m in self.miembros) + 1

    def agregar_miembro(self, nombre: str, email: str, telefono: str) -> Optional[Miembro]:
        """Agrega un nuevo miembro"""
        # Validaciones
        if not nombre or not nombre.strip():
            print(Color.RED + "[Error] El nombre no puede estar vacío." + Color.RESET)
            return None
        if not email or '@' not in email:
            print(Color.RED + "[Error] Email inválido." + Color.RESET)
            return None
        
        # Verificar email duplicado
        for m in self.miembros:
            if m.email.lower() == email.lower():
                print(Color.RED + f"[Error] Ya existe un miembro con el email {email}" + Color.RESET)
                return None

        nuevo_id = self.obtener_siguiente_id()
        nuevo = Miembro(nuevo_id, nombre.strip(), email.strip(), telefono.strip())
        self.miembros.append(nuevo)
        
        if self._guardar():
            print(Color.GREEN + f"[OK] Miembro '{nombre}' agregado con ID {nuevo_id}" + Color.RESET)
            return nuevo
        return None

    def buscar_miembro(self, criterio: str) -> List[Miembro]:
        """Busca miembros por nombre, email o ID"""
        resultados = []
        criterio = criterio.lower().strip()
        
        # Buscar por ID si es número
        if criterio.isdigit():
            for m in self.miembros:
                if str(m.id) == criterio:
                    resultados.append(m)
        else:
            for m in self.miembros:
                if criterio in m.nombre.lower() or criterio in m.email.lower():
                    resultados.append(m)
        return resultados

    def obtener_miembro_por_id(self, id_miembro: int) -> Optional[Miembro]:
        """Obtiene un miembro por su ID"""
        for m in self.miembros:
            if m.id == id_miembro:
                return m
        return None

    def actualizar_miembro(self, id_miembro: int, nombre: str = None, email: str = None, telefono: str = None) -> bool:
        """Actualiza los datos de un miembro"""
        miembro = self.obtener_miembro_por_id(id_miembro)
        if not miembro:
            print(Color.RED + f"[Error] No se encontró miembro con ID {id_miembro}" + Color.RESET)
            return False

        if nombre and nombre.strip():
            miembro.nombre = nombre.strip()
        if email and email.strip():
            if '@' not in email:
                print(Color.RED + "[Error] Email inválido." + Color.RESET)
                return False
            # Verificar que el nuevo email no esté en uso por otro miembro
            for m in self.miembros:
                if m.email.lower() == email.lower() and m.id != id_miembro:
                    print(Color.RED + f"[Error] El email {email} ya está en uso." + Color.RESET)
                    return False
            miembro.email = email.strip()
        if telefono and telefono.strip():
            miembro.telefono = telefono.strip()

        if self._guardar():
            print(Color.GREEN + f"[OK] Miembro ID {id_miembro} actualizado." + Color.RESET)
            return True
        return False

    def eliminar_miembro(self, id_miembro: int) -> bool:
        """Elimina un miembro por su ID"""
        miembro = self.obtener_miembro_por_id(id_miembro)
        if not miembro:
            print(Color.RED + f"[Error] No se encontró miembro con ID {id_miembro}" + Color.RESET)
            return False

        self.miembros.remove(miembro)
        if self._guardar():
            print(Color.GREEN + f"[OK] Miembro '{miembro.nombre}' eliminado." + Color.RESET)
            return True
        return False

    def listar_miembros(self) -> List[Miembro]:
        """Retorna todos los miembros"""
        return self.miembros.copy()

    def mostrar_tabla_miembros(self):
        """Muestra los miembros en formato de tabla con colores"""
        if not self.miembros:
            print(Color.YELLOW + "No hay miembros registrados." + Color.RESET)
            return

        print(Color.CYAN + "\n" + "=" * 80 + Color.RESET)
        print(Color.BOLD + Color.MAGENTA + f"{'ID':<6} {'NOMBRE':<25} {'EMAIL':<30} {'TELÉFONO':<15}" + Color.RESET)
        print(Color.CYAN + "-" * 80 + Color.RESET)
        
        for m in self.miembros:
            print(f"{Color.GREEN}{m.id:<6}{Color.RESET} "
                  f"{Color.WHITE}{m.nombre[:24]:<25}{Color.RESET} "
                  f"{Color.CYAN}{m.email[:29]:<30}{Color.RESET} "
                  f"{Color.YELLOW}{m.telefono:<15}{Color.RESET}")
        
        print(Color.CYAN + "=" * 80 + Color.RESET)
        print(Color.GREEN + f"Total de miembros: {len(self.miembros)}" + Color.RESET)


def menu_miembros(manager: MiembrosManager):
    """Menú interactivo para gestionar miembros"""
    while True:
        print(Color.MAGENTA + "\n" + "#" * 50 + Color.RESET)
        print(Color.CYAN + Color.BOLD + "          GESTIÓN DE MIEMBROS" + Color.RESET)
        print(Color.MAGENTA + "#" * 50 + Color.RESET)
        print(Color.GREEN + "1. Listar todos los miembros" + Color.RESET)
        print(Color.GREEN + "2. Buscar miembro" + Color.RESET)
        print(Color.GREEN + "3. Agregar nuevo miembro" + Color.RESET)
        print(Color.GREEN + "4. Actualizar miembro" + Color.RESET)
        print(Color.GREEN + "5. Eliminar miembro" + Color.RESET)
        print(Color.GREEN + "6. Volver al menú principal" + Color.RESET)
        print(Color.CYAN + "-" * 50 + Color.RESET)

        opcion = input(Color.YELLOW + "Seleccione una opción: " + Color.RESET).strip()

        if opcion == "1":
            manager.mostrar_tabla_miembros()
        elif opcion == "2":
            criterio = input("Ingrese nombre, email o ID a buscar: ").strip()
            resultados = manager.buscar_miembro(criterio)
            if resultados:
                print(Color.GREEN + f"\nEncontrados {len(resultados)} resultados:" + Color.RESET)
                print(Color.CYAN + "-" * 60 + Color.RESET)
                for m in resultados:
                    print(f"ID: {m.id} | {m.nombre} | {m.email} | {m.telefono}")
            else:
                print(Color.RED + "No se encontraron resultados." + Color.RESET)
        elif opcion == "3":
            print(Color.CYAN + "\n--- NUEVO MIEMBRO ---" + Color.RESET)
            nombre = input("Nombre: ").strip()
            email = input("Email: ").strip()
            telefono = input("Teléfono: ").strip()
            manager.agregar_miembro(nombre, email, telefono)
        elif opcion == "4":
            manager.mostrar_tabla_miembros()
            try:
                id_m = int(input("\nID del miembro a actualizar: ").strip())
                print("(Deje vacío para no cambiar)")
                nombre = input("Nuevo nombre: ").strip()
                email = input("Nuevo email: ").strip()
                telefono = input("Nuevo teléfono: ").strip()
                manager.actualizar_miembro(id_m, nombre or None, email or None, telefono or None)
            except ValueError:
                print(Color.RED + "ID inválido." + Color.RESET)
        elif opcion == "5":
            manager.mostrar_tabla_miembros()
            try:
                id_m = int(input("\nID del miembro a eliminar: ").strip())
                confirm = input(f"¿Seguro que desea eliminar al miembro ID {id_m}? (s/n): ").strip().lower()
                if confirm == 's':
                    manager.eliminar_miembro(id_m)
            except ValueError:
                print(Color.RED + "ID inválido." + Color.RESET)
        elif opcion == "6":
            break
        else:
            print(Color.RED + "Opción inválida." + Color.RESET)