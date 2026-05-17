
# Módulo de Inscripciones - Sistema de Gestión de Gimnasioz
# Responsabilidades:
# - Gestionar inscripciones de miembros en clases.
# - Validar cupos máximos.
# - Validar choques de horario.
# - Permitir cancelaciones de inscripciones.
# - Mostrar información de miembros, clases e inscripciones.

# DATOS DE EJEMPLO PARA FINES DE DEMOSTRACIÓN
miembros = [
    "Kevin Hernandez",
    "Franklin Garcia"
]

clases = [
    {
        "nombre": "Yoga",
        "horario": 8,
        "cupo_max": 5,
        "inscritos": 0
    },
    {
        "nombre": "Spinning",
        "horario": 8,
        "cupo_max": 1,
        "inscritos": 0
    },
    {
        "nombre": "Crossfit",
        "horario": 10,
        "cupo_max": 3,
        "inscritos": 0
    }
]

# Matriz de inscripciones
# Filas = miembros
# Columnas = clases
inscripciones = [
    [False for _ in clases]
    for _ in miembros
]

# FUNCIONES DE CONSULTA (READ)

# Muestra todos los miembros registrados.
def mostrar_miembros():
    
    print("\n========== MIEMBROS ==========")
    for indice_miembro, nombre_miembro in enumerate(miembros):
        print(f"{indice_miembro}. {nombre_miembro}")

# Muestra todas las clases disponibles, incluyendo horario y cupos.
def mostrar_clases():
    print("\n========== CLASES ==========")
    for indice_clase, clase_obj in enumerate(clases):

        print(
            f"{indice_clase}. "
            f"{clase_obj['nombre']} | "
            f"Horario: {clase_obj['horario']} AM | "
            f"Cupos: "
            f"{clase_obj['inscritos']}/"
            f"{clase_obj['cupo_max']}"
        )


#  Muestra las clases en las que está inscrito cada miembro.
def mostrar_inscripciones():
    print("\n========== INSCRIPCIONES ==========")
    for indice_miembro, nombre_miembro in enumerate(miembros):

        print(f"\nMiembro: {nombre_miembro}")
        tiene_inscripciones = False
        for indice_clase, clase_obj in enumerate(clases):

            if inscripciones[indice_miembro][indice_clase]:
                print(
                    f"✔ {clase_obj['nombre']} "
                    f"({clase_obj['horario']} AM)"
                )
                tiene_inscripciones = True

        if not tiene_inscripciones:
            print("Sin inscripciones registradas")

# VALIDACIONES DEL SISTEMA
def validar_cupo(indice_clase):

    # Verifica si la clase aún tiene cupo disponible.
    # Retorna:
    #     True -> Hay cupo
    #     False -> Clase llena
    return (
        clases[indice_clase]["inscritos"] < clases[indice_clase]["cupo_max"]
    )


def validar_choque_horario( indice_miembro, indice_clase ):
    # Verifica si el miembro ya está inscrito en otra clase con el mismo horario.
    # Retorna: True si existe choque de horario o False si No hay conflicto
    horario_nueva_clase = (
        clases[indice_clase]["horario"]
    )

    for indice_clase_actual, clase_obj in enumerate(clases):
        if ( inscripciones[indice_miembro] [indice_clase_actual]):
            if (clase_obj["horario"] == horario_nueva_clase):
                return True
    return False


def validar_inscripcion_existente( indice_miembro, indice_clase ):
    # Verifica si el miembro ya está inscrito en la clase.
    return inscripciones[indice_miembro][indice_clase]


# FUNCIONALIDAD DE CREACION (CREATE)
def inscribir_miembro( indice_miembro, indice_clase):

    if validar_inscripcion_existente( indice_miembro, indice_clase):
        print( "\nERROR: El miembro ya está inscrito en esta clase" )
        return

    if not validar_cupo(indice_clase):
        print( "\nERROR: No hay cupo disponible")
        return

    if validar_choque_horario( indice_miembro, indice_clase):
        print("\nERROR: Choque de horario detectado")
        return

    inscripciones[indice_miembro][indice_clase] = True

    clases[indice_clase]["inscritos"] += 1

    print( "\nInscripción realizada correctamente :)" )

# DELETE
def cancelar_inscripcion(indice_miembro,indice_clase):

    if not inscripciones[indice_miembro][indice_clase]:
        print("\n! El miembro no está inscrito en esta clase")
        return

    inscripciones[indice_miembro][indice_clase] = False

    clases[indice_clase]["inscritos"] -= 1

    print( "\n Inscripción cancelada correctamente" )

# UPDATE
def actualizar_inscripcion(indice_miembro, clase_actual, nueva_clase):

    if not inscripciones[indice_miembro][clase_actual]:
        print("\n ERROR: El miembro no está inscrito en la clase actual")
        return

    cancelar_inscripcion(indice_miembro,clase_actual)
    inscribir_miembro( indice_miembro, nueva_clase)
