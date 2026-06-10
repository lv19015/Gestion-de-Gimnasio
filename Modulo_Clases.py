# Modulo_Clases.py
# Modulo B: Gestion de Clases (CRUD completo)
# Autor: Franklin Omar Garcia Roman (GR20016)

import json
import os

ARCHIVO_CLASES = "clases.json"

# ==================== COLORES ANSI ====================
class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


# ==================== CLASE CLASE ====================
class Clase:
    def __init__(self, id, nombre, entrenador, horario, cupo_maximo, inscritos=None):
        self.id = id
        self.nombre = nombre
        self.entrenador = entrenador
        self.horario = horario
        self.cupo_maximo = cupo_maximo
        self.inscritos = inscritos if inscritos is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "entrenador": self.entrenador,
            "horario": self.horario,
            "cupo_maximo": self.cupo_maximo,
            "inscritos": self.inscritos
        }

    @staticmethod
    def from_dict(data):
        return Clase(
            data["id"],
            data["nombre"],
            data["entrenador"],
            data["horario"],
            data["cupo_maximo"],
            data["inscritos"]
        )

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


# ==================== PERSISTENCIA ====================
clases = []
contador_id = 1


def guardar_clases():
    try:
        with open(ARCHIVO_CLASES, 'w', encoding='utf-8') as f:
            json.dump([c.to_dict() for c in clases], f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"{Color.RED}[Error] No se pudo guardar: {e}{Color.RESET}")
        return False


def cargar_clases():
    global clases, contador_id
    if not os.path.exists(ARCHIVO_CLASES):
        return False
    try:
        with open(ARCHIVO_CLASES, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            clases = []
            max_id = 0
            for item in datos:
                nueva = Clase.from_dict(item)
                clases.append(nueva)
                if item["id"] > max_id:
                    max_id = item["id"]
            contador_id = max_id + 1
            return True
    except Exception as e:
        print(f"{Color.RED}[Error] No se pudo cargar: {e}{Color.RESET}")
        return False


# ==================== VALIDACIONES ====================
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


# ==================== CRUD ====================
def crear_clase():
    global contador_id
    print(Color.CYAN + "\n" + "=" * 40 + Color.RESET)
    print(Color.MAGENTA + "        CREAR NUEVA CLASE" + Color.RESET)
    print(Color.CYAN + "=" * 40 + Color.RESET)

    nombre = input("Nombre de la clase: ").strip()
    while not nombre:
        print(Color.RED + "[Error] El nombre no puede estar vacio" + Color.RESET)
        nombre = input("Nombre de la clase: ").strip()

    entrenador = input("Nombre del entrenador: ").strip()
    while not entrenador:
        print(Color.RED + "[Error] El nombre del entrenador no puede estar vacio" + Color.RESET)
        entrenador = input("Nombre del entrenador: ").strip()

    print(Color.YELLOW + "\nHorario - Opciones:" + Color.RESET)
    print("  - Numero entero (ej: 8 para 8:00 AM)")
    print("  - Formato HH:MM (ej: 14:30)")
    horario_input = input("Horario: ").strip()

    try:
        horario = int(horario_input)
    except ValueError:
        horario = horario_input

    while not validar_horario(horario):
        print(Color.RED + "[Error] Horario invalido" + Color.RESET)
        horario_input = input("Horario: ").strip()
        try:
            horario = int(horario_input)
        except ValueError:
            horario = horario_input

    cupo = int(input("Cupo maximo: "))
    while cupo <= 0:
        print(Color.RED + "[Error] El cupo debe ser mayor a 0" + Color.RESET)
        cupo = int(input("Cupo maximo: "))

    nueva_clase = Clase(contador_id, nombre, entrenador, horario, cupo)
    clases.append(nueva_clase)
    contador_id += 1

    if guardar_clases():
        print(Color.GREEN + f"\n[OK] Clase '{nombre}' creada con ID {nueva_clase.id}" + Color.RESET)
    else:
        print(Color.YELLOW + f"\n[Advertencia] Clase creada pero no se guardo en archivo" + Color.RESET)


def listar_clases():
    print(Color.CYAN + "\n" + "=" * 70 + Color.RESET)
    print(Color.MAGENTA + Color.BOLD + "                       LISTA DE CLASES" + Color.RESET)
    print(Color.CYAN + "=" * 70 + Color.RESET)

    if not clases:
        print(Color.YELLOW + "[Info] No hay clases registradas" + Color.RESET)
        return

    print(Color.MAGENTA + f"{'ID':<5} {'Nombre':<20} {'Entrenador':<18} {'Horario':<10} {'Cupo':<10}" + Color.RESET)
    print(Color.CYAN + "-" * 70 + Color.RESET)
    for c in clases:
        color_cupo = Color.GREEN if c.cupo_disponible() > 0 else Color.RED
        if isinstance(c.horario, int):
            horario_str = f"{c.horario}:00"
        else:
            horario_str = c.horario
        print(f"{c.id:<5} {c.nombre:<20} {c.entrenador:<18} {horario_str:<10} " + color_cupo + f"{len(c.inscritos)}/{c.cupo_maximo}" + Color.RESET)


def editar_clase():
    listar_clases()
    if not clases:
        return

    try:
        id_editar = int(input(Color.YELLOW + "\nID de la clase a editar: " + Color.RESET))
        clase = buscar_clase_por_id(id_editar)

        if not clase:
            print(Color.RED + "[Error] Clase no encontrada" + Color.RESET)
            return

        print(Color.CYAN + f"\n--- EDITANDO: {clase.nombre} ---" + Color.RESET)
        print(Color.YELLOW + "(Enter para mantener valor)" + Color.RESET)

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
                print(Color.RED + "[Error] Horario invalido, se mantiene el original" + Color.RESET)

        nuevo_cupo = input(f"Cupo maximo [{clase.cupo_maximo}]: ").strip()
        if nuevo_cupo:
            nuevo_cupo = int(nuevo_cupo)
            if nuevo_cupo > 0:
                if nuevo_cupo < len(clase.inscritos):
                    print(Color.YELLOW + f"[Advertencia] Hay {len(clase.inscritos)} inscritos. El nuevo cupo es menor." + Color.RESET)
                    if input("¿Continuar? (s/n): ").lower() != 's':
                        guardar_clases()
                        return
                clase.cupo_maximo = nuevo_cupo

        if guardar_clases():
            print(Color.GREEN + "[OK] Clase actualizada" + Color.RESET)
        else:
            print(Color.YELLOW + "[Advertencia] Clase actualizada pero no se guardo" + Color.RESET)

    except ValueError:
        print(Color.RED + "[Error] ID invalido" + Color.RESET)


def eliminar_clase():
    listar_clases()
    if not clases:
        return

    try:
        id_eliminar = int(input(Color.YELLOW + "\nID de la clase a eliminar: " + Color.RESET))
        clase = buscar_clase_por_id(id_eliminar)

        if not clase:
            print(Color.RED + "[Error] Clase no encontrada" + Color.RESET)
            return

        if clase.inscritos:
            print(Color.YELLOW + f"[Advertencia] La clase tiene {len(clase.inscritos)} miembros inscritos" + Color.RESET)
            if input("¿Eliminar de todas formas? (s/n): ").lower() != 's':
                print(Color.YELLOW + "[Info] Eliminacion cancelada" + Color.RESET)
                return

        clases.remove(clase)

        if guardar_clases():
            print(Color.GREEN + "[OK] Clase eliminada" + Color.RESET)
        else:
            print(Color.YELLOW + "[Advertencia] Clase eliminada pero no se guardo el cambio" + Color.RESET)

    except ValueError:
        print(Color.RED + "[Error] ID invalido" + Color.RESET)


# ==================== FUNCIONES DE COMPATIBILIDAD ====================
def mostrar_clases():
    print(Color.CYAN + "\n========== CLASES DISPONIBLES ==========" + Color.RESET)
    if not clases:
        print(Color.YELLOW + "No hay clases registradas" + Color.RESET)
        return

    for i, c in enumerate(clases):
        if isinstance(c.horario, int):
            horario_str = f"{c.horario} AM" if c.horario < 12 else f"{c.horario} PM"
        else:
            horario_str = c.horario
        color_cupo = Color.GREEN if c.cupo_disponible() > 0 else Color.RED
        print(f"{i}. {c.nombre} | Horario: {horario_str} | Cupos: {color_cupo}{len(c.inscritos)}/{c.cupo_maximo}{Color.RESET} | Entrenador: {c.entrenador}")


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
        resultado = clases[indice_clase].inscribir_miembro(miembro_id)
        if resultado:
            guardar_clases()
        return resultado
    return False


def desinscribir_miembro_de_clase(miembro_id, indice_clase):
    if 0 <= indice_clase < len(clases):
        resultado = clases[indice_clase].desinscribir_miembro(miembro_id)
        if resultado:
            guardar_clases()
        return resultado
    return False


# ==================== CLASES DE DEMOSTRACION ====================
def cargar_clases_demo():
    global contador_id
    if len(clases) == 0:
        clases_demo = [
            {"nombre": "Yoga", "entrenador": "Maria", "horario": 8, "cupo_maximo": 5},
            {"nombre": "Spinning", "entrenador": "Carlos", "horario": 8, "cupo_maximo": 1},
            {"nombre": "Crossfit", "entrenador": "Ana", "horario": 10, "cupo_maximo": 3},
            {"nombre": "Pilates", "entrenador": "Laura", "horario": 9, "cupo_maximo": 4},
            {"nombre": "Zumba", "entrenador": "Javier", "horario": "18:30", "cupo_maximo": 6},
            {"nombre": "Boxeo", "entrenador": "Roberto", "horario": 19, "cupo_maximo": 2},
            {"nombre": "Natacion", "entrenador": "Patricia", "horario": 7, "cupo_maximo": 8},
            {"nombre": "Funcional", "entrenador": "Luis", "horario": "17:00", "cupo_maximo": 5}
        ]
        for demo in clases_demo:
            nueva_clase = Clase(contador_id, demo["nombre"], demo["entrenador"], demo["horario"], demo["cupo_maximo"])
            clases.append(nueva_clase)
            contador_id += 1
        guardar_clases()
        print(Color.GREEN + "[Info] Clases de demostracion cargadas" + Color.RESET)


# ==================== MENU PRINCIPAL ====================
def menu_clases():
    cargar_clases()
    if len(clases) == 0:
        print(Color.YELLOW + "\n[Info] No hay clases guardadas. Cargando clases de demostracion..." + Color.RESET)
        cargar_clases_demo()

    while True:
        print(Color.CYAN + "\n" + "=" * 50 + Color.RESET)
        print(Color.MAGENTA + Color.BOLD + "           MODULO DE CLASES" + Color.RESET)
        print(Color.CYAN + "=" * 50 + Color.RESET)
        print(Color.GREEN + "1. Crear clase" + Color.RESET)
        print(Color.GREEN + "2. Lista de clases" + Color.RESET)
        print(Color.GREEN + "3. Editar clase" + Color.RESET)
        print(Color.GREEN + "4. Eliminar clase" + Color.RESET)
        print(Color.YELLOW + "5. Volver al menu principal" + Color.RESET)
        print(Color.CYAN + "=" * 50 + Color.RESET)

        opcion = input(Color.CYAN + "\nSeleccione una opcion: " + Color.RESET)

        if opcion == "1":
            crear_clase()
        elif opcion == "2":
            listar_clases()
        elif opcion == "3":
            editar_clase()
        elif opcion == "4":
            eliminar_clase()
        elif opcion == "5":
            print(Color.YELLOW + "\nVolviendo al menu principal..." + Color.RESET)
            break
        else:
            print(Color.RED + "\n[Error] Opcion invalida" + Color.RESET)


if __name__ == "__main__":
    menu_clases()