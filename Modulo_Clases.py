# Modulo_Clases.py
# Módulo B: Gestión de Clases (CRUD completo)
# Autor: Franklin Omar García Román (GR20016)

class Clase:
    def __init__(self, id, nombre, entrenador, horario, cupo_maximo):
        self.id = id
        self.nombre = nombre
        self.entrenador = entrenador
        self.horario = horario
        self.cupo_maximo = cupo_maximo
        self.inscritos = []     # Lista de IDs de miembros inscritos
    
    def cupo_disponible(self):
        return self.cupo_maximo - len(self.inscritos)
    
    def inscribir_miembro(self, miembro_id):
        if self.cupo_disponible() > 0 and miembro_id not in self.inscritos:
            self.inscritos.append(miembro_id)
            return True
        return False
    
    def desinscribir_miembro(self, miembro_id):
        if miembro_id in self.inscritos:
            self.inscritos.remove(miembro_id)
            return True
        return False


# Datos globales
clases = []
contador_id = 1


def generar_id():
    global contador_id
    actual = contador_id
    contador_id += 1
    return actual


def validar_horario(horario):
    if isinstance(horario, int):
        return 1 <= horario <= 24
    if isinstance(horario, str) and len(horario) == 5 and horario[2] == ':':
        try:
            hora = int(horario[0:2])
            minuto = int(horario[3:5])
            return 0 <= hora <= 23 and 0 <= minuto <= 59
        except:
            return False
    return False


def buscar_clase_por_id(id_buscar):
    for clase in clases:
        if clase.id == id_buscar:
            return clase
    return None


# ========== CLASES DE DEMOSTRACIÓN AUTOMÁTICAS (SILENCIOSAS) ==========

def cargar_clases_demo_auto():
    """Carga clases de demostración automáticamente sin mostrar mensajes"""
    global contador_id
    
    if len(clases) == 0:
        clases_demo = [
            {"nombre": "Yoga", "entrenador": "María", "horario": 8, "cupo_maximo": 5},
            {"nombre": "Spinning", "entrenador": "Carlos", "horario": 8, "cupo_maximo": 1},
            {"nombre": "Crossfit", "entrenador": "Ana", "horario": 10, "cupo_maximo": 3},
        ]
        
        for demo in clases_demo:
            nueva_clase = Clase(generar_id(), demo["nombre"], demo["entrenador"], demo["horario"], demo["cupo_maximo"])
            clases.append(nueva_clase)


# ========== FUNCIONES CRUD ==========

def crear_clase():
    print("\n" + "="*40)
    print("        CREAR NUEVA CLASE")
    print("="*40)
    
    nombre = input("Nombre de la clase: ").strip()
    while not nombre:
        print("❌ El nombre no puede estar vacío")
        nombre = input("Nombre de la clase: ").strip()
    
    entrenador = input("Nombre del entrenador: ").strip()
    while not entrenador:
        print("❌ El nombre del entrenador no puede estar vacío")
        entrenador = input("Nombre del entrenador: ").strip()
    
    print("\nHorario - Opciones:")
    print("  - Número entero (ej: 8 para 8:00 AM)")
    print("  - Formato HH:MM (ej: 14:30)")
    horario_input = input("Horario: ").strip()
    
    try:
        horario = int(horario_input)
    except ValueError:
        horario = horario_input
    
    while not validar_horario(horario):
        print("❌ Horario inválido")
        horario_input = input("Horario: ").strip()
        try:
            horario = int(horario_input)
        except ValueError:
            horario = horario_input
    
    cupo = int(input("Cupo máximo: "))
    while cupo <= 0:
        print("❌ El cupo debe ser mayor a 0")
        cupo = int(input("Cupo máximo: "))
    
    nueva_clase = Clase(generar_id(), nombre, entrenador, horario, cupo)
    clases.append(nueva_clase)
    print(f"\n✅ Clase '{nombre}' creada con ID {nueva_clase.id}")


def listar_clases():
    print("\n" + "="*55)
    print("              LISTADO DE CLASES")
    print("="*55)
    
    if not clases:
        print("📭 No hay clases registradas")
        return
    
    print(f"{'ID':<5} {'Nombre':<20} {'Entrenador':<18} {'Horario':<10} {'Cupo':<10}")
    print("-" * 65)
    for c in clases:
        if isinstance(c.horario, int):
            horario_str = f"{c.horario}:00"
        else:
            horario_str = c.horario
        print(f"{c.id:<5} {c.nombre:<20} {c.entrenador:<18} {horario_str:<10} {len(c.inscritos)}/{c.cupo_maximo}")


def editar_clase():
    listar_clases()
    if not clases:
        return
    
    try:
        id_editar = int(input("\nID de la clase a editar: "))
        clase = buscar_clase_por_id(id_editar)
        
        if not clase:
            print("❌ Clase no encontrada")
            return
        
        print(f"\n--- EDITANDO: {clase.nombre} ---")
        print("(Enter para mantener valor)")
        
        nuevo_nombre = input(f"Nombre [{clase.nombre}]: ").strip()
        if nuevo_nombre:
            clase.nombre = nuevo_nombre
        
        nuevo_entrenador = input(f"Entrenador [{clase.entrenador}]: ").strip()
        if nuevo_entrenador:
            clase.entrenador = nuevo_entrenador
        
        nuevo_horario_input = input(f"Horario [{clase.horario}]: ").strip()
        if nuevo_horario_input:
            try:
                nuevo_horario = int(nuevo_horario_input)
            except ValueError:
                nuevo_horario = nuevo_horario_input
            if validar_horario(nuevo_horario):
                clase.horario = nuevo_horario
            else:
                print("❌ Horario inválido, se mantiene el original")
        
        nuevo_cupo = input(f"Cupo máximo [{clase.cupo_maximo}]: ").strip()
        if nuevo_cupo:
            nuevo_cupo = int(nuevo_cupo)
            if nuevo_cupo > 0:
                if nuevo_cupo < len(clase.inscritos):
                    print(f"⚠️ Hay {len(clase.inscritos)} inscritos. El nuevo cupo es menor.")
                    if input("¿Continuar? (s/n): ").lower() != 's':
                        return
                clase.cupo_maximo = nuevo_cupo
        
        print(f"✅ Clase actualizada")
        
    except ValueError:
        print("❌ ID inválido")


def eliminar_clase():
    listar_clases()
    if not clases:
        return
    
    try:
        id_eliminar = int(input("\nID de la clase a eliminar: "))
        clase = buscar_clase_por_id(id_eliminar)
        
        if not clase:
            print("❌ Clase no encontrada")
            return
        
        if clase.inscritos:
            print(f"⚠️ La clase tiene {len(clase.inscritos)} miembros inscritos")
            if input("¿Eliminar de todas formas? (s/n): ").lower() != 's':
                print("❌ Eliminación cancelada")
                return
        
        clases.remove(clase)
        print(f"✅ Clase eliminada")
        
    except ValueError:
        print("❌ ID inválido")


# ========== FUNCIONES DE COMPATIBILIDAD (para Inscripciones) ==========

def mostrar_clases():
    """Muestra clases en formato que espera Inscripciones"""
    print("\n========== CLASES DISPONIBLES ==========")
    if not clases:
        print("No hay clases registradas")
        return
    
    for i, c in enumerate(clases):
        if isinstance(c.horario, int):
            horario_str = f"{c.horario} AM" if c.horario < 12 else f"{c.horario} PM"
        else:
            horario_str = c.horario
        print(f"{i}. {c.nombre} | Horario: {horario_str} | Cupos: {len(c.inscritos)}/{c.cupo_maximo} | Entrenador: {c.entrenador}")


def obtener_clase_por_indice(indice):
    if 0 <= indice < len(clases):
        c = clases[indice]
        return {
            "nombre": c.nombre,
            "horario": c.horario,
            "cupo_max": c.cupo_maximo,
            "inscritos": len(c.inscritos)
        }
    return None


def obtener_todas_las_clases():
    return clases


def verificar_cupo_disponible(indice_clase):
    if 0 <= indice_clase < len(clases):
        return clases[indice_clase].cupo_disponible() > 0
    return False


def verificar_choque_horario(miembro_id, indice_nueva_clase):
    if not (0 <= indice_nueva_clase < len(clases)):
        return False
    
    nuevo_horario = clases[indice_nueva_clase].horario
    
    for clase in clases:
        if miembro_id in clase.inscritos and clase.horario == nuevo_horario:
            return True
    return False


def verificar_inscripcion_existente(miembro_id, indice_clase):
    if 0 <= indice_clase < len(clases):
        return miembro_id in clases[indice_clase].inscritos
    return False


def inscribir_miembro_en_clase(miembro_id, indice_clase):
    if 0 <= indice_clase < len(clases):
        return clases[indice_clase].inscribir_miembro(miembro_id)
    return False


def desinscribir_miembro_de_clase(miembro_id, indice_clase):
    if 0 <= indice_clase < len(clases):
        return clases[indice_clase].desinscribir_miembro(miembro_id)
    return False


# ========== MENÚ PRINCIPAL ==========

def menu_clases():
    # Cargar clases de demostración automáticamente al entrar (sin mensajes)
    cargar_clases_demo_auto()
    
    while True:
        print("\n" + "="*50)
        print("           MÓDULO DE CLASES")
        print("="*50)
        print("1. Crear clase")
        print("2. Listar clases")
        print("3. Editar clase")
        print("4. Eliminar clase")
        print("5. Volver al menú principal")
        print("="*50)
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            crear_clase()
        elif opcion == "2":
            listar_clases()
        elif opcion == "3":
            editar_clase()
        elif opcion == "4":
            eliminar_clase()
        elif opcion == "5":
            print("\nVolviendo al menú principal...")
            break
        else:
            print("\n❌ Opción inválida")