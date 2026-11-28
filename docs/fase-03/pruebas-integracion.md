# Pruebas de integración con MySQL

## 1. Introducción

Las pruebas de integración verifican la comunicación
entre el aplicativo Python, los repositorios y
la base de datos MySQL.

Complementan las 182 pruebas originales del sistema.

## 2. Objetivos

- Verificar la conexión con MySQL.
- Validar el aislamiento del ambiente de pruebas.
- Comprobar las operaciones de los repositorios.
- Verificar la persistencia de información.
- Comprobar las restricciones de negocio.
- Detectar regresiones del aplicativo original.

## 3. Herramientas

- Python.
- unittest.
- MySQL 8.4.
- mysql-connector-python.
- Docker.
- Pylance.

## 4. Estructura de pruebas

```text
tests/integracion/
├── __init__.py
├── test_conexion.py
├── test_repositorio_profesores.py
├── test_repositorio_aprendices.py
├── test_repositorio_cursos.py
├── test_repositorio_inscripciones.py
├── test_repositorio_calificaciones.py
└── test_persistencia.py
```

## 5. Base reutilizable de integración

BaseIntegracion centraliza:

- Configuración del ambiente.
- Verificación de la base de datos.
- Verificación del usuario.
- Construcción del sistema.
- Generación de identificadores de prueba.
- Preparación de entidades.
- Limpieza de registros temporales.

## 6. Aislamiento de pruebas

Las pruebas utilizan exclusivamente:

```text
Base: sistema_gestion_academica_test
Usuario: academic_test_user
```

La ejecución requiere:

```bash
RUN_MYSQL_TESTS=1
```

Esto evita ejecutar accidentalmente las pruebas
de integración durante una ejecución ordinaria.

## 7. Pruebas de conexión

Archivo: test_conexion.py

| Caso | Validación |
|---|---|
| 1 | Conexión con MySQL |
| 2 | Base de datos de pruebas |
| 3 | Usuario de pruebas |
| 4 | Rollback de transacciones |

Total: 4 pruebas.

## 8. Repositorio de profesores

Archivo: test_repositorio_profesores.py

| Caso | Validación |
|---|---|
| 1 | Registrar profesor |
| 2 | Recuperar datos |
| 3 | Listar profesores |
| 4 | Rechazar duplicados |
| 5 | Consultar profesor inexistente |

Total: 5 pruebas.

## 9. Repositorio de aprendices

Archivo: test_repositorio_aprendices.py

| Caso | Validación |
|---|---|
| 1 | Registrar aprendiz |
| 2 | Recuperar datos personales |
| 3 | Listar aprendices |
| 4 | Rechazar duplicados |
| 5 | Consultar aprendiz inexistente |

Total: 5 pruebas.

## 10. Repositorio de cursos

Archivo: test_repositorio_cursos.py

| Caso | Validación |
|---|---|
| 1 | Registrar curso |
| 2 | Consultar curso sin profesor |
| 3 | Asignar profesor |
| 4 | Buscar cursos por profesor |
| 5 | Rechazar cursos duplicados |
| 6 | Listar cursos |
| 7 | Consultar curso inexistente |

Total: 7 pruebas.

## 11. Repositorio de inscripciones

Archivo: test_repositorio_inscripciones.py

| Caso | Validación |
|---|---|
| 1 | Registrar inscripción |
| 2 | Rechazar código duplicado |
| 3 | Rechazar duplicidad aprendiz-curso |
| 4 | Buscar por aprendiz |
| 5 | Buscar por curso |
| 6 | Cancelar inscripción |
| 7 | Finalizar inscripción |
| 8 | Rechazar transición inválida |
| 9 | Listar inscripciones |

Total: 9 pruebas.

## 12. Repositorio de calificaciones

Archivo: test_repositorio_calificaciones.py

| Caso | Validación |
|---|---|
| 1 | Registrar calificación |
| 2 | Rechazar calificación duplicada |
| 3 | Modificar calificación |
| 4 | Calcular promedio |
| 5 | Recalcular promedio |
| 6 | Determinar aprobación |
| 7 | Determinar reprobación |
| 8 | Determinar rendimiento pendiente |
| 9 | Rechazar promedio insuficiente |
| 10 | Buscar notas por inscripción |
| 11 | Buscar notas por aprendiz |
| 12 | Buscar notas por curso |
| 13 | Impedir modificación de inscripción finalizada |
| 14 | Impedir registro en inscripción cancelada |

Total: 14 pruebas.

## 13. Pruebas de persistencia

Archivo: test_persistencia.py

| Caso | Validación |
|---|---|
| 1 | Persistencia de profesores |
| 2 | Persistencia de aprendices |
| 3 | Persistencia de cursos |
| 4 | Persistencia de asignaciones |
| 5 | Persistencia de inscripciones |
| 6 | Persistencia de estados |
| 7 | Persistencia de calificaciones |
| 8 | Persistencia de rendimiento |
| 9 | Generación de reportes persistentes |

Total: 9 pruebas.

Estas pruebas construyen nuevas instancias
del aplicativo para recuperar los datos almacenados.

## 14. Distribución de pruebas

| Componente | Cantidad |
|---|---:|
| Conexión | 4 |
| Profesores | 5 |
| Aprendices | 5 |
| Cursos | 7 |
| Inscripciones | 9 |
| Calificaciones | 14 |
| Persistencia | 9 |
| Total de integración | 53 |
| Pruebas originales | 182 |
| Total general | 235 |

## 15. Limpieza de datos

Las pruebas utilizan identificadores temporales
y eliminan los registros creados respetando
las relaciones de integridad referencial.

Orden de limpieza:

1. Calificaciones.
2. Inscripciones.
3. Cursos.
4. Aprendices.
5. Profesores.
6. Registros personales correspondientes.

No se utiliza TRUNCATE sobre las tablas.

## 16. Validación de tipos

Durante el desarrollo se identificaron 40
diagnósticos de Pylance.

Se incorporaron comprobaciones de valores
opcionales, validaciones de filas SQL y
anotaciones de tipos.

Las correcciones permiten verificar que los
objetos recuperados existen antes de acceder
a sus atributos.

## 17. Ejecución

```bash
python3 -m compileall -q tests persistencia &&
RUN_MYSQL_TESTS=1 python3 -m unittest discover -s tests -v
```

## 18. Criterios de aceptación

- Conexión MySQL disponible.
- Ambiente de pruebas independiente.
- 53 pruebas de integración aprobadas.
- 182 pruebas originales aprobadas.
- Ausencia de errores durante la ejecución.
- Recuperación de información persistente.
- Limpieza de los registros temporales.

## 19. Alcance y limitaciones

Las pruebas verifican los escenarios implementados,
pero no representan una cobertura del 100 % del código.

No se han realizado pruebas exhaustivas de carga,
concurrencia o seguridad ofensiva.

La recuperación mediante nuevas instancias no
equivale por sí sola a una prueba de recuperación
ante desastres.

## 20. Conclusión

Las pruebas de integración permiten verificar
el funcionamiento de la persistencia MySQL
y conservar la compatibilidad con los escenarios
originales del aplicativo.