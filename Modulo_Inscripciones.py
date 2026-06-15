
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

#MiembrosManager se utilizara para validar miembros durante inscripciones y cancelaciones
from Modulo_Miembros import MiembrosManager

class InscripcionesManager:
    ARCHIVO = "inscripciones.json"

    # El constructor ahora acepta un MiembrosManager
    def __init__(self, miembros_manager: MiembrosManager = None):
        self.miembros_manager = miembros_manager if miembros_manager else MiembrosManager()
        self.inscripciones = {}  # formato: {miembro_id: [clase_indices]}
        self.load()

    #validar que el miembro exista antes de cargar inscripciones
    def load(self):
        if not os.path.exists(self.ARCHIVO):
            self.inscripciones = {}
            self.save()
            return
        try:
            with open(self.ARCHIVO, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido:
                    self.inscripciones = {}
                    return
                data = json.loads(contenido)
                self.inscripciones = data.get("inscripciones", {})
                # Convertir claves a integers si es necesario
                self.inscripciones = {int(k): v for k, v in self.inscripciones.items()}
        except Exception as e:
            print(Color.RED + f"[Error] No se pudo cargar inscripciones: {e}" + Color.RESET)
            self.inscripciones = {}

    # Guardar inscripciones en formato JSON
    def save(self):
        try:
            with open(self.ARCHIVO, "w", encoding="utf-8") as f:
                json.dump({"inscripciones": self.inscripciones}, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(Color.RED + f"[Error] No se pudo guardar inscripciones: {e}" + Color.RESET)
            return False

    # Agregar miembro a través de MiembrosManager
    def mostrar_miembros(self):
        print(Color.CYAN + "\n========== MIEMBROS ==========" + Color.RESET)
        miembros = self.miembros_manager.listar_miembros()
        if not miembros:
            print(Color.YELLOW + "No hay miembros registrados" + Color.RESET)
            return
        for m in miembros:
            print(f"{m.id}. {m.nombre} ({m.email})")

    # Inscripcion
    def mostrar_inscripciones(self):
        print(Color.CYAN + "\n========== INSCRIPCIONES ==========" + Color.RESET)
        clases = obtener_todas_las_clases()
        miembros = self.miembros_manager.listar_miembros()
        
        # Validar que existan inscripciones antes de mostrar
        if not self.inscripciones:
            print(Color.YELLOW + "No hay inscripciones registradas" + Color.RESET)
            return
        
        # Mostrar inscripciones por miembro
        for miembro in miembros:
            clase_indices = self.inscripciones.get(miembro.id, [])
            print(Color.MAGENTA + f"\nMiembro: {miembro.nombre} (ID: {miembro.id})" + Color.RESET)
            if not clase_indices:
                print(Color.YELLOW + "Sin inscripciones registradas" + Color.RESET)
                continue
            for clase_idx in clase_indices:
                try:
                    c = clases[clase_idx]
                    horario = c.horario if not isinstance(c.horario, int) else f"{c.horario}:00"
                    print(f"✔ {c.nombre} ({horario}) | Entrenador: {c.entrenador}")
                except Exception:
                    print(Color.RED + f"[Advertencia] Clase index {clase_idx} no existe" + Color.RESET)

    # Inscribir miembro en clase con validaciones de existencia, cupo y choques horarios
    def inscribir(self, miembro_id, clase_idx):
        try:
            miembro_id = int(miembro_id)
            clase_idx = int(clase_idx)
            
            miembro = self.miembros_manager.obtener_miembro_por_id(miembro_id)
            if not miembro:
                raise ValueError(f"Miembro ID {miembro_id} no existe")
            
            clases = obtener_todas_las_clases()
            if clase_idx < 0 or clase_idx >= len(clases):
                raise IndexError("Clase no existe")

            # Ya inscrito?
            if miembro_id in self.inscripciones and clase_idx in self.inscripciones[miembro_id]:
                print(Color.YELLOW + "[Info] El miembro ya está inscrito en esta clase" + Color.RESET)
                return

            # Verificar cupo y choques usando Modulo_Clases helpers
            if not verificar_cupo_disponible(clase_idx):
                print(Color.RED + "[Error] No hay cupo disponible en la clase" + Color.RESET)
                return

            if verificar_choque_horario(miembro_id, clase_idx):
                print(Color.RED + "[Error] Choque de horario detectado" + Color.RESET)
                return

            # Inscribir en Modulo_Clases (persistira clases.json)
            resultado = inscribir_miembro_en_clase(miembro_id, clase_idx)
            if resultado:
                # Actualizar registro local
                if miembro_id not in self.inscripciones:
                    self.inscripciones[miembro_id] = []
                self.inscripciones[miembro_id].append(clase_idx)
                self.save()
                print(Color.GREEN + "[OK] Inscripción completada" + Color.RESET)
            else:
                print(Color.RED + "[Error] No se pudo inscribir en modulo de clases" + Color.RESET)

        except Exception as e:
            print(Color.RED + f"[Error] Inscripción fallida: {e}" + Color.RESET)

    # Revierte la inscripción de un miembro en una clase, con validaciones similares a inscribir() y actualización de ambos módulos
    def cancelar(self, miembro_id, clase_idx):
        try:
            miembro_id = int(miembro_id)
            clase_idx = int(clase_idx)
            
            miembro = self.miembros_manager.obtener_miembro_por_id(miembro_id)
            if not miembro:
                raise ValueError(f"Miembro ID {miembro_id} no existe")
            
            clases = obtener_todas_las_clases()
            if clase_idx < 0 or clase_idx >= len(clases):
                raise IndexError("Clase no existe")

            if miembro_id not in self.inscripciones or clase_idx not in self.inscripciones[miembro_id]:
                print(Color.YELLOW + "[Info] El miembro no figura inscrito en esa clase" + Color.RESET)
                return

            resultado = desinscribir_miembro_de_clase(miembro_id, clase_idx)
            if resultado:
                try:
                    self.inscripciones[miembro_id].remove(clase_idx)
                    if not self.inscripciones[miembro_id]:
                        del self.inscripciones[miembro_id]
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
            self.load() # Recargar inscripciones desde archivo al inicio del bucle
            print(Color.CYAN + "\n" + "+" + "=" * 58 + "+" + Color.RESET)
            print(Color.MAGENTA + Color.BOLD + "        MODULO DE INSCRIPCIONES" + Color.RESET)
            print(Color.CYAN + "+" + "=" * 58 + "+" + Color.RESET)
            print(Color.GREEN + "|" + Color.BOLD + " 1. Mostrar miembros".ljust(58) + Color.GREEN + "|" + Color.RESET)
            print(Color.GREEN + "|" + Color.BOLD + " 2. Mostrar clases disponibles".ljust(58) + Color.GREEN + "|" + Color.RESET)
            print(Color.GREEN + "|" + Color.BOLD + " 3. Inscribir miembro en clase".ljust(58) + Color.GREEN + "|" + Color.RESET)
            print(Color.GREEN + "|" + Color.BOLD + " 4. Cancelar inscripcion".ljust(58) + Color.GREEN + "|" + Color.RESET)
            print(Color.GREEN + "|" + Color.BOLD + " 5. Mostrar inscripciones".ljust(58) + Color.GREEN + "|" + Color.RESET)
            print(Color.YELLOW + "|" + Color.BOLD + " 6. Volver al menu principal".ljust(58) + Color.YELLOW + "|" + Color.RESET)
            print(Color.CYAN + "+" + "=" * 58 + "+" + Color.RESET)

            opcion = input(Color.CYAN + "\nSeleccione una opcion: " + Color.RESET).strip()
            if opcion == "1":
                self.mostrar_miembros()
            elif opcion == "2":
                mostrar_clases_disponibles()
            elif opcion == "3":
                try:
                    self.mostrar_miembros()
                    miembro_id = int(input(Color.CYAN + "ID del miembro: " + Color.RESET).strip())
                    mostrar_clases_disponibles()
                    clase_idx = int(input(Color.CYAN + "Indice de la clase: " + Color.RESET).strip())
                    self.inscribir(miembro_id, clase_idx)
                except ValueError:
                    print(Color.RED + "[Error] Entrada invalida" + Color.RESET)
            elif opcion == "4":
                try:
                    self.mostrar_miembros()
                    miembro_id = int(input(Color.CYAN + "ID del miembro: " + Color.RESET).strip())
                    clases = obtener_todas_las_clases()
                    inscritas = self.inscripciones.get(miembro_id, [])
                    if not inscritas:
                        print(Color.YELLOW + "[Info] El miembro no tiene inscripciones." + Color.RESET)
                        continue
                    print(Color.CYAN + "\nClases inscritas del miembro:" + Color.RESET)
                    for idx in inscritas:
                        try:
                            c = clases[idx]
                            horario = c.horario if not isinstance(c.horario, int) else f"{c.horario}:00"
                            print(f"{idx}. {c.nombre} ({horario}) | Entrenador: {c.entrenador}")
                        except Exception:
                            print(Color.RED + f"[Advertencia] Clase index {idx} no existe" + Color.RESET)
                    clase_idx = int(input(Color.CYAN + "Ingrese el índice (numero) de la clase a cancelar: " + Color.RESET).strip())
                    self.cancelar(miembro_id, clase_idx)
                except ValueError:
                    print(Color.RED + "[Error] Entrada invalida" + Color.RESET)
            elif opcion == "5":
                self.mostrar_inscripciones()
            elif opcion == "6":
                print(Color.YELLOW + "\nVolviendo al menu principal..." + Color.RESET)
                break
            else:
                print(Color.RED + "\n[Error] Opcion invalida" + Color.RESET)