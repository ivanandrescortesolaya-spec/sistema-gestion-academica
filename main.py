
from gestion_academica import GestionAcademica
from personas.profesores import Profesor
from gestion_academica import GestionAcademica
from personas.profesores import Profesor
from personas.aprendices import Aprendiz
from gestion_academica import GestionAcademica
from personas.profesores import Profesor
from personas.aprendices import Aprendiz
from cursos.curso import Curso


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


def menu_profesores(sistema: GestionAcademica):
    while True:
        print("\n====================================")
        print("       GESTIÓN DE PROFESORES")
        print("====================================")
        print("1. Registrar profesor")
        print("2. Buscar profesor")
        print("3. Listar profesores")
        print("4. Consultar cursos asignados")
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
                    profesores = sistema.listar_profesores()

                    if not profesores:
                        print("\nNo hay profesores registrados.")
                    else:
                        for profesor in profesores:
                            print("\n------------------------")
                            print(profesor.mostrar_informacion())

                case "4":
                    documento = int(input("Documento del profesor: "))

                    if sistema.buscar_profesor(documento) is None:
                        print("\nProfesor no encontrado.")
                    else:
                        cursos = sistema.consultar_cursos_profesor(
                            documento
                        )

                        if not cursos:
                            print("\nNo tiene cursos asignados.")
                        else:
                            for curso in cursos:
                                print("\n------------------------")
                                print(curso.mostrar_informacion())

                case "0":
                    break

                case _:
                    print("\nOpción inválida.")

        except ValueError as error:
            print(f"\nError: {error}")


def menu_aprendices(sistema: GestionAcademica):
    while True:
        print("\n====================================")
        print("       GESTIÓN DE APRENDICES")
        print("====================================")
        print("1. Registrar aprendiz")
        print("2. Buscar aprendiz")
        print("3. Listar aprendices")
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
                    aprendices = sistema.listar_aprendices()

                    if not aprendices:
                        print("\nNo hay aprendices registrados.")
                    else:
                        for aprendiz in aprendices:
                            print("\n------------------------")
                            print(aprendiz.mostrar_informacion())

                case "0":
                    break

                case _:
                    print("\nOpción inválida.")

        except ValueError as error:
            print(f"\nError: {error}")


def menu_cursos(sistema: GestionAcademica):
    while True:
        print("\n====================================")
        print("         GESTIÓN DE CURSOS")
        print("====================================")
        print("1. Registrar curso")
        print("2. Buscar curso")
        print("3. Listar cursos")
        print("4. Asignar profesor")
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
                    cursos = sistema.listar_cursos()

                    if not cursos:
                        print("\nNo hay cursos registrados.")
                    else:
                        for curso in cursos:
                            print("\n------------------------")
                            print(curso.mostrar_informacion())

                case "4":
                    codigo = input("Código del curso: ").strip()
                    documento = int(
                        input("Documento del profesor: ")
                    )

                    sistema.asignar_profesor(codigo, documento)

                    print("\nProfesor asignado correctamente.")

                case "0":
                    break

                case _:
                    print("\nOpción inválida.")

        except ValueError as error:
            print(f"\nError: {error}")


def main():
    sistema = GestionAcademica()

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
                print("\nMódulo de inscripciones pendiente")

            case "5":
                print("\nMódulo de calificaciones pendiente")

            case "6":
                resumen = sistema.obtener_resumen()

                print("\n--- Resumen académico ---")
                print(f"Profesores: {resumen['profesores']}")
                print(f"Aprendices: {resumen['aprendices']}")
                print(f"Cursos: {resumen['cursos']}")

            case "0":
                print("\nGracias por utilizar el sistema.")
                break

            case _:
                print("\nOpción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
