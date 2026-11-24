
from gestion_academica import GestionAcademica
from personas.profesores import Profesor


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


def main():
    sistema = GestionAcademica()

    while True:
        mostrar_menu()

        opcion = input("\nSeleccione una opción: ").strip()

        match opcion:
            case "1":
                menu_profesores(sistema)

            case "2":
                print("\nGestión de aprendices")

            case "3":
                print("\nGestión de cursos")

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
