# Pruebas unitarias y funcionales de la API REST

## 1. Introducción

Las pruebas unitarias y funcionales verifican los componentes
de la API REST del Sistema de Gestión Académica.

Se utiliza unittest como herramienta de automatización y
gestores en memoria para evaluar la lógica académica sin
depender de una base de datos externa.

También se incluyen pruebas funcionales del servidor HTTP
que utilizan conexiones locales reales.

## 2. Objetivo

Comprobar el comportamiento de los componentes de la API,
las reglas de negocio, las validaciones y las respuestas
HTTP mediante escenarios automatizados.

## 3. Organización de archivos

```text
tests/
└── api_rest/
    ├── __init__.py
    ├── test_aprendices.py
    ├── test_calificaciones.py
    ├── test_cursos.py
    ├── test_enrutador.py
    ├── test_errores_http.py
    ├── test_excepciones.py
    ├── test_inscripciones.py
    ├── test_profesores.py
    ├── test_reportes.py
    ├── test_respuestas.py
    ├── test_serializadores.py
    ├── test_servidor.py
    └── test_validaciones.py
```

## 4. Infraestructura reutilizable

### 4.1. BasePruebasAPI

La clase BasePruebasAPI centraliza la preparación del
entorno de pruebas.

Sus responsabilidades incluyen:

- Crear una instancia de GestionAcademica.
- Inicializar los gestores en memoria.
- Construir el enrutador.
- Ejecutar solicitudes directamente sobre el enrutador.
- Verificar la estructura de las respuestas.

Cada prueba dispone de un entorno preparado para evitar
dependencias innecesarias entre casos.

### 4.2. BasePruebasHTTP

La clase BasePruebasHTTP amplía la infraestructura de pruebas
para realizar solicitudes HTTP reales.

Sus responsabilidades incluyen:

- Crear un servidor HTTP temporal.
- Utilizar un puerto disponible asignado automáticamente.
- Ejecutar el servidor en un hilo independiente.
- Enviar solicitudes mediante urllib.
- Interpretar las respuestas JSON.
- Verificar encabezados y códigos de estado.
- Detener el servidor al finalizar las pruebas.

## 5. Distribución de pruebas

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
| Total | 297 |

## 6. Pruebas de infraestructura

### 6.1. Enrutador

Archivo: test_enrutador.py.

Cantidad: 15 pruebas.

Evalúa el registro y resolución de rutas, los parámetros
dinámicos, los métodos HTTP y el tratamiento de solicitudes
que no corresponden a rutas disponibles.

### 6.2. Excepciones

Archivo: test_excepciones.py.

Cantidad: 12 pruebas.

Comprueba las excepciones personalizadas de la API y su
asociación con los códigos de estado HTTP correspondientes.

### 6.3. Respuestas

Archivo: test_respuestas.py.

Cantidad: 17 pruebas.

Verifica la construcción de respuestas exitosas, respuestas
de creación, respuestas de error y representación JSON.

### 6.4. Validaciones

Archivo: test_validaciones.py.

Cantidad: 43 pruebas.

Evalúa la validación de:

- Campos obligatorios y opcionales.
- Textos.
- Documentos de identificación.
- Números enteros.
- Códigos académicos.
- Calificaciones.
- Modalidades.
- Estados.
- Fechas.

### 6.5. Serializadores

Archivo: test_serializadores.py.

Cantidad: 25 pruebas.

Comprueba la transformación de las entidades académicas en
estructuras compatibles con JSON.

## 7. Pruebas de módulos académicos

### 7.1. Profesores

Archivo: test_profesores.py.

Cantidad: 15 pruebas.

Evalúa el registro, consulta, listado, validaciones,
duplicados y relaciones académicas de los profesores.

### 7.2. Aprendices

Archivo: test_aprendices.py.

Cantidad: 17 pruebas.

Comprueba el registro, consulta, listado, validaciones y
relaciones académicas de los aprendices.

### 7.3. Cursos

Archivo: test_cursos.py.

Cantidad: 22 pruebas.

Verifica las operaciones de registro, consulta, listado,
asignación de profesores y relaciones con otros módulos.

### 7.4. Inscripciones

Archivo: test_inscripciones.py.

Cantidad: 26 pruebas.

Evalúa el registro de inscripciones, duplicados, consultas,
transiciones de estado y rendimiento académico.

### 7.5. Calificaciones

Archivo: test_calificaciones.py.

Cantidad: 28 pruebas.

Comprueba el registro, consulta y modificación de notas,
validaciones y restricciones asociadas al estado de las
inscripciones.

### 7.6. Reportes

Archivo: test_reportes.py.

Cantidad: 15 pruebas.

Verifica la generación de reportes, resúmenes académicos
y consultas relacionadas con el rendimiento.

## 8. Pruebas HTTP

### 8.1. Servidor HTTP

Archivo: test_servidor.py.

Cantidad: 26 pruebas.

Comprueba el funcionamiento del servidor mediante
solicitudes HTTP reales sobre un entorno local.

### 8.2. Manejo de errores

Archivo: test_errores_http.py.

Cantidad: 36 pruebas.

Evalúa solicitudes inválidas, errores internos simulados,
formatos incorrectos y continuidad del servicio.

## 9. Códigos HTTP evaluados

| Código | Significado |
|---|---|
| 200 | Operación exitosa |
| 201 | Recurso creado |
| 400 | Solicitud incorrecta |
| 404 | Recurso no encontrado |
| 405 | Método no permitido |
| 408 | Tiempo de espera agotado |
| 409 | Conflicto |
| 413 | Contenido demasiado grande |
| 415 | Formato no soportado |
| 422 | Datos inválidos |
| 500 | Error interno |
| 503 | Servicio no disponible |

## 10. Estructura de respuestas

Las respuestas de la API utilizan una estructura uniforme.

Ejemplo de respuesta exitosa:

```json
{
    "exito": true,
    "mensaje": "Operación exitosa",
    "datos": {}
}
```

Ejemplo de respuesta de error:

```json
{
    "exito": false,
    "mensaje": "Recurso no encontrado",
    "datos": null
}
```

## 11. Correcciones realizadas

Durante la revisión se identificaron advertencias de análisis
estático relacionadas con respuestas HTTP que podían contener
un valor None.

Se incorporaron comprobaciones explícitas antes de acceder
a los elementos de dichas respuestas.

Archivos corregidos:

- tests/api_rest/test_servidor.py.
- tests/api_rest/test_errores_http.py.

Commit asociado:

```text
479291f fix: resolve optional response type errors in HTTP tests
```

Después de la corrección se ejecutaron nuevamente las
62 pruebas HTTP y la regresión existente.

Ambas ejecuciones finalizaron correctamente.

## 12. Ejecución

Ejecutar todas las pruebas de este paquete:

```bash
python3 -m unittest discover \
    -s tests/api_rest \
    -t . \
    -v
```

Ejecutar únicamente las pruebas de validaciones:

```bash
python3 -m unittest \
    tests.api_rest.test_validaciones \
    -v
```

Ejecutar las pruebas del servidor y manejo de errores:

```bash
python3 -m unittest \
    tests.api_rest.test_servidor \
    tests.api_rest.test_errores_http \
    -v
```

## 13. Resultados

| Grupo | Pruebas |
|---|---:|
| Infraestructura y componentes | 112 |
| Controladores académicos | 123 |
| Servidor HTTP y errores | 62 |
| Total | 297 |

Las 297 pruebas forman parte de la regresión completa de
587 pruebas aprobadas.

## 14. Conclusión

Las pruebas permiten verificar los componentes principales
de la API REST, sus reglas de negocio y el comportamiento
del servidor HTTP.

La infraestructura reutilizable facilita la incorporación
de nuevos casos y el mantenimiento de las pruebas.