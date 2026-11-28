# Documentación de endpoints REST

## 1. Información general

| Propiedad | Valor |
|---|---|
| Servicio | Sistema de Gestión Académica |
| Versión de rutas | v1 |
| Protocolo | HTTP |
| Formato | JSON |
| Host predeterminado | 127.0.0.1 |
| Puerto predeterminado | 8000 |
| Endpoints | 34 |

URL base:

```text
http://127.0.0.1:8000/api/v1
```

Todas las rutas de las siguientes tablas son relativas a esta URL.

## 2. Métodos HTTP

| Método | Cantidad |
|---|---:|
| GET | 26 |
| POST | 5 |
| PUT | 1 |
| PATCH | 2 |
| Total | 34 |

## 3. Salud del servidor

| N.º | Método | Ruta | Éxito |
|---:|---|---|---:|
| 1 | GET | /salud | 200 |

Permite comprobar que el servidor HTTP se encuentra operativo.

## 4. Profesores

| N.º | Método | Ruta | Éxito |
|---:|---|---|---:|
| 2 | GET | /profesores | 200 |
| 3 | POST | /profesores | 201 |
| 4 | GET | /profesores/{documento} | 200 |
| 5 | GET | /profesores/{documento}/cursos | 200 |
| 6 | GET | /profesores/{documento}/aprendices | 200 |

### Registrar profesor

POST /profesores

```json
{
    "nombre": "Profesor de ejemplo",
    "documento": 1000000001,
    "edad": 35,
    "profesion": "Ingeniero",
    "codigo": 1001,
    "especialidad": "Python"
}
```

### Consultar profesor

```http
GET /api/v1/profesores/1000000001
```

### Consultar cursos asignados

```http
GET /api/v1/profesores/1000000001/cursos
```

### Consultar aprendices por profesor

```http
GET /api/v1/profesores/1000000001/aprendices
```

## 5. Aprendices

| N.º | Método | Ruta | Éxito |
|---:|---|---|---:|
| 7 | GET | /aprendices | 200 |
| 8 | POST | /aprendices | 201 |
| 9 | GET | /aprendices/{documento} | 200 |
| 10 | GET | /aprendices/{documento}/cursos | 200 |
| 11 | GET | /aprendices/{documento}/inscripciones | 200 |
| 12 | GET | /aprendices/{documento}/calificaciones | 200 |
| 13 | GET | /aprendices/{documento}/rendimiento | 200 |

### Registrar aprendiz

POST /aprendices

```json
{
    "nombre": "Aprendiz de ejemplo",
    "documento": 1000000002,
    "edad": 22,
    "telefono": "3001234567",
    "correo": "aprendiz@example.com",
    "direccion": "Dirección de ejemplo"
}
```

### Consultar rendimiento

```http
GET /api/v1/aprendices/1000000002/rendimiento
```

## 6. Cursos

| N.º | Método | Ruta | Éxito |
|---:|---|---|---:|
| 14 | GET | /cursos | 200 |
| 15 | POST | /cursos | 201 |
| 16 | GET | /cursos/{codigo} | 200 |
| 17 | PUT | /cursos/{codigo}/profesor | 200 |
| 18 | GET | /cursos/{codigo}/aprendices | 200 |
| 19 | GET | /cursos/{codigo}/inscripciones | 200 |
| 20 | GET | /cursos/{codigo}/calificaciones | 200 |
| 21 | GET | /cursos/{codigo}/rendimiento | 200 |

### Registrar curso

POST /cursos

```json
{
    "codigo": "CUR-001",
    "nombre": "Programación en Python",
    "descripcion": "Fundamentos de programación",
    "duracion_horas": 48,
    "modalidad": "complementaria"
}
```

### Asignar profesor

PUT /cursos/CUR-001/profesor

```json
{
    "documento": 1000000001
}
```

### Modalidades admitidas

- titulada
- complementaria

## 7. Inscripciones

| N.º | Método | Ruta | Éxito |
|---:|---|---|---:|
| 22 | GET | /inscripciones | 200 |
| 23 | POST | /inscripciones | 201 |
| 24 | GET | /inscripciones/{codigo} | 200 |
| 25 | PATCH | /inscripciones/{codigo}/estado | 200 |
| 26 | GET | /inscripciones/{codigo}/calificaciones | 200 |
| 27 | GET | /inscripciones/{codigo}/rendimiento | 200 |
| 28 | GET | /inscripciones/{codigo}/promedio | 200 |

### Registrar inscripción

POST /inscripciones

```json
{
    "codigo": "INS-001",
    "documento_aprendiz": 1000000002,
    "codigo_curso": "CUR-001"
}
```

El aprendiz y el curso deben existir previamente.

### Finalizar inscripción

PATCH /inscripciones/INS-001/estado

```json
{
    "estado": "Finalizada"
}
```

### Cancelar inscripción

PATCH /inscripciones/INS-001/estado

```json
{
    "estado": "Cancelada"
}
```

### Estados administrativos

| Estado | Descripción |
|---|---|
| Activa | Inscripción vigente |
| Cancelada | Inscripción cancelada |
| Finalizada | Inscripción finalizada |

La modificación de estado admite Cancelada o Finalizada.

Las transiciones se realizan desde una inscripción activa.

## 8. Calificaciones

| N.º | Método | Ruta | Éxito |
|---:|---|---|---:|
| 29 | GET | /calificaciones | 200 |
| 30 | POST | /calificaciones | 201 |
| 31 | GET | /calificaciones/{codigo} | 200 |
| 32 | PATCH | /calificaciones/{codigo} | 200 |

### Registrar calificación

POST /calificaciones

```json
{
    "codigo": "NOT-001",
    "codigo_inscripcion": "INS-001",
    "nota": 4.5
}
```

### Modificar calificación

PATCH /calificaciones/NOT-001

```json
{
    "nota": 4.8
}
```

### Reglas académicas

- Las notas deben ser numéricas.
- El rango permitido es de 0.0 a 5.0.
- Se admiten máximo dos decimales.
- Se requieren mínimo tres calificaciones para calcular el promedio definitivo.
- La nota mínima de aprobación es 3.0.
- Las inscripciones no activas restringen el registro y modificación de notas.

## 9. Reportes

| N.º | Método | Ruta | Éxito |
|---:|---|---|---:|
| 33 | GET | /reportes/resumen | 200 |
| 34 | GET | /reportes/calificaciones | 200 |

El resumen académico contiene las cantidades de profesores, aprendices, cursos, inscripciones y calificaciones.

Ejemplo ilustrativo del contenido de datos:

```json
{
    "profesores": 1,
    "aprendices": 1,
    "cursos": 1,
    "inscripciones": 1,
    "calificaciones": 3
}
```

## 10. Parámetros de identificación

### Documento

- Número entero positivo.
- Máximo 20 dígitos.
- Se utiliza para identificar profesores y aprendices.

### Código de recurso

- Cadena de texto.
- Máximo 30 caracteres.
- Admite letras ASCII, números, guiones y guiones bajos.

El código numérico del profesor es diferente del código textual utilizado para identificar cursos, inscripciones y calificaciones.

### Fechas

El validador de fechas utiliza el formato:

```text
AAAA-MM-DD
```

Las fechas serializadas utilizan el formato ISO.

## 11. Estructuras serializadas

| Entidad | Campos |
|---|---|
| Profesor | nombre, documento, edad, profesion, codigo, especialidad |
| Aprendiz | nombre, documento, edad, telefono, correo, direccion |
| Curso | codigo, nombre, descripcion, duracion_horas, modalidad, profesor |
| Inscripcion | codigo, aprendiz, curso, fecha_inscripcion, estado |
| Calificacion | codigo, inscripcion, nota, fecha |

Los recursos relacionados se representan mediante objetos JSON anidados.

Un curso sin profesor asignado contiene profesor con valor null.

## 12. Ejemplo de curso serializado

Ejemplo ilustrativo del contenido de datos:

```json
{
    "codigo": "CUR-001",
    "nombre": "Programación en Python",
    "descripcion": "Fundamentos de programación",
    "duracion_horas": 48,
    "modalidad": "complementaria",
    "profesor": null
}
```

## 13. Formato general de respuesta

### Respuesta exitosa

Ejemplo ilustrativo:

```json
{
    "exito": true,
    "mensaje": "Operación exitosa",
    "datos": {}
}
```

### Respuesta de error

Ejemplo ilustrativo:

```json
{
    "exito": false,
    "mensaje": "Recurso no encontrado",
    "datos": null
}
```

Los mensajes específicos dependen de la operación ejecutada.

## 14. Códigos HTTP

| Código | Significado | Situación |
|---:|---|---|
| 200 | OK | Consulta o modificación exitosa |
| 201 | Created | Registro exitoso |
| 400 | Bad Request | Solicitud o JSON inválido |
| 404 | Not Found | Ruta o recurso inexistente |
| 405 | Method Not Allowed | Método no permitido |
| 408 | Request Timeout | Tiempo de espera agotado |
| 409 | Conflict | Conflicto de datos o estado |
| 413 | Content Too Large | Contenido superior al límite |
| 415 | Unsupported Media Type | Formato no soportado |
| 422 | Unprocessable Content | Datos inválidos |
| 500 | Internal Server Error | Error interno |
| 503 | Service Unavailable | MySQL no disponible |

Los códigos anteriores representan comportamientos contemplados por la implementación.

La comprobación integral de la fase 4 verificó específicamente los códigos 200, 201, 404, 405, 409 y 422.

## 15. Encabezados HTTP

### Solicitudes con contenido

```http
Content-Type: application/json
```

### Respuestas

```http
Content-Type: application/json; charset=utf-8
Cache-Control: no-store
X-Content-Type-Options: nosniff
Connection: close
```

El servidor incluye Content-Length.

Las respuestas de método no permitido incluyen Allow.

## 16. Restricciones

- Las solicitudes POST, PUT y PATCH requieren un objeto JSON.
- No se admiten campos JSON duplicados.
- El tamaño máximo del contenido es de 1 MiB.
- No se admite Transfer-Encoding.
- No se implementan endpoints DELETE.
- No se dispone de autenticación ni paginación.

## 17. Resumen de endpoints

| Módulo | Cantidad |
|---|---:|
| Salud | 1 |
| Profesores | 5 |
| Aprendices | 7 |
| Cursos | 8 |
| Inscripciones | 7 |
| Calificaciones | 4 |
| Reportes | 2 |
| Total | 34 |

Los 34 endpoints fueron ejercitados durante la comprobación integral HTTP con MySQL de la fase 4.