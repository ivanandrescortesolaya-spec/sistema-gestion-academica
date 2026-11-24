
from gestion_academica import GestionAcademica


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


def main():
    sistema = GestionAcademica()

    while True:
        mostrar_menu()

        opcion = input("\nSeleccione una opción: ").strip()

        match opcion:
            case "1":
                print("\nGestión de profesores")

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
