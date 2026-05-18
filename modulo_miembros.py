
import json
import os
from datetime import datetime

# Archivo donde se almacenarán los datos
ARCHIVO_DATOS = "miembros.json"


class Miembro:
    """Clase que representa a un miembro"""
    
    def __init__(self, id_miembro, nombre, email, telefono, fecha_registro=None):
        self.id = id_miembro
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.fecha_registro = fecha_registro or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        """Convierte el objeto a diccionario para JSON"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "fecha_registro": self.fecha_registro
        }
    
    @staticmethod
    def from_dict(datos):
        """Crea un objeto Miembro desde un diccionario"""
        return Miembro(
            datos["id"],
            datos["nombre"],
            datos["email"],
            datos["telefono"],
            datos["fecha_registro"]
        )


## FUNCIONES DE PERSISTENCIA ##

def cargar_datos():
    """Carga los miembros desde el archivo JSON"""
    if not os.path.exists(ARCHIVO_DATOS):
        return []
    
    try:
        with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            return [Miembro.from_dict(m) for m in datos]
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def guardar_datos(miembros):
    """Guarda los miembros en el archivo JSON"""
    with open(ARCHIVO_DATOS, 'w', encoding='utf-8') as archivo:
        json.dump([m.to_dict() for m in miembros], archivo, indent=4, ensure_ascii=False)


## CRUD ##

def generar_id(miembros):
    """Genera un nuevo ID único automáticamente"""
    if not miembros:
        return 1
    return max(m.id for m in miembros) + 1


def validar_nombre(nombre):
    """Valida que el nombre no esté vacío y sea razonable"""
    if not nombre or not nombre.strip():
        return False, "El nombre no puede estar vacío"
    if len(nombre) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"
    if len(nombre) > 100:
        return False, "El nombre es demasiado largo (máx 100 caracteres)"
    return True, ""


def validar_email(email, miembros, id_actual=None):
    """Valida el formato del email y que no esté duplicado"""
    if not email or not email.strip():
        return False, "El email no puede estar vacío"
    
    ## Validación básica de formato ##
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Formato de email inválido"
    
    ## Verificar duplicados (excluyendo al miembro actual en edición) ##
    for m in miembros:
        if m.email.lower() == email.lower():
            if id_actual is None or m.id != id_actual:
                return False, f"El email {email} ya está registrado"
    
    return True, ""


def validar_telefono(telefono):
    """Valida que el teléfono tenga un formato aceptable"""
    if not telefono or not telefono.strip():
        return False, "El teléfono no puede estar vacío"
    
    ## Eliminar espacios y guiones para la validación ##
    telefono_limpio = telefono.replace(" ", "").replace("-", "").replace("+", "")
    
    if not telefono_limpio.isdigit():
        return False, "El teléfono solo debe contener números, espacios o guiones"
    
    if len(telefono_limpio) < 7 or len(telefono_limpio) > 15:
        return False, "El teléfono debe tener entre 7 y 15 dígitos"
    
    return True, ""


def crear_miembro():
    """Crea un nuevo miembro con validaciones"""
    miembros = cargar_datos()
    
    print("\n=== CREAR NUEVO MIEMBRO ===\n")
    
    ## Validar nombre ##
    while True:
        nombre = input("Nombre completo: ").strip()
        valido, mensaje = validar_nombre(nombre)
        if valido:
            break
        print(f"❌ Error: {mensaje}")
    
    ## Validar email ##
    while True:
        email = input("Email: ").strip().lower()
        valido, mensaje = validar_email(email, miembros)
        if valido:
            break
        print(f"❌ Error: {mensaje}")
    
    ## Validar teléfono ##
    while True:
        telefono = input("Teléfono: ").strip()
        valido, mensaje = validar_telefono(telefono)
        if valido:
            break
        print(f"❌ Error: {mensaje}")
    
    ## Crear miembro con ID automático ##
    nuevo_id = generar_id(miembros)
    nuevo_miembro = Miembro(nuevo_id, nombre, email, telefono)
    
    ## Guardar ##
    miembros.append(nuevo_miembro)
    guardar_datos(miembros)
    
    print(f"\n✅ Miembro creado exitosamente con ID: {nuevo_id}")
    return nuevo_miembro


def listar_miembros():
    """Lista todos los miembros registrados"""
    miembros = cargar_datos()
    
    print("\n=== LISTA DE MIEMBROS ===\n")
    
    if not miembros:
        print("No hay miembros registrados.")
        return
    
    print(f"{'ID':<5} {'NOMBRE':<30} {'EMAIL':<35} {'TELÉFONO':<15} {'FECHA REGISTRO':<20}")
    print("-" * 110)
    
    for m in miembros:
        print(f"{m.id:<5} {m.nombre[:30]:<30} {m.email[:35]:<35} {m.telefono:<15} {m.fecha_registro:<20}")
    
    print(f"\nTotal de miembros: {len(miembros)}")


def buscar_miembro_por_id(id_buscar, miembros):
    """Busca un miembro por su ID"""
    for m in miembros:
        if m.id == id_buscar:
            return m
    return None


def editar_miembro():
    """Edita un miembro existente"""
    miembros = cargar_datos()
    
    print("\n=== EDITAR MIEMBRO ===\n")
    
    if not miembros:
        print("No hay miembros para editar.")
        return
    
    try:
        id_editar = int(input("Ingrese el ID del miembro a editar: "))
    except ValueError:
        print("❌ Error: ID inválido")
        return
    
    miembro = buscar_miembro_por_id(id_editar, miembros)
    
    if not miembro:
        print(f"❌ Error: No existe un miembro con ID {id_editar}")
        return
    
    print(f"\nEditando miembro: {miembro.nombre} (ID: {miembro.id})")
    print("(Deje en blanco para mantener el valor actual)\n")
    
    ## Editar nombre ##
    nuevo_nombre = input(f"Nombre [{miembro.nombre}]: ").strip()
    if nuevo_nombre:
        valido, mensaje = validar_nombre(nuevo_nombre)
        if valido:
            miembro.nombre = nuevo_nombre
        else:
            print(f"❌ {mensaje} - Se mantiene el nombre anterior")
    
    ## Editar email ##
    nuevo_email = input(f"Email [{miembro.email}]: ").strip().lower()
    if nuevo_email:
        valido, mensaje = validar_email(nuevo_email, miembros, miembro.id)
        if valido:
            miembro.email = nuevo_email
        else:
            print(f"❌ {mensaje} - Se mantiene el email anterior")
    
    ## Editar teléfono ##
    nuevo_telefono = input(f"Teléfono [{miembro.telefono}]: ").strip()
    if nuevo_telefono:
        valido, mensaje = validar_telefono(nuevo_telefono)
        if valido:
            miembro.telefono = nuevo_telefono
        else:
            print(f"❌ {mensaje} - Se mantiene el teléfono anterior")
    
    ## Guardar cambios ##
    guardar_datos(miembros)
    print("\n✅ Miembro actualizado exitosamente")


def eliminar_miembro():
    """Elimina un miembro del sistema"""
    miembros = cargar_datos()
    
    print("\n=== ELIMINAR MIEMBRO ===\n")
    
    if not miembros:
        print("No hay miembros para eliminar.")
        return
    
    try:
        id_eliminar = int(input("Ingrese el ID del miembro a eliminar: "))
    except ValueError:
        print("❌ Error: ID inválido")
        return
    
    miembro = buscar_miembro_por_id(id_eliminar, miembros)
    
    if not miembro:
        print(f"❌ Error: No existe un miembro con ID {id_eliminar}")
        return
    
    ## Mostrar información del miembro a eliminar ##
    print(f"\n⚠️  Va a eliminar al siguiente miembro:")
    print(f"   ID: {miembro.id}")
    print(f"   Nombre: {miembro.nombre}")
    print(f"   Email: {miembro.email}")
    
    confirmacion = input("\n¿Está seguro? (S/N): ").strip().lower()
    
    if confirmacion == 'S':
        miembros.remove(miembro)
        guardar_datos(miembros)
        print("\n✅ Miembro eliminado exitosamente")
    else:
        print("\n❌ Operación cancelada")


# ============ MENÚ PRINCIPAL ============ 

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 50)
    print("      SISTEMA DE GESTIÓN DE MIEMBROS")
    print("=" * 50)
    print("1. Crear nuevo miembro")
    print("2. Listar todos los miembros")
    print("3. Editar miembro")
    print("4. Eliminar miembro")
    print("5. Salir")
    print("=" * 50)


def main():
    """Función principal del módulo"""
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-5): ").strip()
        
        if opcion == "1":
            crear_miembro()
        elif opcion == "2":
            listar_miembros()
        elif opcion == "3":
            editar_miembro()
        elif opcion == "4":
            eliminar_miembro()
        elif opcion == "5":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n❌ Opción inválida. Por favor, seleccione 1-5")
        
        input("\nPresione Enter para continuar...")


# ============ EJECUCIÓN ============

if __name__ == "__main__":
    main()