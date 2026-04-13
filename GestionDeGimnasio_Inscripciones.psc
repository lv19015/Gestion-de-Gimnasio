Algoritmo GestionDeGimnasio_Inscripciones
	
    // VARIABLES
    Definir opcion, i, j Como Entero
    Definir miembro, clase Como Entero
    Definir choque_horario Como Logico
	
    // Miembros
    Definir nombresMiembros Como Caracter
    Dimension miembros[10] //lista de miembros
	
    // Detalles de las Clases
    Definir nombreClase Como Caracter
    Definir horarioClase Como Entero
    Definir cupoMax Como Entero
    Definir inscritos Como Entero
	
    Dimension nombreClase[10]
    Dimension horarioClase[10]
    Dimension cupoMax[10]
    Dimension inscritos[10]
	
    // Matriz de Inscripciones, filas de miembros y columnas de clases
    Definir inscripciones Como Entero
    Dimension inscripciones[10,10]
	
    // DATOS PREDEFINIDOS PARA PRUEBAS
    // Miembros
    miembros[1] <- "Kevin Hernandez"
    miembros[2] <- "Franklin Garcia"
	
    // Clases
    nombreClase[1] <- "Yoga"
    horarioClase[1] <- 8
    cupoMax[1] <- 5
    inscritos[1] <- 0
    nombreClase[2] <- "Spinning"
    horarioClase[2] <- 8
    cupoMax[2] <- 1
    inscritos[2] <- 0
	
    // Inicializar inscripciones 
    Para i <- 1 Hasta 10 Hacer
        Para j <- 1 Hasta 10 Hacer
            inscripciones[i,j] <- 0 //0 indica que el miembro no esta inscrito en una clase
        FinPara
    FinPara
	
    // MENU
    Repetir
        Escribir "------ Sistema de Gestion de Gimnasio ------"
        Escribir "1. Mostrar miembros"
        Escribir "2. Mostrar clases"
        Escribir "3. Inscribir miembro en clase"
        Escribir "4. Salir"
        Leer opcion
		
        Segun opcion Hacer
            1:
                Escribir "---- LISTA DE MIEMBROS ----"
                Para i <- 1 Hasta 2 Hacer
                    Escribir i, "- ", miembros[i]
                FinPara
				Escribir " "
            2:
                Escribir "---- LISTA DE CLASES ----"
                Para i <- 1 Hasta 2 Hacer
                    Escribir i, ". ", nombreClase[i], " - Hora: ", horarioClase[i], " AM, Cupos: ", inscritos[i], " de ", cupoMax[i]
                FinPara
				Escribir " "
            3:
                choque_horario <- Falso
                Escribir "Seleccione miembro:"
                Para i <- 1 Hasta 2 Hacer
                    Escribir i, "- ", miembros[i]
                FinPara
                Leer miembro //numero del miembro seleccionado
				Escribir " "
				
                Escribir "Seleccione clase:"
                Para i <- 1 Hasta 2 Hacer
                    Escribir i, ". ", nombreClase[i]
                FinPara
                Leer clase //numero de la clase seleccionada
				
                // Validar cupo
                Si inscritos[clase] >= cupoMax[clase] Entonces
                    Escribir "Error: No hay cupo disponible en esta clase"
					Escribir " "
                Sino
                    // Validar choque de horario
                    Para j <- 1 Hasta 2 Hacer  
                        Si inscripciones[miembro,j] = 1 Entonces
                            Si horarioClase[j] = horarioClase[clase] Entonces
                                choque_horario <- Verdadero
                            FinSi
                        FinSi
                    FinPara
					
                    Si choque_horario = Verdadero Entonces
                        Escribir "Error: Choque de horario! Ya se encuentra inscrito en una clase en el mismo horario"
						Escribir " "
                    Sino
                        inscripciones[miembro,clase] <- 1 
                        inscritos[clase] <- inscritos[clase] + 1
                        Escribir "*** Inscripción exitosa ***"
                        Escribir "Miembro inscrito en: ", nombreClase[clase]
						Escribir " "
                    FinSi
					
                FinSi
				
        FinSegun
		
    Hasta Que opcion = 4
	Escribir "... FIN DEL SISTEMA ..."
	
FinAlgoritmo