from api import PREFIJO_API, VERSION_API

from api.enrutador import Enrutador

from api.respuestas import respuesta_exitosa

from api.controladores import (
    ControladorProfesores,
    ControladorAprendices,
    ControladorCursos,
    ControladorInscripciones,
    ControladorCalificaciones,
    ControladorReportes
)

from gestion_academica import GestionAcademica


def crear_enrutador(
    sistema: GestionAcademica
) -> Enrutador:

    enrutador = Enrutador()

    profesores = ControladorProfesores(sistema)
    aprendices = ControladorAprendices(sistema)
    cursos = ControladorCursos(sistema)
    inscripciones = ControladorInscripciones(sistema)
    calificaciones = ControladorCalificaciones(sistema)
    reportes = ControladorReportes(sistema)

    base = PREFIJO_API

    # Salud del servidor

    enrutador.registrar(
        "GET",
        f"{base}/salud",
        lambda parametros, datos: respuesta_exitosa({
            "estado": "operativo",
            "version": VERSION_API,
            "servicio": "Sistema de Gestión Académica"
        })
    )

    # Profesores

    enrutador.registrar(
        "GET",
        f"{base}/profesores",
        profesores.listar
    )

    enrutador.registrar(
        "POST",
        f"{base}/profesores",
        profesores.registrar
    )

    enrutador.registrar(
        "GET",
        f"{base}/profesores/{{documento}}",
        profesores.buscar
    )

    enrutador.registrar(
        "GET",
        f"{base}/profesores/{{documento}}/cursos",
        profesores.consultar_cursos
    )

    enrutador.registrar(
        "GET",
        f"{base}/profesores/{{documento}}/aprendices",
        profesores.consultar_aprendices
    )

    # Aprendices

    enrutador.registrar(
        "GET",
        f"{base}/aprendices",
        aprendices.listar
    )

    enrutador.registrar(
        "POST",
        f"{base}/aprendices",
        aprendices.registrar
    )

    enrutador.registrar(
        "GET",
        f"{base}/aprendices/{{documento}}",
        aprendices.buscar
    )

    enrutador.registrar(
        "GET",
        f"{base}/aprendices/{{documento}}/cursos",
        aprendices.consultar_cursos
    )

    enrutador.registrar(
        "GET",
        f"{base}/aprendices/{{documento}}/inscripciones",
        aprendices.consultar_inscripciones
    )

    enrutador.registrar(
        "GET",
        f"{base}/aprendices/{{documento}}/calificaciones",
        aprendices.consultar_calificaciones
    )

    enrutador.registrar(
        "GET",
        f"{base}/aprendices/{{documento}}/rendimiento",
        aprendices.consultar_rendimiento
    )

    # Cursos

    enrutador.registrar(
        "GET",
        f"{base}/cursos",
        cursos.listar
    )

    enrutador.registrar(
        "POST",
        f"{base}/cursos",
        cursos.registrar
    )

    enrutador.registrar(
        "GET",
        f"{base}/cursos/{{codigo}}",
        cursos.buscar
    )

    enrutador.registrar(
        "PUT",
        f"{base}/cursos/{{codigo}}/profesor",
        cursos.asignar_profesor
    )

    enrutador.registrar(
        "GET",
        f"{base}/cursos/{{codigo}}/aprendices",
        cursos.consultar_aprendices
    )

    enrutador.registrar(
        "GET",
        f"{base}/cursos/{{codigo}}/inscripciones",
        cursos.consultar_inscripciones
    )

    enrutador.registrar(
        "GET",
        f"{base}/cursos/{{codigo}}/calificaciones",
        cursos.consultar_calificaciones
    )

    enrutador.registrar(
        "GET",
        f"{base}/cursos/{{codigo}}/rendimiento",
        cursos.consultar_rendimiento
    )

    # Inscripciones

    enrutador.registrar(
        "GET",
        f"{base}/inscripciones",
        inscripciones.listar
    )

    enrutador.registrar(
        "POST",
        f"{base}/inscripciones",
        inscripciones.registrar
    )

    enrutador.registrar(
        "GET",
        f"{base}/inscripciones/{{codigo}}",
        inscripciones.buscar
    )

    enrutador.registrar(
        "PATCH",
        f"{base}/inscripciones/{{codigo}}/estado",
        inscripciones.cambiar_estado
    )

    enrutador.registrar(
        "GET",
        f"{base}/inscripciones/{{codigo}}/calificaciones",
        inscripciones.consultar_calificaciones
    )

    enrutador.registrar(
        "GET",
        f"{base}/inscripciones/{{codigo}}/rendimiento",
        inscripciones.consultar_rendimiento
    )

    enrutador.registrar(
        "GET",
        f"{base}/inscripciones/{{codigo}}/promedio",
        inscripciones.calcular_promedio
    )

    # Calificaciones

    enrutador.registrar(
        "GET",
        f"{base}/calificaciones",
        calificaciones.listar
    )

    enrutador.registrar(
        "POST",
        f"{base}/calificaciones",
        calificaciones.registrar
    )

    enrutador.registrar(
        "GET",
        f"{base}/calificaciones/{{codigo}}",
        calificaciones.buscar
    )

    enrutador.registrar(
        "PATCH",
        f"{base}/calificaciones/{{codigo}}",
        calificaciones.modificar
    )

    # Reportes

    enrutador.registrar(
        "GET",
        f"{base}/reportes/resumen",
        reportes.resumen
    )

    enrutador.registrar(
        "GET",
        f"{base}/reportes/calificaciones",
        reportes.calificaciones
    )

    return enrutador