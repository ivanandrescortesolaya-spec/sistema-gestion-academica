# Estrategia de pruebas de la API REST

## 1. Introducción

La fase 5 del Sistema de Gestión Académica tiene como propósito
verificar el funcionamiento, la integridad, la estabilidad y la
persistencia de la API REST mediante pruebas automatizadas.

La estrategia permite comprobar que la incorporación de la API
no afecta las funcionalidades implementadas durante las fases
anteriores del proyecto.

## 2. Objetivo general

Validar el funcionamiento de la API REST y su integración con
MySQL mediante pruebas unitarias, funcionales, de integración,
concurrencia, persistencia y regresión.

## 3. Objetivos específicos

- Verificar las reglas de negocio del sistema académico.
- Validar las solicitudes y respuestas HTTP.
- Comprobar el funcionamiento de los controladores.
- Verificar el enrutamiento de las solicitudes.
- Validar la serialización de entidades.
- Comprobar el manejo de excepciones.
- Verificar la integración entre Python y MySQL.
- Evaluar operaciones concurrentes.
- Comprobar la persistencia de los registros.
- Detectar regresiones en funcionalidades existentes.
- Garantizar el aislamiento de la base de datos de pruebas.

## 4. Alcance

La estrategia contempla los siguientes módulos:

- Profesores.
- Aprendices.
- Cursos.
- Inscripciones.
- Calificaciones.
- Reportes académicos.
- Enrutador.
- Validaciones.
- Serializadores.
- Respuestas HTTP.
- Excepciones.
- Servidor HTTP.
- Repositorios MySQL.

La API cuenta con 34 rutas registradas bajo el prefijo `/api/v1`.

## 5. Herramientas utilizadas

| Herramienta | Propósito |
|---|---|
| Python 3 | Lenguaje de programación |
| unittest | Automatización de pruebas |
| urllib | Solicitudes HTTP |
| threading | Ejecución del servidor y operaciones concurrentes |
| MySQL 8.4 | Persistencia relacional |
| MySQL Connector/Python | Comunicación con MySQL |
| Docker | Ejecución del motor de base de datos |
| Docker Compose | Administración de infraestructura |
| Git | Control de versiones |
| GitHub | Repositorio remoto |
| Visual Studio Code | Desarrollo y revisión de código |

## 6. Niveles de pruebas

### 6.1. Pruebas unitarias

Evalúan componentes individuales y reglas de negocio sin
depender de una conexión real con MySQL.

Incluyen validaciones, serializadores, excepciones, respuestas
y enrutamiento.

### 6.2. Pruebas funcionales

Comprueban las operaciones de los controladores y las
funcionalidades académicas utilizando gestores en memoria.

### 6.3. Pruebas HTTP

Verifican el comportamiento del servidor mediante solicitudes
HTTP reales realizadas sobre la interfaz local.

Se comprueban códigos de estado, encabezados, contenido JSON,
manejo de errores y continuidad del servicio.

### 6.4. Pruebas de integración

Comprueban la comunicación entre la API, la lógica de negocio,
los repositorios y la base de datos MySQL.

### 6.5. Pruebas de concurrencia

Evalúan el comportamiento del sistema cuando diferentes
solicitudes intentan ejecutar operaciones simultáneamente.

Se verifican registros duplicados, calificaciones, inscripciones
y transiciones de estado.

### 6.6. Pruebas de persistencia

Comprueban que los datos permanecen almacenados después de
reiniciar el servidor HTTP y reconstruir los componentes de
acceso a la base de datos.

### 6.7. Pruebas de regresión

Ejecutan el conjunto completo de pruebas para detectar
afectaciones sobre funcionalidades previamente implementadas.

## 7. Arquitectura de pruebas

```text
Pruebas automatizadas
        |
        v
Servidor HTTP / Enrutador
        |
        v
Controladores REST
        |
        v
GestionAcademica
        |
        +----------------------+
        |                      |
        v                      v
Gestores en memoria      Repositorios MySQL
                               |
                               v
                       Base de datos de pruebas
```

## 8. Aislamiento del entorno

Las pruebas de integración utilizan exclusivamente:

- Base de datos: sistema_gestion_academica_test.
- Usuario: academic_test_user.
- Motor: MySQL 8.4.
- Contenedor: academic-mysql.
- Puerto local: 3307.

La clase BaseIntegracion verifica la identidad de la base de
datos y del usuario antes de ejecutar las pruebas.

Los registros de prueba utilizan identificadores generados
dinámicamente y procedimientos de limpieza.

Las credenciales se administran mediante variables de entorno
y no deben publicarse en el repositorio.

## 9. Distribución de pruebas

| Categoría | Cantidad |
|---|---:|
| Python y lógica de negocio | 182 |
| Integración de repositorios MySQL | 53 |
| Pruebas REST API en memoria y HTTP | 297 |
| Integración API MySQL | 30 |
| Concurrencia API | 10 |
| Persistencia API | 15 |
| Total | 587 |

La fase 5 incorpora 352 pruebas relacionadas con la API REST,
además de conservar las 235 pruebas de las fases anteriores.

## 10. Criterios de aceptación

- Todas las pruebas automatizadas deben aprobarse.
- Las solicitudes válidas deben obtener respuestas correctas.
- Las solicitudes inválidas deben rechazarse.
- Los registros duplicados deben generar conflictos.
- Las calificaciones deben respetar las reglas académicas.
- Las operaciones concurrentes evaluadas deben conservar
  la integridad de los registros.
- Los datos deben conservarse después del reinicio de la API.
- Las pruebas deben utilizar la base de datos de pruebas.
- Los errores internos no deben exponer detalles sensibles
  mediante las respuestas HTTP.
- No deben introducirse regresiones.

## 11. Ejecución general

Desde la raíz del proyecto:

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest discover \
    -s tests \
    -t . \
    -q
```

## 12. Limitaciones

La aprobación de las pruebas no representa una medición de
cobertura de líneas de código.

Las pruebas de concurrencia verifican escenarios definidos,
pero no garantizan la ausencia de interbloqueos bajo cualquier
nivel de carga.

No se realizaron pruebas exhaustivas de rendimiento, seguridad
ofensiva o escalabilidad en producción.

## 13. Conclusión

La estrategia permite verificar los principales componentes
del sistema académico y detectar problemas de integración,
concurrencia y persistencia.

La regresión completa registró 587 pruebas aprobadas sin
fallos, proporcionando evidencia del funcionamiento del
sistema dentro de los escenarios evaluados.