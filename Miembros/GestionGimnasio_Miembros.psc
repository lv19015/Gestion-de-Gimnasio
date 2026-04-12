Algoritmo GestionGimnasio_Miembros
	
	Definir opcion Como Entero
	Definir nombres, apellidos, membresias Como Caracter
	Definir totalMiembros Como Entero
	Dimension nombres[50], apellidos[50], membresias[50]
	
	Definir idMiembro Como Entero
	idMiembro <- 1
	totalMiembros <- 0
	
	totalMiembros <- totalMiembros + 1
	nombres[totalMiembros] <- "Kevin Daniel"
	apellidos[totalMiembros] <- "Hernandez Belloso"
	membresias[totalMiembros] <- "Premium Anual"
	
	totalMiembros <- totalMiembros + 1
	nombres[totalMiembros] <- "Brenda Ivania"
	apellidos[totalMiembros] <- "Lainez Vides"
	membresias[totalMiembros] <- "Mensual Basica"
	
	Repetir
		Limpiar Pantalla
		Escribir "=========================================="
		Escribir "     SISTEMA DE GESTION DE GIMNASIO       "
		Escribir "       MODULO: GESTION DE MIEMBROS        "
		Escribir "=========================================="
		Escribir "1. Registrar Nuevo Miembro"
		Escribir "2. Mostrar Lista de Miembros"
		Escribir "3. Salir (Fin de Demo)"
		Escribir "=========================================="
		Escribir "Seleccione una opcion: "
		Leer opcion
		
		Segun opcion Hacer
			1:
				Limpiar Pantalla
				Escribir ">> REGISTRO DE NUEVO MIEMBRO <<"
				Escribir ""
				
				Si totalMiembros < 50 Entonces
					totalMiembros <- totalMiembros + 1
					Escribir "Ingrese el Nombre del Miembro: "
					Leer nombres[totalMiembros]
					Escribir "Ingrese el Apellido del Miembro: "
					Leer apellidos[totalMiembros]
					Escribir "Ingrese el Tipo de Membresia (Ej: Basica, Premium): "
					Leer membresias[totalMiembros]
					
					Escribir ""
					Escribir "*** Miembro Registrado Exitosamente! ***"
					Escribir "ID Interno Asignado: ", totalMiembros
				Sino
					Escribir "ERROR: Capacidad maxima de miembros alcanzada (Demo)."
				FinSi
				Escribir ""
				Escribir "Presione ENTER para continuar..."
				Esperar Tecla
				
			2:
				Limpiar Pantalla
				Escribir ">> LISTADO GENERAL DE MIEMBROS <<"
				Escribir ""
				
				Si totalMiembros = 0 Entonces
					Escribir "No hay miembros registrados en el sistema."
				Sino
					Escribir "Total Miembros Registrados: ", totalMiembros
					Escribir "---------------------------------------------"
					Para i<-1 Hasta totalMiembros Con Paso 1 Hacer
						Escribir "ID: ", i
						Escribir "  Nombre   : ", nombres[i], " ", apellidos[i]
						Escribir "  Membresia: ", membresias[i]
						Escribir "---------------------------------------------"
					FinPara
				FinSi
				Escribir ""
				Escribir "Presione ENTER para continuar..."
				Esperar Tecla
				
			3:
				Escribir "Saliendo del modulo de Miembros..."
				Esperar 1 Segundos
				
			De Otro Modo:
				Escribir "Opcion no valida. Intente de nuevo."
				Esperar 2 Segundos
		Fin Segun
		
	Hasta Que opcion = 3
	
FinAlgoritmo