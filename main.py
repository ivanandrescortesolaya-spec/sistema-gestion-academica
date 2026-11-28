
from gestion_academica import GestionAcademica

from personas.profesores import Profesor
from personas.aprendices import Aprendiz
from cursos.curso import Curso
from inscripciones.inscripcion import Inscripcion
from calificaciones.calificacion import Calificacion

from personas.gestion_profesores import Gestion_profesores
from personas.gestion_aprendices import Gestion_aprendices
from cursos.gestion_cursos import GestionCursos
from inscripciones.gestion_inscripciones import GestionInscripciones
from calificaciones.gestion_calificaciones import GestionCalificaciones



# Funciones auxiliares

def mostrar_registros(registros, mensaje):
    if not registros:
        print(f"\n{mensaje}")
        return

    for registro in registros:
        print("\n------------------------")
        print(registro.mostrar_informacion())


def mostrar_rendimiento(resultado):
    print("\n------------------------")
    print(f"Inscripción: {resultado['inscripcion']}")
    print(f"Aprendiz: {resultado['aprendiz']}")
    print(f"Curso: {resultado['curso']}")

    notas = resultado["notas"]

    if notas:
        print("Notas:", ", ".join(f"{nota:.2f}" for nota in notas))
    else:
        print("Notas: Sin calificaciones")

    promedio = resultado["promedio"]

    if promedio is None:
        print("Promedio: Pendiente")
    else:
        print(f"Promedio: {promedio:.2f}")

    print(f"Estado: {resultado['estado']}")


def mostrar_resumen(sistema: GestionAcademica):
    resumen = sistema.obtener_resumen()

    print("\n--- Resumen académico ---")
    print(f"Profesores: {resumen['profesores']}")
    print(f"Aprendices: {resumen['aprendices']}")
    print(f"Cursos: {resumen['cursos']}")
    print(f"Inscripciones: {resumen['inscripciones']}")
    print(f"Calificaciones: {resumen['calificaciones']}")


# Menu principal

def mostrar_menu():
    print("\n====================================")
    print("   SISTEMA DE GESTIÓN ACADÉMICA")
    print("====================================")
    print("1. Gestión de profesores")
    print("2. Gestión de aprendices")
    print("3. Gestión de cursos")
    print("4. Gestión de inscripciones")
    print("5. Gestión de calificaciones")
    print("6. Reportes académicos")
    print("0. Salir")


# Gestion de profesores

def menu_profesores(sistema: GestionAcademica):
    while True:
        print("\n====================================")
        print("       GESTIÓN DE PROFESORES")
        print("====================================")
        print("1. Registrar profesor")
        print("2. Buscar profesor")
        print("3. Listar profesores")
        print("4. Consultar cursos asignados")
        print("5. Consultar aprendices de sus cursos")
        print("0. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()

        try:
            match opcion:
                case "1":
                    nombre = input("Nombre: ")
                    documento = int(input("Documento: "))
                    edad = int(input("Edad: "))
                    profesion = input("Profesión: ")
                    codigo = int(input("Código: "))
                    especialidad = input("Especialidad: ")

                    profesor = Profesor(
                        nombre,
                        documento,
                        edad,
                        profesion,
                        codigo,
                        especialidad
                    )

                    sistema.registrar_profesor(profesor)

                    print("\nProfesor registrado correctamente.")

                case "2":
                    documento = int(input("Documento: "))
                    profesor = sistema.buscar_profesor(documento)

                    if profesor is None:
                        print("\nProfesor no encontrado.")
                    else:
                        print(profesor.mostrar_informacion())

                case "3":
                    mostrar_registros(
                        sistema.listar_profesores(),
                        "No hay profesores registrados."
                    )

                case "4":
                    documento = int(input("Documento del profesor: "))

                    if sistema.buscar_profesor(documento) is None:
                        print("\nProfesor no encontrado.")
                    else:
                        mostrar_registros(
                            sistema.consultar_cursos_profesor(
                                documento
                            ),
                            "No tiene cursos asignados."
                        )

                case "5":
                    documento = int(input("Documento del profesor: "))

                    resultado = sistema.consultar_aprendices_profesor(
                        documento
                    )

                    if not resultado:
                        print("\nNo tiene cursos asignados.")
                    else:
                        for registro in resultado:
                            curso = registro["curso"]
                            aprendices = registro["aprendices"]

                            print(f"\nCurso: {curso.nombre}")

                            mostrar_registros(
                                aprendices,
                                "No hay aprendices inscritos."
                            )

                case "0":
                    break

                case _:
                    print("\nOpción inválida.")

        except ValueError as error:
            print(f"\nError: {error}")


# Gestion de aprendices

def menu_aprendices(sistema: GestionAcademica):
    while True:
        print("\n====================================")
        print("       GESTIÓN DE APRENDICES")
        print("====================================")
        print("1. Registrar aprendiz")
        print("2. Buscar aprendiz")
        print("3. Listar aprendices")
        print("4. Consultar cursos inscritos")
        print("0. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()

        try:
            match opcion:
                case "1":
                    nombre = input("Nombre: ")
                    documento = int(input("Documento: "))
                    edad = int(input("Edad: "))
                    telefono = input("Teléfono: ")
                    correo = input("Correo electrónico: ")
                    direccion = input("Dirección: ")

                    aprendiz = Aprendiz(
                        nombre,
                        documento,
                        edad,
                        telefono,
                        correo,
                        direccion
                    )

                    sistema.registrar_aprendiz(aprendiz)

                    print("\nAprendiz registrado correctamente.")

                case "2":
                    documento = int(input("Documento: "))
                    aprendiz = sistema.buscar_aprendiz(documento)

                    if aprendiz is None:
                        print("\nAprendiz no encontrado.")
                    else:
                        print(aprendiz.mostrar_informacion())

                case "3":
                    mostrar_registros(
                        sistema.listar_aprendices(),
                        "No hay aprendices registrados."
                    )

                case "4":
                    documento = int(input("Documento del aprendiz: "))

                    mostrar_registros(
                        sistema.consultar_cursos_aprendiz(documento),
                        "No tiene cursos inscritos."
                    )

                case "0":
                    break

                case _:
                    print("\nOpción inválida.")

        except ValueError as error:
            print(f"\nError: {error}")


# Gestion de cursos

def menu_cursos(sistema: GestionAcademica):
    while True:
        print("\n====================================")
        print("         GESTIÓN DE CURSOS")
        print("====================================")
        print("1. Registrar curso")
        print("2. Buscar curso")
        print("3. Listar cursos")
        print("4. Asignar profesor")
        print("5. Consultar aprendices inscritos")
        print("0. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()

        try:
            match opcion:
                case "1":
                    codigo = input("Código: ")
                    nombre = input("Nombre: ")
                    descripcion = input("Descripción: ")
                    duracion = int(input("Duración en horas: "))
                    modalidad = input(
                        "Modalidad (titulada/complementaria): "
                    )

                    curso = Curso(
                        codigo,
                        nombre,
                        descripcion,
                        duracion,
                        modalidad
                    )

                    sistema.registrar_curso(curso)

                    print("\nCurso registrado correctamente.")

                case "2":
                    codigo = input("Código del curso: ").strip()
                    curso = sistema.buscar_curso(codigo)

                    if curso is None:
                        print("\nCurso no encontrado.")
                    else:
                        print(curso.mostrar_informacion())

                case "3":
                    mostrar_registros(
                        sistema.listar_cursos(),
                        "No hay cursos registrados."
                    )

                case "4":
                    codigo = input("Código del curso: ").strip()
                    documento = int(input("Documento del profesor: "))

                    sistema.asignar_profesor(codigo, documento)

                    print("\nProfesor asignado correctamente.")

                case "5":
                    codigo = input("Código del curso: ").strip()

                    mostrar_registros(
                        sistema.consultar_aprendices_curso(codigo),
                        "No hay aprendices inscritos."
                    )

                case "0":
                    break

                case _:
                    print("\nOpción inválida.")

        except ValueError as error:
            print(f"\nError: {error}")


# Gestion de inscripciones

def menu_inscripciones(sistema: GestionAcademica):
    while True:
        print("\n====================================")
        print("      GESTIÓN DE INSCRIPCIONES")
        print("====================================")
        print("1. Registrar inscripción")
        print("2. Buscar inscripción")
        print("3. Listar inscripciones")
        print("4. Consultar inscripciones por aprendiz")
        print("5. Consultar inscripciones por curso")
        print("6. Cancelar inscripción")
        print("7. Finalizar inscripción")
        print("0. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()

        try:
            match opcion:
                case "1":
                    codigo = input("Código de inscripción: ").strip()
                    documento = int(input("Documento del aprendiz: "))
                    codigo_curso = input("Código del curso: ").strip()

                    aprendiz = sistema.buscar_aprendiz(documento)
                    curso = sistema.buscar_curso(codigo_curso)

                    if aprendiz is None:
                        raise ValueError("El aprendiz no está registrado")

                    if curso is None:
                        raise ValueError("El curso no está registrado")

                    inscripcion = Inscripcion(
                        codigo,
                        aprendiz,
                        curso
                    )

                    sistema.registrar_inscripcion(inscripcion)

                    print("\nInscripción registrada correctamente.")

                case "2":
                    codigo = input("Código de inscripción: ").strip()
                    inscripcion = sistema.buscar_inscripcion(codigo)

                    if inscripcion is None:
                        print("\nInscripción no encontrada.")
                    else:
                        print(inscripcion.mostrar_informacion())

                case "3":
                    mostrar_registros(
                        sistema.listar_inscripciones(),
                        "No hay inscripciones registradas."
                    )

                case "4":
                    documento = int(input("Documento del aprendiz: "))

                    if sistema.buscar_aprendiz(documento) is None:
                        raise ValueError("El aprendiz no está registrado")

                    mostrar_registros(
                        sistema.consultar_inscripciones_aprendiz(
                            documento
                        ),
                        "No hay inscripciones registradas."
                    )

                case "5":
                    codigo = input("Código del curso: ").strip()

                    if sistema.buscar_curso(codigo) is None:
                        raise ValueError("El curso no está registrado")

                    mostrar_registros(
                        sistema.consultar_inscripciones_curso(codigo),
                        "No hay inscripciones registradas."
                    )

                case "6":
                    codigo = input("Código de inscripción: ").strip()
                    inscripcion = sistema.buscar_inscripcion(codigo)

                    if inscripcion is None:
                        raise ValueError("La inscripción no existe")

                    inscripcion.cancelar()

                    print("\nInscripción cancelada correctamente.")

                case "7":
                    codigo = input("Código de inscripción: ").strip()
                    inscripcion = sistema.buscar_inscripcion(codigo)

                    if inscripcion is None:
                        raise ValueError("La inscripción no existe")

                    inscripcion.finalizar()

                    print("\nInscripción finalizada correctamente.")

                case "0":
                    break

                case _:
                    print("\nOpción inválida.")

        except ValueError as error:
            print(f"\nError: {error}")


# Gestion de calificaciones

def menu_calificaciones(sistema: GestionAcademica):
    while True:
        print("\n====================================")
        print("      GESTIÓN DE CALIFICACIONES")
        print("====================================")
        print("1. Registrar calificación")
        print("2. Buscar calificación")
        print("3. Listar calificaciones")
        print("4. Modificar calificación")
        print("5. Consultar notas por inscripción")
        print("6. Consultar notas por aprendiz")
        print("7. Consultar notas por curso")
        print("8. Consultar promedio y estado académico")
        print("0. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()

        try:
            match opcion:
                case "1":
                    codigo = input("Código de calificación: ").strip()

                    codigo_inscripcion = input(
                        "Código de inscripción: "
                    ).strip()

                    inscripcion = sistema.buscar_inscripcion(
                        codigo_inscripcion
                    )

                    if inscripcion is None:
                        raise ValueError("La inscripción no existe")

                    nota = float(input("Nota (0.0 - 5.0): "))

                    calificacion = Calificacion(
                        codigo,
                        inscripcion,
                        nota
                    )

                    sistema.registrar_calificacion(calificacion)

                    print("\nCalificación registrada correctamente.")

                case "2":
                    codigo = input("Código de calificación: ").strip()

                    calificacion = sistema.buscar_calificacion(codigo)

                    if calificacion is None:
                        print("\nCalificación no encontrada.")
                    else:
                        print(calificacion.mostrar_informacion())

                case "3":
                    mostrar_registros(
                        sistema.listar_calificaciones(),
                        "No hay calificaciones registradas."
                    )

                case "4":
                    codigo = input("Código de calificación: ").strip()
                    nueva_nota = float(input("Nueva nota: "))

                    sistema.modificar_calificacion(
                        codigo,
                        nueva_nota
                    )

                    print("\nCalificación modificada correctamente.")

                case "5":
                    codigo = input("Código de inscripción: ").strip()

                    if sistema.buscar_inscripcion(codigo) is None:
                        raise ValueError("La inscripción no existe")

                    mostrar_registros(
                        sistema.consultar_calificaciones_inscripcion(
                            codigo
                        ),
                        "No hay calificaciones registradas."
                    )

                case "6":
                    documento = int(input("Documento del aprendiz: "))

                    if sistema.buscar_aprendiz(documento) is None:
                        raise ValueError("El aprendiz no está registrado")

                    mostrar_registros(
                        sistema.consultar_calificaciones_aprendiz(
                            documento
                        ),
                        "No hay calificaciones registradas."
                    )

                case "7":
                    codigo = input("Código del curso: ").strip()

                    if sistema.buscar_curso(codigo) is None:
                        raise ValueError("El curso no está registrado")

                    mostrar_registros(
                        sistema.consultar_calificaciones_curso(codigo),
                        "No hay calificaciones registradas."
                    )

                case "8":
                    codigo = input("Código de inscripción: ").strip()

                    resultado = sistema.consultar_rendimiento_inscripcion(
                        codigo
                    )

                    mostrar_rendimiento(resultado)

                case "0":
                    break

                case _:
                    print("\nOpción inválida.")

        except ValueError as error:
            print(f"\nError: {error}")


# Reportes academicos

def menu_reportes(sistema: GestionAcademica):
    while True:
        print("\n====================================")
        print("         REPORTES ACADÉMICOS")
        print("====================================")
        print("1. Resumen académico")
        print("2. Reporte general de calificaciones")
        print("3. Rendimiento por aprendiz")
        print("4. Rendimiento por curso")
        print("5. Rendimiento por inscripción")
        print("0. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()

        try:
            match opcion:
                case "1":
                    mostrar_resumen(sistema)

                case "2":
                    print(sistema.generar_reporte_calificaciones())

                case "3":
                    documento = int(input("Documento del aprendiz: "))

                    resultados = sistema.consultar_rendimiento_aprendiz(
                        documento
                    )

                    if not resultados:
                        print("\nNo hay inscripciones registradas.")
                    else:
                        for resultado in resultados:
                            mostrar_rendimiento(resultado)

                case "4":
                    codigo = input("Código del curso: ").strip()

                    resultados = sistema.consultar_rendimiento_curso(
                        codigo
                    )

                    if not resultados:
                        print("\nNo hay inscripciones registradas.")
                    else:
                        for resultado in resultados:
                            mostrar_rendimiento(resultado)

                case "5":
                    codigo = input("Código de inscripción: ").strip()

                    resultado = sistema.consultar_rendimiento_inscripcion(
                        codigo
                    )

                    mostrar_rendimiento(resultado)

                case "0":
                    break

                case _:
                    print("\nOpción inválida.")

        except ValueError as error:
            print(f"\nError: {error}")


# Ejecucion principal


def main():
    sistema = GestionAcademica(
        profesores=Gestion_profesores(),
        aprendices=Gestion_aprendices(),
        cursos=GestionCursos(),
        inscripciones=GestionInscripciones(),
        calificaciones=GestionCalificaciones()
    )


    while True:
        mostrar_menu()

        opcion = input("\nSeleccione una opción: ").strip()

        match opcion:
            case "1":
                menu_profesores(sistema)

            case "2":
                menu_aprendices(sistema)

            case "3":
                menu_cursos(sistema)

            case "4":
                menu_inscripciones(sistema)

            case "5":
                menu_calificaciones(sistema)

            case "6":
                menu_reportes(sistema)

            case "0":
                print("\nGracias por utilizar el sistema.")
                break

            case _:
                print("\nOpción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
