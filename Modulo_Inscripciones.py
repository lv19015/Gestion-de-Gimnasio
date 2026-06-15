
# Módulo de Inscripciones - Clase orientada a objetos con persistencia JSON
import json
import os
from Modulo_Clases import (
    mostrar_clases as mostrar_clases_disponibles,
    obtener_todas_las_clases,
    verificar_cupo_disponible,
    verificar_choque_horario,
    verificar_inscripcion_existente,
    inscribir_miembro_en_clase,
    desinscribir_miembro_de_clase,
    Color,
)

DEFAULT_MIEMBROS = [
    {"nombre": "Kevin Hernandez", "inscritos": []},
    {"nombre": "Franklin Garcia", "inscritos": []},
]


class InscripcionesManager:
    ARCHIVO = "inscripciones.json"

    def __init__(self):
        self.miembros = []  # lista de dicts: {"nombre": str, "inscritos": [indices_clase]}
        self.load()

    def load(self):
        if not os.path.exists(self.ARCHIVO):
            self.miembros = DEFAULT_MIEMBROS.copy()
            self.save()
            return
        try:
            with open(self.ARCHIVO, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.miembros = data.get("miembros", DEFAULT_MIEMBROS.copy())
        except Exception as e:
            print(Color.RED + f"[Error] No se pudo cargar inscripciones: {e}" + Color.RESET)
            self.miembros = DEFAULT_MIEMBROS.copy()

    def save(self):
        try:
            with open(self.ARCHIVO, "w", encoding="utf-8") as f:
                json.dump({"miembros": self.miembros}, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(Color.RED + f"[Error] No se pudo guardar inscripciones: {e}" + Color.RESET)
            return False

    # Miembros
    def agregar_miembro(self, nombre):
        try:
            nombre = str(nombre).strip()
            if not nombre:
                raise ValueError("Nombre vacio")
            self.miembros.append({"nombre": nombre, "inscritos": []})
            self.save()
            print(Color.GREEN + "[OK] Miembro agregado" + Color.RESET)
        except Exception as e:
            print(Color.RED + f"[Error] No se pudo agregar miembro: {e}" + Color.RESET)

    def mostrar_miembros(self):
        print(Color.CYAN + "\n========== MIEMBROS ==========" + Color.RESET)
        if not self.miembros:
            print(Color.YELLOW + "No hay miembros registrados" + Color.RESET)
            return
        for idx, m in enumerate(self.miembros):
            print(f"{idx}. {m.get('nombre')}")

    # Inscripciones
    def mostrar_inscripciones(self):
        print(Color.CYAN + "\n========== INSCRIPCIONES ==========" + Color.RESET)
        clases = obtener_todas_las_clases()
        for idx, m in enumerate(self.miembros):
            print(Color.MAGENTA + f"\nMiembro: {m.get('nombre')} (id: {idx})" + Color.RESET)
            if not m.get("inscritos"):
                print(Color.YELLOW + "Sin inscripciones registradas" + Color.RESET)
                continue
            for clase_idx in m.get("inscritos", []):
                try:
                    c = clases[clase_idx]
                    horario = c.horario if not isinstance(c.horario, int) else f"{c.horario}:00"
                    print(f"✔ {c.nombre} ({horario}) | Entrenador: {c.entrenador}")
                except Exception:
                    print(Color.RED + f"[Advertencia] Clase index {clase_idx} no existe" + Color.RESET)

    def inscribir(self, miembro_idx, clase_idx):
        try:
            miembro_idx = int(miembro_idx)
            clase_idx = int(clase_idx)
            if miembro_idx < 0 or miembro_idx >= len(self.miembros):
                raise IndexError("Miembro no existe")
            clases = obtener_todas_las_clases()
            if clase_idx < 0 or clase_idx >= len(clases):
                raise IndexError("Clase no existe")

            # Ya inscrito en nuestro registro?
            if clase_idx in self.miembros[miembro_idx]["inscritos"]:
                print(Color.YELLOW + "[Info] El miembro ya figura inscrito localmente" + Color.RESET)
                return

            # Verificar cupo y choques usando Modulo_Clases helpers
            if not verificar_cupo_disponible(clase_idx):
                print(Color.RED + "[Error] No hay cupo disponible en la clase" + Color.RESET)
                return

            miembro_id_para_clases = miembro_idx  # usamos el indice como id
            if verificar_choque_horario(miembro_id_para_clases, clase_idx):
                print(Color.RED + "[Error] Choque de horario detectado (segun registro de clases)" + Color.RESET)
                return

            # Inscribir en Modulo_Clases (persistira clases.json)
            resultado = inscribir_miembro_en_clase(miembro_id_para_clases, clase_idx)
            if resultado:
                # Actualizar registro local
                self.miembros[miembro_idx]["inscritos"].append(clase_idx)
                self.save()
                print(Color.GREEN + "[OK] Inscripción completada" + Color.RESET)
            else:
                print(Color.RED + "[Error] No se pudo inscribir en modulo de clases" + Color.RESET)

        except Exception as e:
            print(Color.RED + f"[Error] Inscripción fallida: {e}" + Color.RESET)

    def cancelar(self, miembro_idx, clase_idx):
        try:
            miembro_idx = int(miembro_idx)
            clase_idx = int(clase_idx)
            if miembro_idx < 0 or miembro_idx >= len(self.miembros):
                raise IndexError("Miembro no existe")
            clases = obtener_todas_las_clases()
            if clase_idx < 0 or clase_idx >= len(clases):
                raise IndexError("Clase no existe")

            if clase_idx not in self.miembros[miembro_idx]["inscritos"]:
                print(Color.YELLOW + "[Info] El miembro no figura inscrito localmente en esa clase" + Color.RESET)
                return

            miembro_id_para_clases = miembro_idx
            resultado = desinscribir_miembro_de_clase(miembro_id_para_clases, clase_idx)
            if resultado:
                try:
                    self.miembros[miembro_idx]["inscritos"].remove(clase_idx)
                except ValueError:
                    pass
                self.save()
                print(Color.GREEN + "[OK] Inscripción cancelada" + Color.RESET)
            else:
                print(Color.RED + "[Error] No se pudo cancelar en modulo de clases" + Color.RESET)

        except Exception as e:
            print(Color.RED + f"[Error] Cancelación fallida: {e}" + Color.RESET)

    # Menu interactivo
    def menu(self):
        while True:
            print(Color.CYAN + "\n" + "=" * 50 + Color.RESET)
            print(Color.MAGENTA + Color.BOLD + "        MODULO DE INSCRIPCIONES" + Color.RESET)
            print(Color.CYAN + "=" * 50 + Color.RESET)
            print(Color.GREEN + "1. Mostrar miembros" + Color.RESET)
            print(Color.GREEN + "2. Agregar miembro" + Color.RESET)
            print(Color.GREEN + "3. Mostrar clases disponibles" + Color.RESET)
            print(Color.GREEN + "4. Inscribir miembro en clase" + Color.RESET)
            print(Color.GREEN + "5. Cancelar inscripcion" + Color.RESET)
            print(Color.GREEN + "6. Mostrar inscripciones" + Color.RESET)
            print(Color.YELLOW + "7. Volver al menu principal" + Color.RESET)
            print(Color.CYAN + "=" * 50 + Color.RESET)

            opcion = input(Color.CYAN + "\nSeleccione una opcion: " + Color.RESET).strip()
            if opcion == "1":
                self.mostrar_miembros()
            elif opcion == "2":
                nombre = input("Nombre completo del miembro: ").strip()
                self.agregar_miembro(nombre)
            elif opcion == "3":
                mostrar_clases_disponibles()
            elif opcion == "4":
                try:
                    self.mostrar_miembros()
                    miembro = int(input("ID miembro: ").strip())
                    mostrar_clases_disponibles()
                    clase = int(input("Indice clase: ").strip())
                    self.inscribir(miembro, clase)
                except ValueError:
                    print(Color.RED + "[Error] Entrada invalida" + Color.RESET)
            elif opcion == "5":
                try:
                    self.mostrar_miembros()
                    miembro = int(input("ID miembro: ").strip())
                    self.mostrar_inscripciones()
                    clase = int(input("Indice clase a cancelar: ").strip())
                    self.cancelar(miembro, clase)
                except ValueError:
                    print(Color.RED + "[Error] Entrada invalida" + Color.RESET)
            elif opcion == "6":
                self.mostrar_inscripciones()
            elif opcion == "7":
                print(Color.YELLOW + "\nVolviendo al menu principal..." + Color.RESET)
                break
            else:
                print(Color.RED + "\n[Error] Opcion invalida" + Color.RESET)