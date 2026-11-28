# Pruebas de integración de la API REST con MySQL

## 1. Introducción

Las pruebas de integración verifican el funcionamiento
conjunto de la API REST, la lógica de negocio, los
repositorios y la base de datos MySQL.

A diferencia de las pruebas en memoria, estas pruebas
realizan operaciones sobre una base de datos relacional real.

## 2. Objetivo general

Comprobar la comunicación entre los componentes del sistema,
la integridad de las operaciones concurrentes y la
persistencia de los datos académicos.

## 3. Arquitectura de integración

```text
Cliente HTTP de pruebas
          |
          v
Servidor HTTP
          |
          v
Enrutador REST
          |
          v
Controladores
          |
          v
GestionAcademica
          |
          v
Repositorios MySQL
          |
          v
ConexionMySQL
          |
          v
sistema_gestion_academica_test
```

## 4. Entorno de ejecución

| Componente | Configuración |
|---|---|
| Motor | MySQL 8.4 |
| Contenedor | academic-mysql |
| Servicio Docker Compose | mysql |
| Host | 127.0.0.1 |
| Puerto local | 3307 |
| Puerto interno | 3306 |
| Base de datos | sistema_gestion_academica_test |
| Usuario | academic_test_user |

La configuración se obtiene mediante variables de entorno.

Las pruebas se habilitan utilizando:

```bash
RUN_MYSQL_TESTS=1
```

## 5. Aislamiento de pruebas

La clase BaseIntegracion verifica la base de datos y el
usuario mediante la consulta:

```sql
SELECT DATABASE(), CURRENT_USER();
```

Los valores esperados corresponden exclusivamente al
entorno de pruebas.

Se generan identificadores dinámicos para evitar conflictos
entre registros de diferentes ejecuciones.

La limpieza elimina los registros creados respetando las
dependencias entre las tablas.

## 6. Archivos implementados

```text
tests/integracion/
├── __init__.py
├── test_api_mysql.py
├── test_api_concurrencia.py
├── test_api_persistencia.py
├── test_conexion.py
├── test_persistencia.py
├── test_repositorio_aprendices.py
├── test_repositorio_calificaciones.py
├── test_repositorio_cursos.py
├── test_repositorio_inscripciones.py
└── test_repositorio_profesores.py
```

## 7. Distribución de pruebas

| Archivo | Cantidad |
|---|---:|
| test_api_mysql.py | 30 |
| test_api_concurrencia.py | 10 |
| test_api_persistencia.py | 15 |
| Total de integración API | 55 |

Pruebas de integración conservadas de la fase anterior:

| Archivo | Cantidad |
|---|---:|
| test_conexion.py | 4 |
| test_persistencia.py | 9 |
| test_repositorio_aprendices.py | 5 |
| test_repositorio_calificaciones.py | 14 |
| test_repositorio_cursos.py | 7 |
| test_repositorio_inscripciones.py | 9 |
| test_repositorio_profesores.py | 5 |
| Total de integración anterior | 53 |

El conjunto de integración contiene 108 pruebas.

## 8. Integración API MySQL

Archivo: test_api_mysql.py.

Cantidad: 30 pruebas.

Se comprueban los siguientes escenarios:

- Aislamiento de la base de datos.
- Cantidad de rutas registradas.
- Disponibilidad del servidor.
- Registro y consulta de profesores.
- Registro y consulta de aprendices.
- Registro y consulta de cursos.
- Asignación de profesores.
- Registro y consulta de inscripciones.
- Cancelación y finalización de inscripciones.
- Registro y modificación de calificaciones.
- Validación de calificaciones fuera de rango.
- Cálculo y actualización de promedios.
- Rechazo de registros duplicados.
- Consultas de relaciones académicas.
- Generación de reportes y resúmenes.

## 9. Pruebas de concurrencia

Archivo: test_api_concurrencia.py.

Cantidad: 10 pruebas.

| Escenario |
|---|
| Registro concurrente de profesores duplicados |
| Registro concurrente de aprendices duplicados |
| Registro concurrente de cursos duplicados |
| Registro concurrente de inscripciones duplicadas |
| Registro concurrente de calificaciones duplicadas |
| Registro concurrente de calificaciones diferentes |
| Modificación concurrente de notas |
| Finalización concurrente de inscripciones |
| Transiciones concurrentes de estado |
| Disponibilidad del servidor después de la concurrencia |

Para los escenarios de cuatro solicitudes de registro
duplicadas se espera una creación exitosa y tres conflictos:

```text
[201, 409, 409, 409]
```

## 10. Problema de concurrencia identificado

Durante las primeras ejecuciones se detectaron
interbloqueos de MySQL al registrar profesores y aprendices
simultáneamente.

MySQL generó el siguiente error:

```text
1213 (40001): Deadlock found when trying to get lock;
try restarting transaction
```

El problema se presentó durante operaciones sobre la tabla
persona realizadas dentro de transacciones concurrentes.

Los repositorios consultaban el documento mediante
SELECT FOR UPDATE antes de insertar una persona.

Cuando diferentes transacciones intentaban registrar
simultáneamente documentos que todavía no existían,
podían producirse conflictos entre bloqueos.

La API transformaba el error de persistencia en una
respuesta HTTP 500.

Uno de los resultados obtenidos fue:

```text
Resultado esperado: [201, 409, 409, 409]
Resultado obtenido: [201, 500, 500, 500]
```

La ejecución inicial del bloque de concurrencia y
persistencia presentó tres pruebas fallidas.

## 11. Solución implementada

Se incorporó un mecanismo limitado de reintentos para
interbloqueos de MySQL.

La solución permite repetir la operación transaccional
cuando se presenta el error correspondiente, después
de finalizar la transacción fallida.

El mecanismo fue aplicado a los métodos de registro
de profesores y aprendices mediante el decorador:

```python
@reintentar_interbloqueo
```

Archivos modificados:

- persistencia/conexion.py.
- persistencia/excepciones.py.
- persistencia/repositorios/repositorio_profesores.py.
- persistencia/repositorios/repositorio_aprendices.py.

Commits asociados:

```text
1ec11d7 fix: implement bounded MySQL deadlock retries
5dfd4c3 fix: handle concurrent academic person registrations
```

La solución conserva las restricciones de integridad
y no modifica las pruebas para aceptar respuestas
HTTP 500 como resultados válidos.

## 12. Validación de la corrección

Después de implementar la solución se realizaron cinco
ejecuciones consecutivas de las pruebas de concurrencia.

| Ejecución | Pruebas | Tiempo | Resultado |
|---|---:|---:|---|
| 1 | 10 | 2.397 s | OK |
| 2 | 10 | 2.232 s | OK |
| 3 | 10 | 2.396 s | OK |
| 4 | 10 | 2.383 s | OK |
| 5 | 10 | 2.277 s | OK |

Las cinco ejecuciones finalizaron correctamente.

Esto representa 50 ejecuciones exitosas de 10 casos
de prueba diferentes.

Los resultados demuestran estabilidad en los escenarios
evaluados, sin garantizar la eliminación absoluta de
interbloqueos bajo cualquier condición de carga.

## 13. Pruebas de persistencia

Archivo: test_api_persistencia.py.

Cantidad: 15 pruebas.

Se evalúa la conservación de:

- Profesores.
- Aprendices.
- Cursos.
- Asignaciones de profesores.
- Inscripciones.
- Estados cancelados.
- Estados finalizados.
- Calificaciones.
- Modificaciones de notas.
- Promedios.
- Reportes.
- Resúmenes académicos.
- Restricciones de duplicados.
- Restricciones de calificaciones.
- Disponibilidad del servidor después del reinicio.

Estas pruebas verifican que los datos no dependen
exclusivamente de objetos almacenados en memoria.

## 14. Preparación de infraestructura

```bash
docker compose --env-file infra/.env \
    -f infra/docker-compose.yml up -d
```

Verificar el estado del contenedor:

```bash
docker compose --env-file infra/.env \
    -f infra/docker-compose.yml ps
```

## 15. Ejecución de pruebas

### Integración API MySQL

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest \
    tests.integracion.test_api_mysql \
    -v
```

### Concurrencia

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest \
    tests.integracion.test_api_concurrencia \
    -v
```

### Persistencia

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest \
    tests.integracion.test_api_persistencia \
    -v
```

### Integración completa de la API

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest \
    tests.integracion.test_api_mysql \
    tests.integracion.test_api_concurrencia \
    tests.integracion.test_api_persistencia \
    -q
```

### Regresión completa

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest discover \
    -s tests \
    -t . \
    -q
```

## 16. Resultados

| Grupo | Pruebas aprobadas |
|---|---:|
| Integración API MySQL | 30 |
| Concurrencia API | 10 |
| Persistencia API | 15 |
| Total | 55 |

Resultado de integración completa:

```text
Ran 55 tests in 12.143s

OK
```

Resultado de regresión completa:

```text
Ran 587 tests in 19.820s

OK
```

## 17. Conclusión

Las pruebas de integración comprobaron la comunicación
entre la API REST y MySQL, la persistencia de los datos
y las operaciones concurrentes evaluadas.

La detección y corrección de los interbloqueos permitió
mejorar el comportamiento del sistema frente a solicitudes
simultáneas de registro.

Las 55 pruebas de integración de la API y la regresión
completa finalizaron correctamente.