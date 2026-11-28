# Evidencias de pruebas de la API REST

## 1. Información general

| Campo | Información |
|---|---|
| Proyecto | Sistema de Gestión Académica |
| Fase | 05 - Pruebas automatizadas API |
| Fecha de ejecución | 28 de noviembre de 2026 |
| Rama | feature/api-testing |
| Herramienta de pruebas | unittest |
| Sistema operativo | Kubuntu |
| Base de datos | MySQL 8.4 |
| Infraestructura | Docker Compose |
| Resultado final | Aprobado |

## 2. Validación de infraestructura

Comando ejecutado:

```bash
docker compose --env-file infra/.env \
    -f infra/docker-compose.yml ps
```

Resultado observado:

| Contenedor | Imagen | Estado | Puerto |
|---|---|---|---|
| academic-mysql | mysql:8.4 | healthy | 127.0.0.1:3307 |

La infraestructura se encontraba operativa durante
la ejecución de las pruebas.

## 3. Validación de sintaxis

Comando ejecutado:

```bash
python3 -m compileall -q persistencia api tests
```

Resultado:

- Compilación completada.
- No se reportaron errores de sintaxis.
- Se continuó con la ejecución de las pruebas.

## 4. Evidencia de pruebas HTTP

Comando ejecutado:

```bash
python3 -m unittest \
    tests.api_rest.test_servidor \
    tests.api_rest.test_errores_http \
    -q
```

Resultado:

```text
----------------------------------------------------------------------
Ran 62 tests

OK
```

## 5. Evidencia de regresión anterior

Después de corregir las advertencias de análisis estático
en las pruebas HTTP se obtuvo:

```text
----------------------------------------------------------------------
Ran 532 tests

OK
```

## 6. Evidencia de integración API MySQL

Comando ejecutado:

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest \
    tests.integracion.test_api_mysql \
    -v
```

Resultado:

```text
----------------------------------------------------------------------
Ran 30 tests in 5.830s

OK
```

Después de incorporar estas pruebas, la regresión registró:

```text
----------------------------------------------------------------------
Ran 562 tests in 12.221s

OK
```

## 7. Evidencia de detección de errores de concurrencia

Durante la primera ejecución del bloque de concurrencia
y persistencia se obtuvo:

```text
----------------------------------------------------------------------
Ran 25 tests in 6.577s

FAILED (failures=3)
```

Pruebas afectadas:

- test_aprendiz_duplicado_concurrente.
- test_profesor_duplicado_concurrente.
- test_servidor_operativo_despues_concurrencia.

Error identificado:

```text
1213 (40001): Deadlock found when trying to get lock;
try restarting transaction
```

La causa se relacionó con transacciones concurrentes
durante el registro de personas.

La API devolvía respuestas HTTP 500 en escenarios donde
se esperaban respuestas HTTP 409 para registros duplicados.

## 8. Evidencia de corrección

Se implementaron reintentos limitados de interbloqueos
y se aplicaron a los repositorios de profesores y
aprendices.

Commits de corrección:

```text
1ec11d7 fix: implement bounded MySQL deadlock retries
5dfd4c3 fix: handle concurrent academic person registrations
```

## 9. Evidencia de pruebas repetidas de concurrencia

### Ejecución 1

```text
Ran 10 tests in 2.397s

OK
```

### Ejecución 2

```text
Ran 10 tests in 2.232s

OK
```

### Ejecución 3

```text
Ran 10 tests in 2.396s

OK
```

### Ejecución 4

```text
Ran 10 tests in 2.383s

OK
```

### Ejecución 5

```text
Ran 10 tests in 2.277s

OK
```

Resumen:

| Indicador | Resultado |
|---|---:|
| Casos diferentes de concurrencia | 10 |
| Ejecuciones consecutivas | 5 |
| Ejecuciones individuales de casos | 50 |
| Ejecuciones exitosas | 50 |
| Fallos observados | 0 |

Las repeticiones no se contabilizan como casos diferentes
dentro de las 587 pruebas de regresión.

## 10. Evidencia de persistencia

Comando ejecutado:

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest \
    tests.integracion.test_api_persistencia \
    -v
```

Resultado:

```text
----------------------------------------------------------------------
Ran 15 tests in 4.101s

OK
```

## 11. Evidencia de integración completa API

Comando ejecutado:

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest \
    tests.integracion.test_api_mysql \
    tests.integracion.test_api_concurrencia \
    tests.integracion.test_api_persistencia \
    -q
```

Resultado:

```text
----------------------------------------------------------------------
Ran 55 tests in 12.143s

OK
```

## 12. Evidencia de regresión completa

Comando ejecutado:

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest discover \
    -s tests \
    -t . \
    -q
```

Resultado final:

```text
----------------------------------------------------------------------
Ran 587 tests in 19.820s

OK
```

Indicadores:

| Indicador | Resultado |
|---|---:|
| Pruebas ejecutadas | 587 |
| Pruebas aprobadas | 587 |
| Fallos | 0 |
| Errores de ejecución de pruebas | 0 |
| Pruebas omitidas reportadas | 0 |
| Porcentaje de aprobación | 100 % |
| Tiempo | 19.820 segundos |

El porcentaje de aprobación no equivale a cobertura
de líneas de código.

## 13. Inventario completo de pruebas

### 13.1. Pruebas originales de Python

| Archivo | Cantidad |
|---|---:|
| tests/test_aprendices.py | 12 |
| tests/test_calificaciones.py | 31 |
| tests/test_cursos.py | 24 |
| tests/test_gestion_academica.py | 45 |
| tests/test_inscripciones.py | 20 |
| tests/test_main.py | 36 |
| tests/test_personas.py | 6 |
| tests/test_profesores.py | 8 |
| Subtotal | 182 |

### 13.2. Pruebas de integración de repositorios

| Archivo | Cantidad |
|---|---:|
| test_conexion.py | 4 |
| test_persistencia.py | 9 |
| test_repositorio_aprendices.py | 5 |
| test_repositorio_calificaciones.py | 14 |
| test_repositorio_cursos.py | 7 |
| test_repositorio_inscripciones.py | 9 |
| test_repositorio_profesores.py | 5 |
| Subtotal | 53 |

### 13.3. Pruebas REST API

| Archivo | Cantidad |
|---|---:|
| test_aprendices.py | 17 |
| test_calificaciones.py | 28 |
| test_cursos.py | 22 |
| test_enrutador.py | 15 |
| test_errores_http.py | 36 |
| test_excepciones.py | 12 |
| test_inscripciones.py | 26 |
| test_profesores.py | 15 |
| test_reportes.py | 15 |
| test_respuestas.py | 17 |
| test_serializadores.py | 25 |
| test_servidor.py | 26 |
| test_validaciones.py | 43 |
| Subtotal | 297 |

### 13.4. Pruebas de integración API

| Archivo | Cantidad |
|---|---:|
| test_api_mysql.py | 30 |
| test_api_concurrencia.py | 10 |
| test_api_persistencia.py | 15 |
| Subtotal | 55 |

## 14. Consolidado general

| Categoría | Cantidad |
|---|---:|
| Python y lógica de negocio | 182 |
| Integración de repositorios | 53 |
| REST API | 297 |
| Integración API MySQL | 30 |
| Concurrencia API | 10 |
| Persistencia API | 15 |
| Total | 587 |

Se identificaron 31 archivos con métodos de prueba.

La fase 5 incorporó 352 casos de prueba relacionados
con la API REST.

## 15. Interpretación de mensajes de error

Durante la regresión completa aparecen mensajes como:

- Error inesperado de la API.
- Error de persistencia.
- Error al serializar la respuesta.
- Error de conexión con MySQL.
- RuntimeError: Error simulado.

Estos mensajes corresponden a escenarios controlados
de las pruebas de manejo de errores HTTP.

Su aparición permite comprobar que el servidor procesa
excepciones y mantiene respuestas controladas.

El resultado final de unittest fue OK.

Estos mensajes deben distinguirse de los interbloqueos
reales detectados inicialmente, los cuales sí provocaron
tres pruebas fallidas antes de la corrección.

## 16. Evidencia de control de versiones

Commits registrados antes de completar la documentación:

| Commit | Descripción |
|---|---|
| bfb6954 | test: validate academic API reports and relationships |
| 4ac5a41 | fix: standardize integration test imports |
| c61098e | test: add automated HTTP server tests |
| bbd269d | test: verify HTTP errors and server resilience |
| 479291f | fix: resolve optional response type errors in HTTP tests |
| 21cb2bb | test: integrate REST API with MySQL database |
| 1ec11d7 | fix: implement bounded MySQL deadlock retries |
| 5dfd4c3 | fix: handle concurrent academic person registrations |
| 781f4c7 | test: verify concurrent REST API operations |
| a50c972 | test: verify REST API data persistence |

El último envío registrado al repositorio remoto fue:

```text
479291f..a50c972 feature/api-testing -> feature/api-testing
```

La rama local quedó sincronizada con origin/feature/api-testing.

## 17. Validación Git

Comando ejecutado:

```bash
git diff --check
```

La validación de los cambios rastreados finalizó sin
reportar errores de formato.

Antes de completar la documentación, los únicos archivos
pendientes de seguimiento correspondían a docs/fase-05/.

## 18. Criterios de aceptación

| Criterio | Resultado |
|---|---|
| Validación de sintaxis | Aprobado |
| Pruebas REST API | Aprobado |
| Pruebas HTTP | Aprobado |
| Integración MySQL | Aprobado |
| Concurrencia evaluada | Aprobado |
| Persistencia evaluada | Aprobado |
| Aislamiento de pruebas | Aprobado |
| Manejo de errores | Aprobado |
| Regresión completa | Aprobado |
| Publicación de código en GitHub | Aprobado |

## 19. Limitaciones de la evidencia

Los resultados corresponden al entorno local de desarrollo
y a los escenarios automatizados implementados.

No se presenta una medición de cobertura de código ni
una certificación de rendimiento bajo carga de producción.

Los tiempos de ejecución pueden variar dependiendo de
los recursos disponibles y del estado de la infraestructura.

## 20. Conclusión

La fase 5 permitió verificar el funcionamiento de la
API REST y su integración con la base de datos MySQL.

Durante el proceso se detectaron y corrigieron problemas
de concurrencia en el registro de profesores y aprendices.

La validación final registró 587 pruebas automatizadas
aprobadas, sin fallos ni errores reportados por unittest.

Los resultados proporcionan evidencia del cumplimiento
de los criterios de aceptación evaluados.