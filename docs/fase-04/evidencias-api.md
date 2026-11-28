# Evidencias de validación de la API REST

## 1. Información general

| Propiedad | Valor |
|---|---|
| Proyecto | Sistema de Gestión Académica |
| Fase | 04 - Implementación API REST |
| Rama | feature/rest-api |
| Fecha de validación | 28 de noviembre de 2026 |
| Lenguaje | Python |
| Persistencia | MySQL |
| Sistema operativo | Kubuntu |
| Resultado | Satisfactorio |

## 2. Objetivo

Comprobar el funcionamiento de la API REST, la integración con MySQL y la conservación de las funcionalidades implementadas en las fases anteriores.

## 3. Estrategia de validación

Se realizaron las siguientes actividades:

- Verificación de archivos de implementación.
- Compilación del código Python.
- Ejecución de pruebas automatizadas de regresión.
- Inicio de un servidor HTTP temporal.
- Solicitudes HTTP reales.
- Validación de códigos de respuesta.
- Validación de estructuras JSON.
- Comprobación de reglas de negocio.
- Recuperación de información persistente.
- Limpieza de registros temporales.

## 4. Archivos de implementación

Salida observada mediante git ls-files:

```text
api/__init__.py
api/controladores/__init__.py
api/controladores/aprendices.py
api/controladores/calificaciones.py
api/controladores/cursos.py
api/controladores/inscripciones.py
api/controladores/profesores.py
api/controladores/reportes.py
api/enrutador.py
api/excepciones.py
api/respuestas.py
api/rutas.py
api/serializadores.py
api/servidor.py
api/validaciones.py
main_api.py
```

Total: 16 archivos de código.

## 5. Validación de sintaxis

Comando ejecutado:

```bash
python3 -m compileall -q api main_api.py
```

No se observaron errores de compilación en la salida compartida.

## 6. Pruebas automatizadas de regresión

Comando ejecutado:

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest discover -s tests -q
```

Resultado observado:

```text
----------------------------------------------------------------------
Ran 235 tests in 6.913s

OK
```

| Indicador | Resultado |
|---|---:|
| Pruebas ejecutadas | 235 |
| Pruebas superadas | 235 |
| Fallos reportados | 0 |
| Tiempo | 6.913 segundos |

## 7. Aislamiento de la base de datos

La comprobación integral verificó la base de datos y el usuario mediante:

```sql
SELECT DATABASE(), CURRENT_USER();
```

Valores esperados:

- Base de datos: sistema_gestion_academica_test.
- Usuario: academic_test_user.

Evidencia observada:

```text
[PASS] Base de datos de pruebas verificada
```

La comprobación utilizó identificadores generados para los registros temporales.

## 8. Verificación de endpoints

Evidencia observada:

```text
[PASS] 34 endpoints registrados
```

| Módulo | Endpoints ejercitados | Resultado |
|---|---:|---|
| Salud | 1 | Correcto |
| Profesores | 5 | Correcto |
| Aprendices | 7 | Correcto |
| Cursos | 8 | Correcto |
| Inscripciones | 7 | Correcto |
| Calificaciones | 4 | Correcto |
| Reportes | 2 | Correcto |
| Total | 34 | Correcto |

La ejecución realizó solicitudes HTTP reales contra un servidor temporal en localhost.

## 9. Salud del servidor

Fragmento de la salida observada:

```text
[PASS] Salud del servidor — HTTP 200
[PASS] Salud del servidor — estructura JSON
```

## 10. Gestión de profesores

```text
[PASS] Registrar profesor — HTTP 201
[PASS] Registrar profesor — estructura JSON
[PASS] Listar profesores — HTTP 200
[PASS] Listar profesores — estructura JSON
[PASS] Buscar profesor — HTTP 200
[PASS] Buscar profesor — estructura JSON
[PASS] Profesor duplicado — HTTP 409
[PASS] Profesor duplicado — estructura JSON
```

Resultado: correcto.

## 11. Gestión de aprendices

```text
[PASS] Registrar aprendiz — HTTP 201
[PASS] Registrar aprendiz — estructura JSON
[PASS] Listar aprendices — HTTP 200
[PASS] Listar aprendices — estructura JSON
[PASS] Buscar aprendiz — HTTP 200
[PASS] Buscar aprendiz — estructura JSON
```

Resultado: correcto.

## 12. Gestión de cursos

```text
[PASS] Registrar curso — HTTP 201
[PASS] Registrar curso — estructura JSON
[PASS] Listar cursos — HTTP 200
[PASS] Listar cursos — estructura JSON
[PASS] Buscar curso — HTTP 200
[PASS] Buscar curso — estructura JSON
[PASS] Asignar profesor — HTTP 200
[PASS] Asignar profesor — estructura JSON
```

Resultado: correcto.

## 13. Gestión de inscripciones

```text
[PASS] Registrar inscripción — HTTP 201
[PASS] Registrar inscripción — estructura JSON
[PASS] Listar inscripciones — HTTP 200
[PASS] Listar inscripciones — estructura JSON
[PASS] Buscar inscripción — HTTP 200
[PASS] Buscar inscripción — estructura JSON
[PASS] Rendimiento inicial — HTTP 200
[PASS] Rendimiento inicial — estructura JSON
[PASS] Estado académico pendiente
```

Resultado: correcto.

## 14. Gestión de calificaciones

Se registraron tres calificaciones mediante HTTP.

| Calificación | Nota inicial | Nota posterior |
|---|---:|---:|
| Primera | 3.0 | 4.0 |
| Segunda | 4.0 | 4.0 |
| Tercera | 5.0 | 5.0 |

Fragmento de la salida observada:

```text
[PASS] Listar calificaciones — HTTP 200
[PASS] Listar calificaciones — estructura JSON
[PASS] Buscar calificación — HTTP 200
[PASS] Buscar calificación — estructura JSON
[PASS] Consultar promedio — HTTP 200
[PASS] Consultar promedio — estructura JSON
[PASS] Promedio inicial igual a 4.0
[PASS] Modificar calificación — HTTP 200
[PASS] Modificar calificación — estructura JSON
[PASS] Consultar promedio actualizado — HTTP 200
[PASS] Consultar promedio actualizado — estructura JSON
[PASS] Promedio actualizado igual a 4.33
[PASS] Estado académico aprobado
```

### Cálculo inicial

```text
(3.0 + 4.0 + 5.0) / 3 = 4.00
```

### Cálculo posterior

```text
(4.0 + 4.0 + 5.0) / 3 = 4.33
```

Resultado: correcto.

## 15. Consultas relacionadas

Se realizaron doce consultas relacionadas.

| Consulta | Resultado |
|---|---|
| Cursos por profesor | HTTP 200 |
| Aprendices por profesor | HTTP 200 |
| Cursos por aprendiz | HTTP 200 |
| Inscripciones por aprendiz | HTTP 200 |
| Calificaciones por aprendiz | HTTP 200 |
| Rendimiento por aprendiz | HTTP 200 |
| Aprendices por curso | HTTP 200 |
| Inscripciones por curso | HTTP 200 |
| Calificaciones por curso | HTTP 200 |
| Rendimiento por curso | HTTP 200 |
| Calificaciones por inscripción | HTTP 200 |
| Rendimiento por inscripción | HTTP 200 |

Las doce consultas superaron también la comprobación de estructura JSON.

## 16. Validación de cambios de estado

```text
[PASS] Finalizar inscripción — HTTP 200
[PASS] Finalizar inscripción — estructura JSON
[PASS] Impedir modificar nota finalizada — HTTP 409
[PASS] Impedir modificar nota finalizada — estructura JSON
[PASS] Impedir transición inválida — HTTP 409
[PASS] Impedir transición inválida — estructura JSON
```

Se comprobó que una inscripción finalizada restringe la modificación de notas y las transiciones administrativas inválidas.

## 17. Reportes académicos

```text
[PASS] Resumen académico — HTTP 200
[PASS] Resumen académico — estructura JSON
[PASS] Reporte de calificaciones — HTTP 200
[PASS] Reporte de calificaciones — estructura JSON
```

Resultado: correcto.

## 18. Persistencia de información

Se creó una nueva instancia de GestionAcademica mediante la fábrica MySQL para recuperar la información registrada a través de HTTP.

Evidencia observada:

```text
[PASS] Recuperar profesor persistido
[PASS] Recuperar aprendiz persistido
[PASS] Recuperar curso persistido
[PASS] Recuperar asignación de profesor
[PASS] Recuperar estado persistido
[PASS] Recuperar tres notas persistidas
[PASS] Recuperar promedio persistente
```

La comprobación demuestra que los registros pueden recuperarse mediante una nueva instancia conectada a MySQL.

No constituye una prueba de reinicio del servidor HTTP ni del contenedor.

## 19. Manejo de errores HTTP

```text
[PASS] Ruta inexistente — HTTP 404
[PASS] Ruta inexistente — estructura JSON
[PASS] Método no permitido — HTTP 405
[PASS] Método no permitido — estructura JSON
[PASS] Campos obligatorios faltantes — HTTP 422
[PASS] Campos obligatorios faltantes — estructura JSON
```

Códigos HTTP comprobados durante la ejecución integral:

| Código | Resultado |
|---:|---|
| 200 | Correcto |
| 201 | Correcto |
| 404 | Correcto |
| 405 | Correcto |
| 409 | Correcto |
| 422 | Correcto |

## 20. Limpieza de registros

La comprobación ejecutó la eliminación de los registros temporales respetando el orden de dependencias:

1. Calificaciones.
2. Inscripciones.
3. Cursos.
4. Aprendices.
5. Profesores.
6. Registros de persona correspondientes a cada rol.

Evidencia observada:

```text
===== LIMPIEZA DE DATOS =====
[PASS] Limpieza de registros completada
[PASS] Servidor temporal detenido
```

La salida confirma que el procedimiento de limpieza terminó sin errores reportados.

No se realizó una comprobación independiente del número de registros restantes después de la limpieza.

## 21. Resultado de la comprobación integral

Salida observada:

```text
============================================================
TOTAL: 100 comprobaciones superadas
============================================================
```

Distribución de las comprobaciones contabilizadas:

| Categoría | Cantidad |
|---|---:|
| Registro de endpoints | 1 |
| Salud | 2 |
| Profesores | 8 |
| Aprendices | 6 |
| Cursos | 8 |
| Inscripciones | 9 |
| Calificaciones y promedios | 19 |
| Consultas relacionadas | 24 |
| Cambios de estado | 6 |
| Reportes | 4 |
| Persistencia | 7 |
| Errores HTTP | 6 |
| Total | 100 |

La verificación inicial del ambiente y los mensajes de limpieza se encuentran fuera del contador de 100 comprobaciones.

## 22. Consolidado de resultados

| Indicador | Resultado |
|---|---:|
| Archivos de implementación | 16 |
| Controladores | 6 |
| Endpoints ejercitados | 34 |
| Pruebas automatizadas anteriores | 235 |
| Comprobaciones temporales HTTP y MySQL | 100 |
| Total combinado de verificaciones | 335 |
| Fallos reportados | 0 |

## 23. Alcance de las evidencias

Los resultados corresponden a la ejecución observada durante la fase 4.

Las 100 comprobaciones fueron ejecutadas mediante un script temporal de Python y no representan 100 casos adicionales de unittest.

El total combinado de 335 corresponde a dos mecanismos diferentes de validación.

No se ha realizado una medición de cobertura de código.

La comprobación de los 34 endpoints no implica que se hayan evaluado todas sus entradas, respuestas y escenarios posibles.

## 24. Validaciones pendientes para la fase 5

- Pruebas permanentes del enrutador.
- Pruebas de validaciones.
- Pruebas de serializadores.
- Pruebas automatizadas de controladores.
- Pruebas HTTP de los endpoints.
- Pruebas adicionales de códigos de error.
- Pruebas de solicitudes malformadas.
- Pruebas de concurrencia.
- Pruebas de reinicio y recuperación.
- Verificación de limpieza de registros.
- Ejecución conjunta de todas las suites.

## 25. Conclusión

La ejecución confirmó el funcionamiento integral de los 34 endpoints, la comunicación HTTP mediante JSON, la persistencia de información en MySQL y las reglas académicas evaluadas.

Las 235 pruebas de regresión y las 100 comprobaciones temporales finalizaron satisfactoriamente.

La fase 4 dispone de una implementación funcional y evidencias de validación para continuar con la automatización de pruebas de la fase 5.