
# Diccionario de datos

## Fase 1: Análisis y diseño de base de datos

**Proyecto:** Sistema de Gestión Académica  
**Documento:** Diccionario de datos  
**Versión:** 1.0

---

## 1. Introducción

El diccionario de datos describe detalladamente la estructura,
características, restricciones y significado de los atributos
que conforman la base de datos del Sistema de Gestión Académica.

Su elaboración se fundamenta en el análisis del aplicativo
existente, las reglas de negocio, el modelo entidad-relación
y el modelo relacional.

Este documento servirá como referencia para la implementación
de la base de datos, el desarrollo de la capa de persistencia,
la construcción de la API REST y las pruebas de integridad.

## 2. Objetivos

### 2.1. Objetivo general

Documentar los atributos de las tablas del Sistema de Gestión
Académica para garantizar una interpretación uniforme de la
información y facilitar su implementación.

### 2.2. Objetivos específicos

- Identificar cada tabla y sus atributos.
- Describir el significado de cada atributo.
- Establecer los tipos de datos.
- Documentar las longitudes y capacidades.
- Identificar atributos obligatorios y opcionales.
- Documentar las claves primarias y foráneas.
- Especificar las restricciones de integridad.
- Identificar los valores predeterminados.
- Proporcionar ejemplos de valores válidos.
- Facilitar las validaciones de la aplicación.

## 3. Documentos de referencia

- [Análisis del aplicativo](analisis-aplicativo.md).
- [Reglas de negocio](reglas-negocio.md).
- [Modelo entidad-relación](modelo-entidad-relacion.md).
- [Modelo relacional](modelo-relacional.md).

## 4. Convenciones

### 4.1. Abreviaturas

| Abreviatura | Significado |
|---|---|
| PK | Clave primaria. |
| FK | Clave foránea. |
| UK | Restricción de unicidad. |
| NN | NOT NULL. |
| AI | AUTO_INCREMENT. |
| CK | Restricción CHECK. |
| NULL | Ausencia de valor. |
| DEFAULT | Valor predeterminado. |
| N/A | No aplica. |

### 4.2. Convenciones de nomenclatura

- Los nombres de tablas se escriben en singular.
- Los nombres se escriben en minúsculas.
- Las palabras se separan mediante guion bajo.
- Los identificadores internos utilizan el prefijo id_.
- Los nombres no contienen espacios ni tildes.

### 4.3. Interpretación de tamaños

Las longitudes de VARCHAR representan cantidades máximas
de caracteres.

El tamaño de INT corresponde a cuatro bytes de almacenamiento.

DECIMAL(3,2) representa una precisión total de tres dígitos,
de los cuales dos corresponden a la parte decimal.

TEXT permite almacenar hasta 65535 bytes, por lo que su
capacidad en caracteres depende de la codificación utilizada.

Los tipos documentados son compatibles con MySQL 8.4,
cuya selección definitiva se justificará posteriormente.

## 5. Inventario de tablas

| Tabla | Descripción | Columnas |
|---|---|---:|
| persona | Información personal común. | 4 |
| profesor | Información profesional. | 4 |
| aprendiz | Información de contacto. | 4 |
| modalidad | Catálogo de modalidades. | 3 |
| curso | Información de los cursos. | 7 |
| inscripcion | Asociación entre aprendices y cursos. | 6 |
| calificacion | Notas académicas. | 5 |
| **Total** | | **33** |

## 6. Tabla persona

### 6.1. Descripción general

Almacena los datos personales comunes de profesores
y aprendices.

Permite centralizar la información de una persona que
puede desempeñar uno o ambos roles académicos.

### 6.2. Diccionario de atributos

| Atributo | Descripción | Tipo | Tamaño | Nulo | Restricciones | Ejemplo |
|---|---|---|---|---|---|---|
| id_persona | Identificador interno de la persona. | INT UNSIGNED | 4 bytes | No | PK, AI, NN | 1 |
| documento | Documento de identificación. | VARCHAR(20) | 20 caracteres | No | UK, NN, CK | 0012345678 |
| nombre | Nombre completo de la persona. | VARCHAR(150) | 150 caracteres | No | NN, CK | Ana Torres |
| edad | Edad expresada en años. | INT UNSIGNED | 4 bytes | No | NN, CK | 22 |

### 6.3. Validaciones por atributo

#### id_persona

- Generado automáticamente por la base de datos.
- Identifica de manera única a cada persona.
- No admite valores nulos.
- No debe modificarse después de su generación.

#### documento

- Debe contener entre 1 y 20 dígitos.
- Debe ser único globalmente.
- No admite letras ni espacios internos.
- No puede estar compuesto exclusivamente por ceros.
- Se almacena como texto para conservar ceros iniciales.
- Se eliminan los espacios externos antes de almacenarlo.

#### nombre

- Debe contener entre 1 y 150 caracteres.
- No admite cadenas vacías.
- Permite caracteres Unicode.
- Se eliminan los espacios externos.

#### edad

- Debe ser un número entero no negativo.
- No admite valores decimales.
- No admite valores booleanos desde Python.
- No se actualiza automáticamente con el paso del tiempo.

### 6.4. Claves

- Clave primaria: id_persona.
- Clave alternativa: documento.
- Claves foráneas: ninguna.

### 6.5. Valores predeterminados

| Atributo | Valor predeterminado |
|---|---|
| id_persona | Generación automática. |
| documento | Ninguno. |
| nombre | Ninguno. |
| edad | Ninguno. |

### 6.6. Ejemplo de registro

| id_persona | documento | nombre | edad |
|---:|---|---|---:|
| 1 | 0012345678 | Ana Torres | 22 |
| 2 | 0098765432 | Carlos Pérez | 35 |

Los registros utilizados en este documento son ficticios.

## 7. Tabla profesor

### 7.1. Descripción general

Almacena los atributos específicos de las personas que
desempeñan el rol de profesor.

Utiliza una clave primaria compartida con persona.

### 7.2. Diccionario de atributos

| Atributo | Descripción | Tipo | Tamaño | Nulo | Restricciones | Ejemplo |
|---|---|---|---|---|---|---|
| id_persona | Identificador de la persona asociada. | INT UNSIGNED | 4 bytes | No | PK, FK, NN | 2 |
| codigo | Código funcional del profesor. | INT UNSIGNED | 4 bytes | No | UK, NN, CK | 1001 |
| profesion | Profesión del profesor. | VARCHAR(100) | 100 caracteres | No | NN, CK | Ingeniero de sistemas |
| especialidad | Área de especialización. | VARCHAR(100) | 100 caracteres | No | NN, CK | Bases de datos |

### 7.3. Validaciones por atributo

#### id_persona

- Debe corresponder a una persona existente.
- No utiliza AUTO_INCREMENT.
- Solo puede existir una vez en la tabla profesor.
- Una misma persona puede tener también el rol de aprendiz.

#### codigo

- Debe ser un número entero positivo.
- Debe ser único entre los profesores.
- No admite valores decimales.
- No admite valores booleanos desde Python.

#### profesion

- Debe contener entre 1 y 100 caracteres.
- No admite cadenas vacías.
- Se eliminan los espacios externos.

#### especialidad

- Debe contener entre 1 y 100 caracteres.
- No admite cadenas vacías.
- Se eliminan los espacios externos.

### 7.4. Claves

- Clave primaria: id_persona.
- Clave alternativa: codigo.
- Clave foránea: id_persona referencia persona.id_persona.

### 7.5. Valores predeterminados

Ninguno de los atributos posee un valor predeterminado.

El identificador se obtiene de una persona previamente
registrada o creada dentro de la misma transacción.

### 7.6. Ejemplo de registro

| id_persona | codigo | profesion | especialidad |
|---:|---:|---|---|
| 2 | 1001 | Ingeniero de sistemas | Bases de datos |

## 8. Tabla aprendiz

### 8.1. Descripción general

Almacena los datos de contacto de las personas que
desempeñan el rol de aprendiz.

Utiliza una clave primaria compartida con persona.

### 8.2. Diccionario de atributos

| Atributo | Descripción | Tipo | Tamaño | Nulo | Restricciones | Ejemplo |
|---|---|---|---|---|---|---|
| id_persona | Identificador de la persona asociada. | INT UNSIGNED | 4 bytes | No | PK, FK, NN | 1 |
| telefono | Número telefónico de contacto. | VARCHAR(20) | 20 caracteres | No | NN, CK | +573000000001 |
| correo | Dirección de correo electrónico. | VARCHAR(254) | 254 caracteres | No | NN, CK | ana@example.com |
| direccion | Dirección de residencia o contacto. | VARCHAR(200) | 200 caracteres | No | NN, CK | Calle 10 # 20-30 |

### 8.3. Validaciones por atributo

#### id_persona

- Debe corresponder a una persona existente.
- No utiliza AUTO_INCREMENT.
- Solo puede existir una vez en la tabla aprendiz.

#### telefono

- Debe contener entre 1 y 20 caracteres.
- Debe contener dígitos.
- Puede incluir un único signo + al inicio.
- No admite letras.
- No admite cadenas vacías.
- No requiere unicidad.

La validación detallada se realizará en la aplicación.

#### correo

- Debe contener entre 1 y 254 caracteres.
- Debe contener una estructura válida de correo electrónico.
- Debe poseer una parte local y un dominio.
- No admite cadenas vacías.
- No requiere unicidad.

La validación de formato no garantiza que la dirección
de correo exista o se encuentre activa.

#### direccion

- Debe contener entre 1 y 200 caracteres.
- No admite cadenas vacías.
- Permite caracteres Unicode.
- Se eliminan los espacios externos.

### 8.4. Claves

- Clave primaria: id_persona.
- Clave foránea: id_persona referencia persona.id_persona.
- Claves alternativas: ninguna.

### 8.5. Valores predeterminados

Ninguno de los atributos posee un valor predeterminado.

### 8.6. Ejemplo de registro

| id_persona | telefono | correo | direccion |
|---:|---|---|---|
| 1 | +573000000001 | ana@example.com | Calle 10 # 20-30 |

## 9. Tabla modalidad

### 9.1. Descripción general

Almacena el catálogo de modalidades de formación.

Permite centralizar los tipos de formación disponibles
y evitar la repetición de sus descripciones en los cursos.

### 9.2. Diccionario de atributos

| Atributo | Descripción | Tipo | Tamaño | Nulo | Restricciones | Ejemplo |
|---|---|---|---|---|---|---|
| id_modalidad | Identificador interno de la modalidad. | INT UNSIGNED | 4 bytes | No | PK, AI, NN | 1 |
| nombre | Nombre de la modalidad. | VARCHAR(50) | 50 caracteres | No | UK, NN, CK | titulada |
| descripcion | Descripción de la modalidad. | VARCHAR(255) | 255 caracteres | Sí | Opcional | Formación titulada |

### 9.3. Validaciones por atributo

#### id_modalidad

- Generado automáticamente.
- Debe identificar una modalidad única.
- No debe modificarse.

#### nombre

- Debe contener entre 1 y 50 caracteres.
- Debe ser único.
- No admite cadenas vacías.
- Se normaliza a minúsculas.
- Se eliminan los espacios externos.

#### descripcion

- Admite hasta 255 caracteres.
- Puede contener NULL.
- Permite ampliar la información de la modalidad.
- No participa en la identificación del registro.

### 9.4. Claves

- Clave primaria: id_modalidad.
- Clave alternativa: nombre.
- Claves foráneas: ninguna.

### 9.5. Valores predeterminados

| Atributo | Valor predeterminado |
|---|---|
| id_modalidad | Generación automática. |
| nombre | Ninguno. |
| descripcion | NULL. |

### 9.6. Datos iniciales del catálogo

| id_modalidad | nombre | descripcion |
|---:|---|---|
| 1 | titulada | Formación correspondiente a programas titulados. |
| 2 | complementaria | Formación orientada al fortalecimiento de competencias. |

Los identificadores presentados son los valores iniciales
propuestos para el catálogo.

La incorporación de modalidades adicionales requerirá
respetar las reglas de negocio de la institución.

## 10. Tabla curso

### 10.1. Descripción general

Almacena la información de los cursos ofrecidos por
la institución.

Cada curso pertenece a una modalidad y puede tener
un profesor responsable.

### 10.2. Diccionario de atributos

| Atributo | Descripción | Tipo | Tamaño | Nulo | Restricciones | Ejemplo |
|---|---|---|---|---|---|---|
| id_curso | Identificador interno del curso. | INT UNSIGNED | 4 bytes | No | PK, AI, NN | 1 |
| codigo | Código funcional del curso. | VARCHAR(30) | 30 caracteres | No | UK, NN, CK | CUR-001 |
| nombre | Nombre del curso. | VARCHAR(150) | 150 caracteres | No | NN, CK | Programación Python |
| descripcion | Descripción del contenido del curso. | TEXT | 65535 bytes máximo | No | NN, CK | Fundamentos de Python |
| duracion_horas | Duración total en horas. | INT UNSIGNED | 4 bytes | No | NN, CK | 48 |
| id_modalidad | Modalidad asociada al curso. | INT UNSIGNED | 4 bytes | No | FK, NN | 2 |
| id_profesor | Profesor responsable del curso. | INT UNSIGNED | 4 bytes | Sí | FK | 2 |

### 10.3. Validaciones por atributo

#### id_curso

- Generado automáticamente.
- Debe identificar un curso único.
- No debe modificarse.

#### codigo

- Debe contener entre 1 y 30 caracteres.
- Debe ser único.
- No admite cadenas vacías.
- Se eliminan los espacios externos.
- Distingue mayúsculas y minúsculas.

#### nombre

- Debe contener entre 1 y 150 caracteres.
- No admite cadenas vacías.
- No requiere unicidad.

#### descripcion

- Debe contener información no vacía.
- Permite almacenar descripciones extensas.
- Su capacidad depende de la codificación utilizada.

#### duracion_horas

- Debe ser un número entero positivo.
- No admite cero.
- No admite números negativos.
- No admite valores decimales ni booleanos desde Python.

#### id_modalidad

- Debe corresponder a una modalidad existente.
- No admite valores nulos.
- Todo curso debe pertenecer a una modalidad.

#### id_profesor

- Debe corresponder a un profesor existente cuando
  contiene un valor.
- Admite NULL.
- Representa al profesor responsable.
- Un curso puede tener como máximo un profesor responsable.
- Un profesor puede estar asociado a varios cursos.

### 10.4. Claves

- Clave primaria: id_curso.
- Clave alternativa: codigo.
- Clave foránea: id_modalidad referencia modalidad.id_modalidad.
- Clave foránea: id_profesor referencia profesor.id_persona.

### 10.5. Valores predeterminados

| Atributo | Valor predeterminado |
|---|---|
| id_curso | Generación automática. |
| codigo | Ninguno. |
| nombre | Ninguno. |
| descripcion | Ninguno. |
| duracion_horas | Ninguno. |
| id_modalidad | Ninguno. |
| id_profesor | NULL. |

### 10.6. Ejemplo de registros

| id_curso | codigo | nombre | descripcion | duracion_horas | id_modalidad | id_profesor |
|---:|---|---|---|---:|---:|---|
| 1 | CUR-001 | Programación Python | Fundamentos de Python | 48 | 2 | 2 |
| 2 | CUR-002 | Desarrollo de software | Formación en desarrollo | 2200 | 1 | NULL |

## 11. Tabla inscripcion

### 11.1. Descripción general

Representa la asociación entre un aprendiz y un curso.

Permite resolver la relación muchos a muchos y almacenar
la fecha y el estado administrativo de la inscripción.

### 11.2. Diccionario de atributos

| Atributo | Descripción | Tipo | Tamaño | Nulo | Restricciones | Ejemplo |
|---|---|---|---|---|---|---|
| id_inscripcion | Identificador interno de la inscripción. | INT UNSIGNED | 4 bytes | No | PK, AI, NN | 1 |
| codigo | Código funcional de la inscripción. | VARCHAR(30) | 30 caracteres | No | UK, NN, CK | INS-001 |
| id_aprendiz | Aprendiz asociado. | INT UNSIGNED | 4 bytes | No | FK, NN, UK compuesta | 1 |
| id_curso | Curso asociado. | INT UNSIGNED | 4 bytes | No | FK, NN, UK compuesta | 1 |
| fecha_inscripcion | Fecha original de inscripción. | DATE | 3 bytes | No | NN, DEFAULT | 2026-11-28 |
| estado | Estado administrativo de la inscripción. | VARCHAR(15) | 15 caracteres | No | NN, CK, DEFAULT | Activa |

### 11.3. Validaciones por atributo

#### id_inscripcion

- Generado automáticamente.
- Identifica una inscripción única.
- No debe modificarse.

#### codigo

- Debe contener entre 1 y 30 caracteres.
- Debe ser único.
- No admite cadenas vacías.
- Distingue mayúsculas y minúsculas.
- Se eliminan los espacios externos.

#### id_aprendiz

- Debe corresponder a un aprendiz existente.
- No admite valores nulos.
- Forma parte de la restricción de unicidad compuesta.

#### id_curso

- Debe corresponder a un curso existente.
- No admite valores nulos.
- Forma parte de la restricción de unicidad compuesta.

#### fecha_inscripcion

- Debe representar una fecha válida.
- Se utiliza el formato de intercambio AAAA-MM-DD.
- Por defecto corresponde a la fecha actual.
- Debe conservarse después de registrar la inscripción.
- No debe reemplazarse al recuperar el registro.

#### estado

- Debe corresponder a uno de los estados permitidos.
- El estado inicial es Activa.
- Solo una inscripción activa puede cancelarse o finalizarse.
- No admite cadenas vacías.
- Las transiciones se controlarán mediante lógica de negocio.

### 11.4. Dominio del estado administrativo

| Valor | Descripción |
|---|---|
| Activa | Inscripción vigente. |
| Cancelada | Inscripción cancelada. |
| Finalizada | Inscripción concluida. |

### 11.5. Transiciones de estado

| Estado actual | Estado destino | Permitido |
|---|---|---|
| Activa | Cancelada | Sí |
| Activa | Finalizada | Sí |
| Cancelada | Activa | No |
| Cancelada | Finalizada | No |
| Finalizada | Activa | No |
| Finalizada | Cancelada | No |

Una actualización que mantenga el mismo estado no constituye
una transición. Su tratamiento como operación idempotente
se definirá durante la implementación.

### 11.6. Restricción de unicidad compuesta

```sql
UNIQUE (id_aprendiz, id_curso)
```

Impide registrar dos inscripciones correspondientes al mismo
aprendiz y curso.

La restricción se aplica independientemente del estado
administrativo.

Cada columna puede repetirse individualmente, pero no puede
repetirse la combinación de ambas.

### 11.7. Claves

- Clave primaria: id_inscripcion.
- Clave alternativa: codigo.
- Clave alternativa compuesta: id_aprendiz, id_curso.
- Clave foránea: id_aprendiz referencia aprendiz.id_persona.
- Clave foránea: id_curso referencia curso.id_curso.

### 11.8. Valores predeterminados

| Atributo | Valor predeterminado |
|---|---|
| id_inscripcion | Generación automática. |
| codigo | Ninguno. |
| id_aprendiz | Ninguno. |
| id_curso | Ninguno. |
| fecha_inscripcion | CURRENT_DATE. |
| estado | Activa. |

### 11.9. Ejemplo de registros

| id_inscripcion | codigo | id_aprendiz | id_curso | fecha_inscripcion | estado |
|---:|---|---:|---:|---|---|
| 1 | INS-001 | 1 | 1 | 2026-11-28 | Activa |
| 2 | INS-002 | 1 | 2 | 2026-11-28 | Activa |

## 12. Tabla calificacion

### 12.1. Descripción general

Almacena las notas académicas correspondientes a
las inscripciones de los aprendices.

Cada calificación pertenece exactamente a una inscripción.

### 12.2. Diccionario de atributos

| Atributo | Descripción | Tipo | Tamaño | Nulo | Restricciones | Ejemplo |
|---|---|---|---|---|---|---|
| id_calificacion | Identificador interno de la calificación. | INT UNSIGNED | 4 bytes | No | PK, AI, NN | 1 |
| codigo | Código funcional de la calificación. | VARCHAR(30) | 30 caracteres | No | UK, NN, CK | CAL-001 |
| id_inscripcion | Inscripción asociada a la nota. | INT UNSIGNED | 4 bytes | No | FK, NN | 1 |
| nota | Valor numérico de la calificación. | DECIMAL(3,2) | 3 dígitos, 2 decimales | No | NN, CK | 4.50 |
| fecha | Fecha original de registro de la nota. | DATE | 3 bytes | No | NN, DEFAULT | 2026-11-28 |

### 12.3. Validaciones por atributo

#### id_calificacion

- Generado automáticamente.
- Identifica una calificación única.
- No debe modificarse.

#### codigo

- Debe contener entre 1 y 30 caracteres.
- Debe ser único.
- No admite cadenas vacías.
- Distingue mayúsculas y minúsculas.
- Se eliminan los espacios externos.

#### id_inscripcion

- Debe corresponder a una inscripción existente.
- No admite valores nulos.
- La inscripción debe estar activa para registrar
  o modificar calificaciones.
- Las calificaciones existentes pueden consultarse
  independientemente del estado de la inscripción.

#### nota

- Debe ser un valor numérico decimal.
- El valor mínimo permitido es 0.00.
- El valor máximo permitido es 5.00.
- Admite como máximo dos posiciones decimales.
- No admite valores booleanos.
- No admite valores nulos.
- No admite valores infinitos ni NaN.

La aplicación deberá validar la precisión antes de almacenar
la nota, debido a que la conversión al tipo DECIMAL puede
redondear valores con una precisión superior.

#### fecha

- Debe representar una fecha válida.
- Utiliza el formato de intercambio AAAA-MM-DD.
- Por defecto corresponde a la fecha actual.
- Debe conservarse después del registro.
- No se modifica cuando se actualiza la nota.

### 12.4. Claves

- Clave primaria: id_calificacion.
- Clave alternativa: codigo.
- Clave foránea: id_inscripcion referencia
  inscripcion.id_inscripcion.

### 12.5. Valores predeterminados

| Atributo | Valor predeterminado |
|---|---|
| id_calificacion | Generación automática. |
| codigo | Ninguno. |
| id_inscripcion | Ninguno. |
| nota | Ninguno. |
| fecha | CURRENT_DATE. |

### 12.6. Ejemplo de registros

| id_calificacion | codigo | id_inscripcion | nota | fecha |
|---:|---|---:|---:|---|
| 1 | CAL-001 | 1 | 4.50 | 2026-11-28 |
| 2 | CAL-002 | 1 | 3.80 | 2026-11-28 |
| 3 | CAL-003 | 1 | 4.20 | 2026-11-28 |

## 13. Diccionario de atributos derivados

Los siguientes atributos se obtienen mediante cálculos
y consultas.

No corresponden a columnas físicas de las siete tablas.

### 13.1. Rendimiento académico

| Atributo | Descripción | Tipo conceptual | Nulo | Origen |
|---|---|---|---|---|
| total_calificaciones | Cantidad de notas registradas. | Entero | No | COUNT |
| promedio | Media aritmética de las notas. | Decimal | Sí | AVG y ROUND |
| estado_academico | Resultado académico del aprendiz. | Texto | No | Regla de negocio |
| nota_maxima | Mayor nota registrada. | Decimal | Sí | MAX |
| nota_minima | Menor nota registrada. | Decimal | Sí | MIN |

### 13.2. Cálculo del promedio

El promedio se obtiene sumando las calificaciones
y dividiendo el resultado entre la cantidad de notas.

Se requieren como mínimo tres calificaciones para
determinar el rendimiento académico definitivo.

El resultado se redondea a dos decimales.

### 13.3. Dominio del estado académico

| Estado | Condición |
|---|---|
| Pendiente | Menos de tres calificaciones. |
| Aprobado | Tres o más notas y promedio redondeado mayor o igual a 3.00. |
| Reprobado | Tres o más notas y promedio redondeado inferior a 3.00. |

### 13.4. Política de redondeo

Se utilizará redondeo decimal al valor más cercano,
resolviendo los empates hacia arriba para valores
no negativos.

En Python se propone Decimal con ROUND_HALF_UP.

El resultado mostrado deberá coincidir con el valor
utilizado para determinar la aprobación.

### 13.5. Ejemplo de rendimiento

A partir de las siguientes calificaciones:

- Primera nota: 4.50.
- Segunda nota: 3.80.
- Tercera nota: 4.20.

Se obtiene:

```text
Cantidad de notas: 3

Promedio = (4.50 + 3.80 + 4.20) / 3

Promedio = 4.166666...

Promedio redondeado = 4.17

Estado académico = Aprobado
```

### 13.6. Diferencia entre estados

El estado administrativo pertenece a la inscripción
y se almacena permanentemente.

El estado académico se calcula a partir de las notas.

| Característica | Estado administrativo | Estado académico |
|---|---|---|
| Almacenamiento | Persistente | Calculado |
| Origen | Inscripcion.estado | Calificacion.nota |
| Valores | Activa, Cancelada, Finalizada | Pendiente, Aprobado, Reprobado |
| Modificación | Operación de negocio | Recalculado automáticamente |

Una inscripción cancelada o finalizada puede conservar
sus calificaciones y permitir su consulta.

## 14. Catálogo de claves primarias

| Tabla | Atributo | Tipo | Autoincremental |
|---|---|---|---|
| persona | id_persona | INT UNSIGNED | Sí |
| profesor | id_persona | INT UNSIGNED | No |
| aprendiz | id_persona | INT UNSIGNED | No |
| modalidad | id_modalidad | INT UNSIGNED | Sí |
| curso | id_curso | INT UNSIGNED | Sí |
| inscripcion | id_inscripcion | INT UNSIGNED | Sí |
| calificacion | id_calificacion | INT UNSIGNED | Sí |

Todas las claves primarias son obligatorias y únicas.

## 15. Catálogo de claves foráneas

| Restricción propuesta | Tabla | Atributo | Referencia | Nulo |
|---|---|---|---|---|
| fk_profesor_persona | profesor | id_persona | persona.id_persona | No |
| fk_aprendiz_persona | aprendiz | id_persona | persona.id_persona | No |
| fk_curso_modalidad | curso | id_modalidad | modalidad.id_modalidad | No |
| fk_curso_profesor | curso | id_profesor | profesor.id_persona | Sí |
| fk_inscripcion_aprendiz | inscripcion | id_aprendiz | aprendiz.id_persona | No |
| fk_inscripcion_curso | inscripcion | id_curso | curso.id_curso | No |
| fk_calificacion_inscripcion | calificacion | id_inscripcion | inscripcion.id_inscripcion | No |

### 15.1. Políticas referenciales

Todas las claves foráneas utilizarán inicialmente:

```sql
ON DELETE RESTRICT
ON UPDATE RESTRICT
```

Estas políticas impedirán eliminar o modificar claves
referenciadas cuando existan registros dependientes.

No se utilizarán eliminaciones automáticas en cascada.

## 16. Catálogo de restricciones de unicidad

| Nombre propuesto | Tabla | Atributos |
|---|---|---|
| uq_persona_documento | persona | documento |
| uq_profesor_codigo | profesor | codigo |
| uq_modalidad_nombre | modalidad | nombre |
| uq_curso_codigo | curso | codigo |
| uq_inscripcion_codigo | inscripcion | codigo |
| uq_inscripcion_aprendiz_curso | inscripcion | id_aprendiz, id_curso |
| uq_calificacion_codigo | calificacion | codigo |

Estas restricciones son adicionales a las claves primarias.

## 17. Catálogo de restricciones de dominio

Las siguientes expresiones representan propuestas para
la implementación física.

| Nombre propuesto | Tabla | Atributo | Condición |
|---|---|---|---|
| ck_persona_documento | persona | documento | Solo dígitos y al menos un dígito distinto de cero. |
| ck_persona_nombre | persona | nombre | CHAR_LENGTH(TRIM(nombre)) > 0 |
| ck_persona_edad | persona | edad | edad >= 0 |
| ck_profesor_codigo | profesor | codigo | codigo > 0 |
| ck_profesor_profesion | profesor | profesion | CHAR_LENGTH(TRIM(profesion)) > 0 |
| ck_profesor_especialidad | profesor | especialidad | CHAR_LENGTH(TRIM(especialidad)) > 0 |
| ck_aprendiz_telefono | aprendiz | telefono | CHAR_LENGTH(TRIM(telefono)) > 0 |
| ck_aprendiz_correo | aprendiz | correo | CHAR_LENGTH(TRIM(correo)) > 0 |
| ck_aprendiz_direccion | aprendiz | direccion | CHAR_LENGTH(TRIM(direccion)) > 0 |
| ck_modalidad_nombre | modalidad | nombre | CHAR_LENGTH(TRIM(nombre)) > 0 |
| ck_curso_codigo | curso | codigo | CHAR_LENGTH(TRIM(codigo)) > 0 |
| ck_curso_nombre | curso | nombre | CHAR_LENGTH(TRIM(nombre)) > 0 |
| ck_curso_descripcion | curso | descripcion | CHAR_LENGTH(TRIM(descripcion)) > 0 |
| ck_curso_duracion | curso | duracion_horas | duracion_horas > 0 |
| ck_inscripcion_codigo | inscripcion | codigo | CHAR_LENGTH(TRIM(codigo)) > 0 |
| ck_inscripcion_estado | inscripcion | estado | estado IN ('Activa', 'Cancelada', 'Finalizada') |
| ck_calificacion_codigo | calificacion | codigo | CHAR_LENGTH(TRIM(codigo)) > 0 |
| ck_calificacion_nota | calificacion | nota | nota BETWEEN 0.00 AND 5.00 |

Las expresiones definitivas se verificarán durante
la implementación en el sistema gestor seleccionado.

Las restricciones de texto no vacío no sustituyen
las validaciones completas de formato en Python.

La comparación del estado deberá distinguir mayúsculas
y minúsculas.

## 18. Catálogo de valores predeterminados

| Tabla | Atributo | Valor |
|---|---|---|
| persona | id_persona | AUTO_INCREMENT |
| modalidad | id_modalidad | AUTO_INCREMENT |
| modalidad | descripcion | NULL |
| curso | id_curso | AUTO_INCREMENT |
| curso | id_profesor | NULL |
| inscripcion | id_inscripcion | AUTO_INCREMENT |
| inscripcion | fecha_inscripcion | CURRENT_DATE |
| inscripcion | estado | Activa |
| calificacion | id_calificacion | AUTO_INCREMENT |
| calificacion | fecha | CURRENT_DATE |

Los atributos restantes deberán proporcionarse
explícitamente durante las operaciones de registro.

## 19. Atributos que permiten valores nulos

| Tabla | Atributo | Justificación |
|---|---|---|
| modalidad | descripcion | La descripción es complementaria. |
| curso | id_profesor | Un curso puede registrarse sin profesor asignado. |

Las demás columnas son obligatorias.

Un valor NULL representa ausencia de información y no
debe confundirse con cero ni con una cadena vacía.

## 20. Correspondencia entre Python y SQL

| Dato | Tipo actual en Python | Tipo propuesto en SQL |
|---|---|---|
| Identificadores internos | No existen actualmente | INT UNSIGNED |
| Documento | int | VARCHAR(20) |
| Nombre | str | VARCHAR(150) |
| Edad | int | INT UNSIGNED |
| Código de profesor | int | INT UNSIGNED |
| Profesión | str | VARCHAR(100) |
| Especialidad | str | VARCHAR(100) |
| Teléfono | str | VARCHAR(20) |
| Correo | str | VARCHAR(254) |
| Dirección | str | VARCHAR(200) |
| Código de curso | str | VARCHAR(30) |
| Descripción de curso | str | TEXT |
| Duración | int | INT UNSIGNED |
| Modalidad | str | FK a modalidad |
| Profesor asociado | Profesor o None | INT UNSIGNED o NULL |
| Aprendiz asociado | Aprendiz | INT UNSIGNED |
| Curso asociado | Curso | INT UNSIGNED |
| Inscripción asociada | Inscripcion | INT UNSIGNED |
| Código de inscripción | str | VARCHAR(30) |
| Código de calificación | str | VARCHAR(30) |
| Fecha | datetime.date | DATE |
| Estado | str | VARCHAR(15) |
| Nota | float | DECIMAL(3,2) |

### 20.1. Adaptaciones futuras

Durante la fase de persistencia será necesario:

- Adaptar el documento de identificación de int a str.
- Incorporar identificadores persistentes.
- Adaptar las notas a Decimal.
- Incorporar límites de longitud.
- Recuperar las fechas originales.
- Recuperar las relaciones mediante claves foráneas.
- Sustituir las comparaciones de identidad de objetos
  por identificadores persistentes cuando corresponda.
- Implementar actualizaciones persistentes de los estados.
- Mantener las validaciones de dominio.

Estas modificaciones no se realizarán durante
la fase actual de diseño.

## 21. Validaciones por nivel

### 21.1. Base de datos

La base de datos será responsable de garantizar:

- Integridad de entidad.
- Integridad referencial.
- Unicidad.
- Obligatoriedad.
- Tipos de datos.
- Longitudes máximas.
- Rangos numéricos.
- Dominios controlados.

### 21.2. Aplicación Python

La aplicación será responsable de validar:

- Formatos de documentos.
- Formatos de correo electrónico.
- Formatos telefónicos.
- Entradas vacías.
- Precisión de las calificaciones.
- Transiciones de estado.
- Existencia de registros relacionados.
- Reglas de rendimiento académico.
- Operaciones sobre inscripciones activas.

Las validaciones de la aplicación complementan las
restricciones de la base de datos y no las sustituyen.

### 21.3. Transacciones

Se utilizarán transacciones para operaciones que
requieran modificar varios registros de forma coherente.

Entre ellas:

- Registro de persona y profesor.
- Registro de persona y aprendiz.
- Asociación de un segundo rol.
- Registro o modificación de notas.
- Cambios de estado de inscripción.

Las operaciones concurrentes deberán coordinarse para
evitar inconsistencias.

## 22. Casos propuestos de validación

### 22.1. Persona

| Atributo | Valor | Resultado esperado |
|---|---|---|
| documento | 0012345678 | Aceptado |
| documento | ABC123 | Rechazado |
| documento | 0000 | Rechazado |
| documento | Documento duplicado | Rechazado |
| nombre | Ana Torres | Aceptado |
| nombre | Cadena vacía | Rechazado |
| edad | 22 | Aceptado |
| edad | 0 | Aceptado |
| edad | -1 | Rechazado |

### 22.2. Profesor

| Atributo | Valor | Resultado esperado |
|---|---|---|
| codigo | 1001 | Aceptado |
| codigo | 0 | Rechazado |
| codigo | -10 | Rechazado |
| codigo | Código duplicado | Rechazado |
| id_persona | Persona inexistente | Rechazado |
| profesion | Cadena vacía | Rechazado |

### 22.3. Aprendiz

| Atributo | Valor | Resultado esperado |
|---|---|---|
| telefono | +573000000001 | Aceptado |
| telefono | ++573000000001 | Rechazado |
| telefono | ABC123 | Rechazado |
| correo | ana@example.com | Aceptado |
| correo | correo-invalido | Rechazado |
| correo | @example.com | Rechazado |
| direccion | Cadena vacía | Rechazado |

### 22.4. Modalidad

| Atributo | Valor | Resultado esperado |
|---|---|---|
| nombre | titulada | Aceptado si no existe |
| nombre | Nombre duplicado | Rechazado |
| nombre | Cadena vacía | Rechazado |
| descripcion | NULL | Aceptado |

### 22.5. Curso

| Atributo | Valor | Resultado esperado |
|---|---|---|
| codigo | CUR-001 | Aceptado si no existe |
| codigo | Código duplicado | Rechazado |
| duracion_horas | 48 | Aceptado |
| duracion_horas | 0 | Rechazado |
| duracion_horas | -20 | Rechazado |
| id_modalidad | Modalidad inexistente | Rechazado |
| id_profesor | NULL | Aceptado |
| id_profesor | Profesor inexistente | Rechazado |

### 22.6. Inscripcion

| Atributo o regla | Valor | Resultado esperado |
|---|---|---|
| codigo | INS-001 | Aceptado si no existe |
| codigo | Código duplicado | Rechazado |
| id_aprendiz | Aprendiz inexistente | Rechazado |
| id_curso | Curso inexistente | Rechazado |
| aprendiz y curso | Combinación duplicada | Rechazado |
| estado | Activa | Aceptado |
| estado | Desconocido | Rechazado |
| Transición | Activa a Cancelada | Aceptado |
| Transición | Finalizada a Activa | Rechazado |

### 22.7. Calificacion

| Atributo o regla | Valor | Resultado esperado |
|---|---|---|
| nota | 0.00 | Aceptado |
| nota | 3.00 | Aceptado |
| nota | 5.00 | Aceptado |
| nota | -0.01 | Rechazado |
| nota | 5.01 | Rechazado |
| nota | 3.456 | Rechazado |
| nota | Texto no numérico | Rechazado |
| nota | Booleano | Rechazado |
| codigo | Código duplicado | Rechazado |
| id_inscripcion | Inscripción inexistente | Rechazado |
| Registro de nota | Inscripción cancelada | Rechazado |
| Modificación de nota | Inscripción finalizada | Rechazado |

### 22.8. Rendimiento académico

| Calificaciones | Promedio | Estado esperado |
|---|---|---|
| Ninguna | NULL | Pendiente |
| 4.00, 5.00 | NULL | Pendiente |
| 3.00, 3.00, 3.00 | 3.00 | Aprobado |
| 2.00, 2.50, 3.00 | 2.50 | Reprobado |
| 2.99, 3.00, 3.00 | 3.00 | Aprobado |
| 4.50, 3.80, 4.20 | 4.17 | Aprobado |

Estos casos representan resultados esperados del diseño.

No constituyen pruebas ejecutadas sobre la base de datos.

## 23. Seguridad y tratamiento de información

La base de datos almacenará información personal y académica.

Los atributos que requieren especial protección incluyen:

| Tabla | Atributos |
|---|---|
| persona | documento, nombre, edad |
| aprendiz | telefono, correo, direccion |
| profesor | codigo, profesion, especialidad |
| inscripcion | Relaciones académicas y estado |
| calificacion | nota y relaciones académicas |

Durante las fases posteriores deberán considerarse:

- Control de acceso a la información.
- Consultas SQL parametrizadas.
- Protección de credenciales.
- Variables de entorno.
- Copias de seguridad.
- Uso de datos ficticios en pruebas.
- Prevención de exposición innecesaria de datos personales.

No deberán almacenarse credenciales reales ni información
personal de producción dentro del repositorio GitHub.

## 24. Resumen estadístico

### 24.1. Distribución por tabla

| Tabla | Columnas | Obligatorias | Opcionales |
|---|---:|---:|---:|
| persona | 4 | 4 | 0 |
| profesor | 4 | 4 | 0 |
| aprendiz | 4 | 4 | 0 |
| modalidad | 3 | 2 | 1 |
| curso | 7 | 6 | 1 |
| inscripcion | 6 | 6 | 0 |
| calificacion | 5 | 5 | 0 |
| **Total** | **33** | **31** | **2** |

### 24.2. Distribución por tipo de dato

| Tipo de dato | Cantidad |
|---|---:|
| INT UNSIGNED | 14 |
| VARCHAR | 15 |
| TEXT | 1 |
| DATE | 2 |
| DECIMAL | 1 |
| **Total** | **33** |

### 24.3. Distribución de claves

| Elemento | Cantidad |
|---|---:|
| Tablas | 7 |
| Claves primarias | 7 |
| Claves primarias autoincrementales | 5 |
| Claves primarias compartidas | 2 |
| Claves foráneas | 7 |
| Restricciones UNIQUE adicionales | 7 |
| Restricciones UNIQUE compuestas | 1 |
| Columnas opcionales | 2 |
| Columnas obligatorias | 31 |

La restricción UNIQUE compuesta está incluida dentro
de las siete restricciones de unicidad adicionales.

## 25. Trazabilidad documental

| Tabla | Reglas relacionadas |
|---|---|
| persona | RN-PER |
| profesor | RN-PRO |
| aprendiz | RN-APR |
| modalidad | RN-MOD |
| curso | RN-CUR |
| inscripcion | RN-INS |
| calificacion | RN-CAL |
| Atributos derivados | RN-REN |
| Reportes | RN-REP |
| Integridad | RN-INT |
| Persistencia | RN-PERST |

Las reglas específicas se encuentran documentadas
en reglas-negocio.md.

## 26. Validación del diccionario de datos

| Requisito | Resultado documental |
|---|---|
| Identificación de las tablas. | Cumple |
| Nombre de cada atributo. | Cumple |
| Descripción de cada atributo. | Cumple |
| Tipo de dato. | Cumple |
| Tamaño cuando corresponde. | Cumple |
| Permisión de valores nulos. | Cumple |
| Restricciones. | Cumple |
| Claves primarias. | Cumple |
| Claves foráneas. | Cumple |
| Valores predeterminados. | Cumple |
| Ejemplos de registros. | Cumple |
| Atributos derivados. | Cumple |
| Correspondencia con Python. | Cumple |
| Casos propuestos de validación. | Cumple |

Esta revisión corresponde al diseño documental.

La validación técnica de las restricciones y los tipos
de datos se realizará durante la implementación física.

## 27. Conclusiones

El diccionario de datos documenta las 33 columnas
distribuidas en las siete tablas del Sistema de Gestión
Académica.

Se establecieron los nombres, descripciones, tipos de datos,
tamaños, restricciones, valores predeterminados y ejemplos
de los atributos.

También se documentaron las claves primarias, claves
foráneas, restricciones de unicidad y atributos derivados.

La correspondencia entre los tipos de Python y SQL permitirá
orientar las futuras adaptaciones de la aplicación.

Este documento constituye una referencia para garantizar
la coherencia entre el diseño relacional, la implementación
de la base de datos, la capa de persistencia y la futura
API REST.

El siguiente paso consiste en justificar el cumplimiento
de la primera, segunda y tercera forma normal.
