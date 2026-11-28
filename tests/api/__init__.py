import unittest

from gestion_academica import GestionAcademica

from personas.gestion_profesores import Gestion_profesores
from personas.gestion_aprendices import Gestion_aprendices
from cursos.gestion_cursos import GestionCursos
from inscripciones.gestion_inscripciones import GestionInscripciones
from calificaciones.gestion_calificaciones import GestionCalificaciones

from api.rutas import crear_enrutador
from api.respuestas import Respuesta


class BasePruebasAPI(unittest.TestCase):

    def setUp(self) -> None:

        self.sistema = GestionAcademica(
            profesores=Gestion_profesores(),
            aprendices=Gestion_aprendices(),
            cursos=GestionCursos(),
            inscripciones=GestionInscripciones(),
            calificaciones=GestionCalificaciones()
        )

        self.enrutador = crear_enrutador(self.sistema)

    def solicitar(
        self,
        metodo: str,
        ruta: str,
        datos: dict | None = None
    ) -> Respuesta:

        return self.enrutador.resolver(
            metodo=metodo,
            url=f"/api/v1{ruta}",
            datos=datos or {}
        )

    def verificar_respuesta(
        self,
        respuesta: Respuesta,
        estado: int,
        exito: bool = True
    ) -> None:

        self.assertEqual(
            respuesta.estado,
            estado
        )

        self.assertIsInstance(
            respuesta.contenido,
            dict
        )

        self.assertEqual(
            respuesta.contenido["exito"],
            exito
        )

        self.assertIn(
            "mensaje",
            respuesta.contenido
        )

        self.assertIn(
            "datos",
            respuesta.contenido
        )