Algoritmo GestionDeGimnasio_Clases
	// Dimensiones (total) para las clases (capacidad para 10 clases) \\
	Dimension nombresClases[10]
	Dimension entrenadores[10]
	Dimension horarios[10] // (hora como entero para las 10 = 10:00) \\
	Dimension cuposMaximos[10]
	Dimension cuposActuales[10]
	
	Definir nombresClases, entrenadores Como Cadena
	Definir horarios, cuposMaximos, cuposActuales, totalClases, i Como Entero
	
	//  2 CLASES PARA PRUEBAS \\
	totalClases <- 2
	
	nombresClases[1] <- "Yoga"
	entrenadores[1] <- "Brenda "
	horarios[1] <- 8 // 8:00 AM \\
	cuposMaximos[1] <- 15
	cuposActuales[1] <- 0
	
	nombresClases[2] <- "Crossfit"
	entrenadores[2] <- "Franklin"
	horarios[2] <- 10 // 10:00 AM \\
	cuposMaximos[2] <- 10
	cuposActuales[2] <- 0
	
	// MENÚ DE GESTIÓN DE CLASES \\
	Definir opcion Como Entero
	Repetir
		Escribir ""
		Escribir "--- GESTIÓN DE CLASES ---"
		Escribir "1. Mostrar clases disponibles"
		Escribir "2. Crear nueva clase"
		Escribir "3. Salir"
		Leer opcion
		
		Segun opcion Hacer
			1:
				Escribir "LISTA DE CLASES:"
				Escribir "ID | Nombre | Entrenador | Horario | Cupo"
				Para i <- 1 Hasta totalClases Hacer
					Escribir i, " | ", nombresClases[i], " | ", entrenadores[i], " | ", horarios[i], ":00 | ", cuposActuales[i], "/", cuposMaximos[i]
				FinPara
			2:
				Si totalClases < 10 Entonces
					totalClases <- totalClases + 1
					Escribir "Ingrese nombre de la clase:"
					Leer nombresClases[totalClases]
					Escribir "Ingrese nombre del entrenador:"
					Leer entrenadores[totalClases]
					Escribir "Ingrese hora (formato 24h, ej: 14):"
					Leer horarios[totalClases]
					Escribir "Ingrese cupo máximo:"
					Leer cuposMaximos[totalClases]
					cuposActuales[totalClases] <- 0
					Escribir "¡Clase creada con éxito!"
				Sino
					Escribir "Error: No hay espacio para más clases."
				FinSi
			3:
				Escribir "Saliendo del módulo de clases..."
			De Otro Modo:
				Escribir "Opción no válida."
		FinSegun
	Hasta Que opcion = 3
	
FinAlgoritmo
