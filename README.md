# Sistema de Gestión de un Gimnasio

Proyecto de ciclo para **Lógica de Programación** - Entrega Final
Ingenieria en Desarrollo de Software
Universidad de El Salvador, Facultad Multidisciplinaria de Occidente

---

## Descripción del Proyecto

Aplicación de línea de comandos (CLI) en Python para gestionar el funcionamiento básico de un gimnasio: miembros, clases impartidas por entrenadores e inscripciones de miembros a esas clases. El sistema valida cupos máximos y evita choques de horario al inscribir a un miembro.

## Objetivo

Aplicar los conceptos de clases, manejo de archivos (persistencia en JSON), manejo de errores con `try/except` y pruebas unitarias, desarrollando una aplicación CLI funcional e integrada.

## Integrantes

| Nombre                         | Carnet  |
| ------------------------------ | ------- |
| Kevin Daniel Hernández Belloso | HH25003 |
| Brenda Ivania Laínez Vides     | LV19015 |
| Franklin Omar García Román     | GR20016 |

## Lógica de Negocio

- Los entrenadores imparten **clases**, cada una con `horario`, `entrenador` y `cupo_maximo`.
- Los **miembros** se registran en el sistema y pueden inscribirse en clases.
- Cada clase tiene un **cupo máximo** de inscritos que no puede excederse.
- No se permite inscribir a un miembro en una clase si:
  - La clase ya alcanzó su cupo máximo.
  - El miembro ya está inscrito en esa misma clase (se evita duplicados).
  - El miembro ya está inscrito en otra clase con el mismo horario (choque de horario).
- Un miembro puede **cancelar** su inscripción a una clase en cualquier momento.
- El sistema usa **validaciones con try/except** para todas las operaciones.

## Estructura del Proyecto

```
Gestion-de-Gimnasio/
├── main.py                      # Punto de entrada: menú principal del sistema
├── Modulo_Miembros.py           # CRUD de miembros (clase Miembro, MiembrosManager)
├── Modulo_Clases.py             # CRUD de clases (clase Clase, funciones CRUD)
├── Modulo_Inscripciones.py      # Inscripciones: conecta miembros y clases
├── miembros.json                # Persistencia de miembros (generado automáticamente)
├── clases.json                  # Persistencia de clases, incluye IDs de inscritos
├── inscripciones.json           # Persistencia de inscripciones (generado automáticamente)
├── tests/                       # Pruebas unitarias (unittest)
│   ├── test_clases.py
│   ├── test_miembros.py
│   └── test_inscripciones.py
└── README.md
```

## Requisitos

- Python 3.10 o superior
- No requiere librerías externas; solo usa la librería estándar (`json`, `os`, `datetime`, `unittest`).

## Cómo ejecutar el programa

Desde la carpeta del proyecto:

```bash
python main.py
```

Se mostrará el menú principal con colores ANSI:

```
############################################################
  GESTION DE GIMNASIO - SISTEMA PRINCIPAL
############################################################

+==========================================================+
| 1. Gestionar clases                                       |
| 2. Gestionar miembros                                     |
| 3. Gestionar inscripciones                                |
| 4. Salir                                                  |
+==========================================================+

Seleccione una opcion:
```

Cada opción abre el submenú del módulo correspondiente, desde donde se pueden crear, listar, editar y eliminar registros.

## Persistencia de Datos

Los datos se guardan automáticamente en archivos JSON ubicados en la raíz del proyecto:

- **miembros.json**: lista de miembros con campos `id`, `nombre`, `email`, `telefono`, `fecha_registro`.
- **clases.json**: lista de clases con campos `id`, `nombre`, `entrenador`, `horario`, `cupo_maximo`, `inscritos` (lista de IDs de miembros inscritos).
- **inscripciones.json**: registro de inscripciones en formato `{miembro_id: [indices_de_clases]}` para rastreabilidad.

Los tres módulos funcionan de forma sincronizada:

- **Modulo_Miembros**: CRUD de miembros, persistencia en `miembros.json`.
- **Modulo_Clases**: CRUD de clases, persistencia en `clases.json` (incluye lista de inscritos).
- **Modulo_Inscripciones**: gestiona inscripciones, lee de ambos módulos y mantiene `inscripciones.json`.

**Nota**: Las clases se seleccionan usando su **índice** (posición en la lista, comenzando en 0), no por su ID.

## Ejemplo de Uso

1. **Crear una clase** desde el menú "1. Gestionar clases", indicando nombre, entrenador, horario (número 1-24 o formato HH:MM) y cupo máximo. Se guarda automáticamente en `clases.json`.
2. **Crear un miembro** desde el menú "2. Gestionar miembros" (nombre, email, teléfono). Se guarda en `miembros.json`.
3. **Inscribir el miembro** desde el menú "3. Gestionar inscripciones": seleccionar el ID del miembro y el **índice** de la clase (mostrado en la lista de clases). El sistema valida cupo disponible y evita duplicados.
4. **Cancelar inscripciones** desde la opción 4 del menú de inscripciones: el sistema muestra las clases inscritas del miembro con sus índices para que selecciones cuál cancelar.
5. **Consultar inscripciones** desde la opción 5 para ver todas las inscripciones activas del sistema.

## Pruebas Unitarias

Cada integrante agregó al menos una prueba unitaria para su módulo. Para ejecutar todas las pruebas:

```bash
python -m unittest discover -s tests
```

O de forma individual, por ejemplo:

```bash
python -m unittest tests.test_inscripciones
```

## Tecnologías Utilizadas

- Python (CLI)
- JSON para persistencia de datos
- `unittest` para pruebas
- PSeInt (usado en etapas iniciales para diseño en pseudocódigo)
- GitHub (control de versiones)
