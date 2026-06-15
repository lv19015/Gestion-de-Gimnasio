# MAIN.PY: Punto de entrada del sistema de gestión de gimnasio.

import os
from Modulo_Clases import cargar_clases, menu_clases, Color
from Modulo_Inscripciones import InscripcionesManager


def imprimir_titulo():
    print(Color.MAGENTA + Color.BOLD + "\n" + "#" * 60 + Color.RESET)
    print(Color.CYAN + Color.BOLD + "  GESTION DE GIMNASIO - SISTEMA PRINCIPAL" + Color.RESET)
    print(Color.MAGENTA + Color.BOLD + "#" * 60 + Color.RESET)


def imprimir_menu_principal():
    print(Color.CYAN + "\n" + "+" + "=" * 58 + "+" + Color.RESET)
    print(Color.GREEN + "|" + Color.BOLD + " 1. Gestionar clases".ljust(58) + Color.GREEN + "|" + Color.RESET)
    print(Color.GREEN + "|" + Color.BOLD + " 2. Gestionar inscripciones".ljust(58) + Color.GREEN + "|" + Color.RESET)
    print(Color.GREEN + "|" + Color.BOLD + " 3. Salir".ljust(58) + Color.GREEN + "|" + Color.RESET)
    print(Color.CYAN + "+" + "=" * 58 + "+" + Color.RESET)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    if not cargar_clases():
        print(Color.YELLOW + "[Info] No se encontro archivo clases.json o no se pudo cargar." + Color.RESET)
        print(Color.YELLOW + "[Info] El modulo de clases se encargara de generar datos de demostracion si es necesario." + Color.RESET)
    inscripciones_mgr = InscripcionesManager()

    while True:
        imprimir_titulo()
        imprimir_menu_principal()
        opcion = input(Color.CYAN + "\nSeleccione una opcion: " + Color.RESET).strip()

        if opcion == "1":
            menu_clases()
        elif opcion == "2":
            inscripciones_mgr.menu()
        elif opcion == "3":
            print(Color.GREEN + "\nGracias por usar el sistema. Hasta luego!" + Color.RESET)
            break
        else:
            print(Color.RED + "\n[Error] Opcion invalida. Intente de nuevo." + Color.RESET)


if __name__ == "__main__":
    main()
