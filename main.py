# importaciones de módulos
import Modulo_Inscripciones as inscripcion

# MAIN.PY: Punto de entrada del sistema de gestión de gimnasio.
while True:
    print("\n========== SISTEMA DE GESTION DEL GIMNASIO ==========")
    print("1. Módulo Miembros")
    print("2. Módulo Clases")
    print("3. Módulo Inscripciones")
    print("4. Salir")

    opcion_principal = input("\nSeleccione una opción: ")

    # MÓDULO MIEMBROS
    if opcion_principal == "1":

        print("\n[MÓDULO MIEMBROS]")
        print("CRUD en desarrollo...")

    # MÓDULO CLASES
    elif opcion_principal == "2":
        print("\n[MÓDULO CLASES]")
        print("CRUD en desarrollo...")

    # MÓDULO INSCRIPCIONES
    elif opcion_principal == "3":
        while True:
            print("\n===== MÓDULO INSCRIPCIONES =====")
            print("1. Inscribir miembro")
            print("2. Cancelar inscripción")
            print("3. Ver inscripciones")
            print("4. Volver al menú principal")

            opcion_inscripcion = input( "\nSeleccione una opción: " )

            # INSCRIBIR MIEMBRO
            if opcion_inscripcion == "1":

                print("\n--- MIEMBROS DISPONIBLES ---")
                inscripcion.mostrar_miembros()
                indice_miembro = int(input("\nSeleccione miembro: "))

                print("\n--- CLASES DISPONIBLES ---")
                inscripcion.mostrar_clases()
                indice_clase = int( input("\nSeleccione clase: "))
                inscripcion.inscribir_miembro( indice_miembro, indice_clase)

            # CANCELAR INSCRIPCIÓN
            elif opcion_inscripcion == "2":

                print("\n--- MIEMBROS DISPONIBLES ---")
                inscripcion.mostrar_miembros()

                indice_miembro = int( input("\nSeleccione miembro: "))
                print("\n--- CLASES DISPONIBLES ---")
                inscripcion.mostrar_clases()
                indice_clase = int(input("\nSeleccione clase: "))
                inscripcion.cancelar_inscripcion( indice_miembro, indice_clase)

            # VER INSCRIPCIONES
            elif opcion_inscripcion == "3":
                inscripcion.mostrar_inscripciones()

            elif opcion_inscripcion == "4":
                break # Volver al menú principal
            else:
                print("\nERROR: Opción inválida")

    # SALIR: Termina de ejecutarse el programa
    elif opcion_principal == "4":
        print("\nSaliendo del sistema...")
        break
    else:
        print("\nERROR: Opción inválida")