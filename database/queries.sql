

-- Sistema de Gestion Academica
-- Fase 2: Implementacion de la base de datos
-- Consultas y operaciones CRUD

-- ============================================
-- MODULO: PROFESORES
-- ============================================

-- 1. Registrar profesor

START TRANSACTION;

INSERT INTO persona (documento, nombre, edad)
VALUES ('6000000001', 'Profesor de ejemplo', 35);

SET @id_profesor = LAST_INSERT_ID();

INSERT INTO profesor
    (id_persona, codigo, profesion, especialidad)
VALUES
    (@id_profesor, 601, 'Ingeniero de sistemas', 'Programacion');

-- 2. Listar profesores

SELECT
    p.id_persona,
    p.documento,
    p.nombre,
    p.edad,
    pr.codigo,
    pr.profesion,
    pr.especialidad
FROM profesor AS pr
INNER JOIN persona AS p
    ON pr.id_persona = p.id_persona
ORDER BY p.nombre;

-- 3. Buscar profesor por documento

SELECT
    p.documento,
    p.nombre,
    p.edad,
    pr.codigo,
    pr.profesion,
    pr.especialidad
FROM profesor AS pr
INNER JOIN persona AS p
    ON pr.id_persona = p.id_persona
WHERE p.documento = '6000000001';

-- 4. Buscar profesor por codigo

SELECT
    p.documento,
    p.nombre,
    pr.codigo,
    pr.profesion,
    pr.especialidad
FROM profesor AS pr
INNER JOIN persona AS p
    ON pr.id_persona = p.id_persona
WHERE pr.codigo = 601;

-- 5. Actualizar datos personales

UPDATE persona
SET nombre = 'Profesor actualizado',
    edad = 36
WHERE id_persona = @id_profesor;

-- 6. Actualizar datos profesionales

UPDATE profesor
SET profesion = 'Ingeniero de software',
    especialidad = 'Bases de datos'
WHERE id_persona = @id_profesor;

-- 7. Consultar cursos asignados al profesor

SELECT
    pr.codigo AS codigo_profesor,
    p.nombre AS profesor,
    c.codigo AS codigo_curso,
    c.nombre AS curso,
    c.duracion_horas
FROM profesor AS pr
INNER JOIN persona AS p
    ON pr.id_persona = p.id_persona
INNER JOIN curso AS c
    ON pr.id_persona = c.id_profesor
WHERE p.documento = '6000000001';

-- 8. Verificar datos actualizados

SELECT
    p.documento,
    p.nombre,
    p.edad,
    pr.codigo,
    pr.profesion,
    pr.especialidad
FROM profesor AS pr
INNER JOIN persona AS p
    ON pr.id_persona = p.id_persona
WHERE pr.id_persona = @id_profesor;

-- Revertir los datos de demostracion

ROLLBACK;



-- ============================================
-- MODULO: APRENDICES
-- ============================================

-- 1. Registrar aprendiz

START TRANSACTION;

INSERT INTO persona (documento, nombre, edad)
VALUES ('7000000001', 'Aprendiz de ejemplo', 22);

SET @id_aprendiz = LAST_INSERT_ID();

INSERT INTO aprendiz
    (id_persona, telefono, correo, direccion)
VALUES
    (@id_aprendiz, '3001234567',
    'aprendiz@example.com', 'Calle 10');

-- 2. Listar aprendices

SELECT
    p.id_persona,
    p.documento,
    p.nombre,
    p.edad,
    a.telefono,
    a.correo,
    a.direccion
FROM aprendiz AS a
INNER JOIN persona AS p
    ON a.id_persona = p.id_persona
ORDER BY p.nombre;

-- 3. Buscar aprendiz por documento

SELECT
    p.documento,
    p.nombre,
    p.edad,
    a.telefono,
    a.correo,
    a.direccion
FROM aprendiz AS a
INNER JOIN persona AS p
    ON a.id_persona = p.id_persona
WHERE p.documento = '7000000001';

-- 4. Actualizar datos personales

UPDATE persona
SET nombre = 'Aprendiz actualizado',
    edad = 23
WHERE id_persona = @id_aprendiz;

-- 5. Actualizar datos de contacto

UPDATE aprendiz
SET telefono = '3109876543',
    correo = 'actualizado@example.com',
    direccion = 'Calle 20'
WHERE id_persona = @id_aprendiz;

-- 6. Consultar cursos del aprendiz

SELECT
    p.documento,
    p.nombre AS aprendiz,
    c.codigo AS codigo_curso,
    c.nombre AS curso,
    m.nombre AS modalidad,
    i.fecha_inscripcion,
    i.estado
FROM aprendiz AS a
INNER JOIN persona AS p
    ON a.id_persona = p.id_persona
INNER JOIN inscripcion AS i
    ON a.id_persona = i.id_aprendiz
INNER JOIN curso AS c
    ON i.id_curso = c.id_curso
INNER JOIN modalidad AS m
    ON c.id_modalidad = m.id_modalidad
WHERE a.id_persona = @id_aprendiz;

-- 7. Verificar datos actualizados

SELECT
    p.documento,
    p.nombre,
    p.edad,
    a.telefono,
    a.correo,
    a.direccion
FROM aprendiz AS a
INNER JOIN persona AS p
    ON a.id_persona = p.id_persona
WHERE a.id_persona = @id_aprendiz;

-- Revertir los datos de demostracion

ROLLBACK;


-- ============================================
-- MODULO: MODALIDADES
-- ============================================

START TRANSACTION;

-- 1. Listar modalidades

SELECT
    id_modalidad,
    nombre,
    descripcion
FROM modalidad
ORDER BY nombre;

-- 2. Buscar modalidad por nombre

SELECT
    id_modalidad,
    nombre,
    descripcion
FROM modalidad
WHERE nombre = 'titulada';

-- 3. Registrar una modalidad de demostracion

INSERT INTO modalidad (nombre, descripcion)
VALUES (
    'especializacion',
    'Formacion especializada de demostracion'
);

SET @id_modalidad_demo = LAST_INSERT_ID();

-- 4. Buscar modalidad por identificador

SELECT
    id_modalidad,
    nombre,
    descripcion
FROM modalidad
WHERE id_modalidad = @id_modalidad_demo;

-- 5. Actualizar descripcion

UPDATE modalidad
SET descripcion = 'Formacion especializada actualizada'
WHERE id_modalidad = @id_modalidad_demo;

-- 6. Consultar cursos por modalidad

SELECT
    m.nombre AS modalidad,
    c.codigo AS codigo_curso,
    c.nombre AS curso,
    c.duracion_horas
FROM modalidad AS m
INNER JOIN curso AS c
    ON m.id_modalidad = c.id_modalidad
WHERE m.nombre = 'titulada';

-- 7. Contar cursos por modalidad

SELECT
    m.id_modalidad,
    m.nombre AS modalidad,
    COUNT(c.id_curso) AS total_cursos
FROM modalidad AS m
LEFT JOIN curso AS c
    ON m.id_modalidad = c.id_modalidad
GROUP BY
    m.id_modalidad,
    m.nombre
ORDER BY m.nombre;

-- 8. Verificar modalidad actualizada

SELECT
    id_modalidad,
    nombre,
    descripcion
FROM modalidad
WHERE id_modalidad = @id_modalidad_demo;

-- Revertir los datos de demostracion

ROLLBACK;


-- ============================================
-- MODULO: CURSOS
-- ============================================

START TRANSACTION;

-- 1. Obtener modalidad existente

SET @id_modalidad = (
    SELECT id_modalidad
    FROM modalidad
    WHERE nombre = 'titulada'
);

-- 2. Registrar profesor de demostracion

INSERT INTO persona (documento, nombre, edad)
VALUES ('8000000001', 'Profesor de cursos', 35);

SET @id_profesor = LAST_INSERT_ID();

INSERT INTO profesor
    (id_persona, codigo, profesion, especialidad)
VALUES
    (@id_profesor, 801, 'Ingeniero de sistemas', 'Python');

-- 3. Registrar curso sin profesor asignado

INSERT INTO curso
    (codigo, nombre, descripcion, duracion_horas, id_modalidad)
VALUES
    ('CUR801', 'Programacion en Python',
    'Fundamentos de programacion orientada a objetos',
    120, @id_modalidad);

SET @id_curso = LAST_INSERT_ID();

-- 4. Listar cursos

SELECT
    c.id_curso,
    c.codigo,
    c.nombre,
    c.descripcion,
    c.duracion_horas,
    m.nombre AS modalidad,
    COALESCE(p.nombre, 'Sin asignar') AS profesor
FROM curso AS c
INNER JOIN modalidad AS m
    ON c.id_modalidad = m.id_modalidad
LEFT JOIN profesor AS pr
    ON c.id_profesor = pr.id_persona
LEFT JOIN persona AS p
    ON pr.id_persona = p.id_persona
ORDER BY c.nombre;

-- 5. Buscar curso por codigo

SELECT
    c.codigo,
    c.nombre,
    c.descripcion,
    c.duracion_horas,
    m.nombre AS modalidad
FROM curso AS c
INNER JOIN modalidad AS m
    ON c.id_modalidad = m.id_modalidad
WHERE c.codigo = 'CUR801';

-- 6. Asignar profesor responsable

UPDATE curso
SET id_profesor = @id_profesor
WHERE id_curso = @id_curso;

-- 7. Actualizar informacion del curso

UPDATE curso
SET nombre = 'Python avanzado',
    descripcion = 'Programacion orientada a objetos y SOLID',
    duracion_horas = 160
WHERE id_curso = @id_curso;

-- 8. Consultar cursos por profesor

SELECT
    p.nombre AS profesor,
    c.codigo,
    c.nombre AS curso,
    c.duracion_horas
FROM curso AS c
INNER JOIN profesor AS pr
    ON c.id_profesor = pr.id_persona
INNER JOIN persona AS p
    ON pr.id_persona = p.id_persona
WHERE pr.id_persona = @id_profesor;

-- 9. Consultar aprendices inscritos en el curso

SELECT
    c.codigo AS codigo_curso,
    c.nombre AS curso,
    p.documento,
    p.nombre AS aprendiz,
    i.fecha_inscripcion,
    i.estado
FROM curso AS c
INNER JOIN inscripcion AS i
    ON c.id_curso = i.id_curso
INNER JOIN aprendiz AS a
    ON i.id_aprendiz = a.id_persona
INNER JOIN persona AS p
    ON a.id_persona = p.id_persona
WHERE c.id_curso = @id_curso;

-- 10. Contar aprendices por curso

SELECT
    c.codigo,
    c.nombre AS curso,
    COUNT(i.id_inscripcion) AS total_aprendices
FROM curso AS c
LEFT JOIN inscripcion AS i
    ON c.id_curso = i.id_curso
GROUP BY
    c.id_curso,
    c.codigo,
    c.nombre;

-- 11. Verificar informacion actualizada

SELECT
    c.codigo,
    c.nombre,
    c.descripcion,
    c.duracion_horas,
    m.nombre AS modalidad,
    COALESCE(p.nombre, 'Sin asignar') AS profesor
FROM curso AS c
INNER JOIN modalidad AS m
    ON c.id_modalidad = m.id_modalidad
LEFT JOIN profesor AS pr
    ON c.id_profesor = pr.id_persona
LEFT JOIN persona AS p
    ON pr.id_persona = p.id_persona
WHERE c.id_curso = @id_curso;

-- Revertir los datos de demostracion

ROLLBACK;


-- ============================================
-- MODULO: INSCRIPCIONES
-- ============================================

START TRANSACTION;

-- 1. Obtener modalidad existente

SET @id_modalidad = (
    SELECT id_modalidad
    FROM modalidad
    WHERE nombre = 'titulada'
);

-- 2. Registrar aprendiz de demostracion

INSERT INTO persona (documento, nombre, edad)
VALUES ('9000000001', 'Aprendiz de inscripciones', 22);

SET @id_aprendiz = LAST_INSERT_ID();

INSERT INTO aprendiz
    (id_persona, telefono, correo, direccion)
VALUES
    (@id_aprendiz, '3001234567',
    'inscripciones@example.com', 'Calle 30');

-- 3. Registrar cursos de demostracion

INSERT INTO curso
    (codigo, nombre, descripcion, duracion_horas, id_modalidad)
VALUES
    ('CUR901', 'Python', 'Programacion en Python',
    120, @id_modalidad);

SET @id_curso = LAST_INSERT_ID();

INSERT INTO curso
    (codigo, nombre, descripcion, duracion_horas, id_modalidad)
VALUES
    ('CUR902', 'MySQL', 'Bases de datos relacionales',
    80, @id_modalidad);

SET @id_curso_segundo = LAST_INSERT_ID();

-- 4. Registrar inscripciones

INSERT INTO inscripcion
    (codigo, id_aprendiz, id_curso)
VALUES
    ('INS901', @id_aprendiz, @id_curso);

SET @id_inscripcion = LAST_INSERT_ID();

INSERT INTO inscripcion
    (codigo, id_aprendiz, id_curso)
VALUES
    ('INS902', @id_aprendiz, @id_curso_segundo);

SET @id_inscripcion_segunda = LAST_INSERT_ID();

-- 5. Listar inscripciones

SELECT
    i.codigo,
    p.documento,
    p.nombre AS aprendiz,
    c.nombre AS curso,
    i.fecha_inscripcion,
    i.estado
FROM inscripcion AS i
INNER JOIN aprendiz AS a
    ON i.id_aprendiz = a.id_persona
INNER JOIN persona AS p
    ON a.id_persona = p.id_persona
INNER JOIN curso AS c
    ON i.id_curso = c.id_curso
ORDER BY i.codigo;

-- 6. Buscar inscripcion por codigo

SELECT
    i.codigo,
    p.nombre AS aprendiz,
    c.nombre AS curso,
    i.fecha_inscripcion,
    i.estado
FROM inscripcion AS i
INNER JOIN persona AS p
    ON i.id_aprendiz = p.id_persona
INNER JOIN curso AS c
    ON i.id_curso = c.id_curso
WHERE i.codigo = 'INS901';

-- 7. Consultar inscripciones por aprendiz

SELECT
    i.codigo AS inscripcion,
    c.codigo AS codigo_curso,
    c.nombre AS curso,
    i.fecha_inscripcion,
    i.estado
FROM inscripcion AS i
INNER JOIN curso AS c
    ON i.id_curso = c.id_curso
WHERE i.id_aprendiz = @id_aprendiz;

-- 8. Consultar inscripciones por curso

SELECT
    i.codigo AS inscripcion,
    p.documento,
    p.nombre AS aprendiz,
    i.fecha_inscripcion,
    i.estado
FROM inscripcion AS i
INNER JOIN persona AS p
    ON i.id_aprendiz = p.id_persona
WHERE i.id_curso = @id_curso;

-- 9. Verificar si existe una inscripcion

SELECT EXISTS (
    SELECT 1
    FROM inscripcion
    WHERE id_aprendiz = @id_aprendiz
      AND id_curso = @id_curso
) AS inscripcion_existente;

-- 10. Cancelar inscripcion activa

UPDATE inscripcion
SET estado = 'Cancelada'
WHERE id_inscripcion = @id_inscripcion
  AND estado = 'Activa';

SELECT ROW_COUNT() AS inscripciones_canceladas;

-- 11. Finalizar inscripcion activa

UPDATE inscripcion
SET estado = 'Finalizada'
WHERE id_inscripcion = @id_inscripcion_segunda
  AND estado = 'Activa';

SELECT ROW_COUNT() AS inscripciones_finalizadas;

-- 12. Intentar finalizar una inscripcion cancelada

UPDATE inscripcion
SET estado = 'Finalizada'
WHERE id_inscripcion = @id_inscripcion
  AND estado = 'Activa';

SELECT ROW_COUNT() AS transiciones_realizadas;

-- 13. Contar inscripciones por estado

SELECT
    estado,
    COUNT(*) AS total_inscripciones
FROM inscripcion
GROUP BY estado
ORDER BY estado;

-- 14. Verificar estados actualizados

SELECT
    i.codigo,
    p.nombre AS aprendiz,
    c.nombre AS curso,
    i.estado
FROM inscripcion AS i
INNER JOIN persona AS p
    ON i.id_aprendiz = p.id_persona
INNER JOIN curso AS c
    ON i.id_curso = c.id_curso
WHERE i.id_aprendiz = @id_aprendiz
ORDER BY i.codigo;

-- Revertir los datos de demostracion

ROLLBACK;


-- ============================================
-- MODULO: CALIFICACIONES
-- ============================================

START TRANSACTION;

-- 1. Obtener modalidad existente

SET @id_modalidad = (
    SELECT id_modalidad
    FROM modalidad
    WHERE nombre = 'titulada'
);

-- 2. Registrar aprendiz de demostracion

INSERT INTO persona (documento, nombre, edad)
VALUES ('9100000001', 'Aprendiz de calificaciones', 23);

SET @id_aprendiz = LAST_INSERT_ID();

INSERT INTO aprendiz
    (id_persona, telefono, correo, direccion)
VALUES
    (@id_aprendiz, '3001234567',
    'calificaciones@example.com', 'Calle 40');

-- 3. Registrar curso de demostracion

INSERT INTO curso
    (codigo, nombre, descripcion, duracion_horas, id_modalidad)
VALUES
    ('CUR910', 'Bases de datos',
    'Fundamentos de MySQL', 120, @id_modalidad);

SET @id_curso = LAST_INSERT_ID();

-- 4. Registrar inscripcion

INSERT INTO inscripcion
    (codigo, id_aprendiz, id_curso)
VALUES
    ('INS910', @id_aprendiz, @id_curso);

SET @id_inscripcion = LAST_INSERT_ID();

-- 5. Bloquear la inscripcion durante la transaccion

SELECT id_inscripcion, estado
FROM inscripcion
WHERE id_inscripcion = @id_inscripcion
FOR UPDATE;

-- 6. Registrar calificaciones en inscripcion activa

INSERT INTO calificacion
    (codigo, id_inscripcion, nota)
SELECT 'CAL910', id_inscripcion, 4.50
FROM inscripcion
WHERE id_inscripcion = @id_inscripcion
  AND estado = 'Activa';

INSERT INTO calificacion
    (codigo, id_inscripcion, nota)
SELECT 'CAL911', id_inscripcion, 3.80
FROM inscripcion
WHERE id_inscripcion = @id_inscripcion
  AND estado = 'Activa';

INSERT INTO calificacion
    (codigo, id_inscripcion, nota)
SELECT 'CAL912', id_inscripcion, 4.20
FROM inscripcion
WHERE id_inscripcion = @id_inscripcion
  AND estado = 'Activa';

-- 7. Listar calificaciones

SELECT
    ca.codigo,
    p.nombre AS aprendiz,
    c.nombre AS curso,
    i.codigo AS inscripcion,
    ca.nota,
    ca.fecha
FROM calificacion AS ca
INNER JOIN inscripcion AS i
    ON ca.id_inscripcion = i.id_inscripcion
INNER JOIN persona AS p
    ON i.id_aprendiz = p.id_persona
INNER JOIN curso AS c
    ON i.id_curso = c.id_curso
ORDER BY ca.codigo;

-- 8. Buscar calificacion por codigo

SELECT
    codigo,
    id_inscripcion,
    nota,
    fecha
FROM calificacion
WHERE codigo = 'CAL910';

-- 9. Consultar calificaciones por inscripcion

SELECT
    codigo,
    nota,
    fecha
FROM calificacion
WHERE id_inscripcion = @id_inscripcion
ORDER BY codigo;

-- 10. Consultar calificaciones por aprendiz

SELECT
    p.documento,
    p.nombre AS aprendiz,
    c.nombre AS curso,
    ca.codigo,
    ca.nota,
    ca.fecha
FROM calificacion AS ca
INNER JOIN inscripcion AS i
    ON ca.id_inscripcion = i.id_inscripcion
INNER JOIN persona AS p
    ON i.id_aprendiz = p.id_persona
INNER JOIN curso AS c
    ON i.id_curso = c.id_curso
WHERE i.id_aprendiz = @id_aprendiz;

-- 11. Consultar calificaciones por curso

SELECT
    c.codigo AS codigo_curso,
    c.nombre AS curso,
    p.nombre AS aprendiz,
    ca.codigo AS codigo_calificacion,
    ca.nota
FROM calificacion AS ca
INNER JOIN inscripcion AS i
    ON ca.id_inscripcion = i.id_inscripcion
INNER JOIN curso AS c
    ON i.id_curso = c.id_curso
INNER JOIN persona AS p
    ON i.id_aprendiz = p.id_persona
WHERE i.id_curso = @id_curso;

-- 12. Modificar calificacion de inscripcion activa

UPDATE calificacion AS ca
INNER JOIN inscripcion AS i
    ON ca.id_inscripcion = i.id_inscripcion
SET ca.nota = 4.80
WHERE ca.codigo = 'CAL910'
  AND i.estado = 'Activa';

SELECT ROW_COUNT() AS calificaciones_modificadas;

-- 13. Finalizar inscripcion

UPDATE inscripcion
SET estado = 'Finalizada'
WHERE id_inscripcion = @id_inscripcion
  AND estado = 'Activa';

-- 14. Intentar registrar nota en inscripcion finalizada

INSERT INTO calificacion
    (codigo, id_inscripcion, nota)
SELECT 'CAL913', id_inscripcion, 5.00
FROM inscripcion
WHERE id_inscripcion = @id_inscripcion
  AND estado = 'Activa';

SELECT ROW_COUNT() AS registros_no_permitidos;

-- 15. Intentar modificar nota en inscripcion finalizada

UPDATE calificacion AS ca
INNER JOIN inscripcion AS i
    ON ca.id_inscripcion = i.id_inscripcion
SET ca.nota = 5.00
WHERE ca.codigo = 'CAL910'
  AND i.estado = 'Activa';

SELECT ROW_COUNT() AS modificaciones_no_permitidas;

-- 16. Verificar calificaciones finales

SELECT
    ca.codigo,
    ca.nota,
    ca.fecha,
    i.estado AS estado_inscripcion
FROM calificacion AS ca
INNER JOIN inscripcion AS i
    ON ca.id_inscripcion = i.id_inscripcion
WHERE ca.id_inscripcion = @id_inscripcion
ORDER BY ca.codigo;

-- Revertir los datos de demostracion

ROLLBACK;


-- ============================================
-- MODULO: RENDIMIENTO ACADEMICO
-- ============================================

START TRANSACTION;

-- 1. Obtener modalidad existente

SET @id_modalidad = (
    SELECT id_modalidad
    FROM modalidad
    WHERE nombre = 'titulada'
);

-- 2. Registrar aprendices de demostracion

INSERT INTO persona (documento, nombre, edad)
VALUES ('9200000001', 'Aprendiz aprobado', 22);

SET @id_aprendiz_aprobado = LAST_INSERT_ID();

INSERT INTO aprendiz
    (id_persona, telefono, correo, direccion)
VALUES
    (@id_aprendiz_aprobado, '3001234567',
    'aprobado@example.com', 'Calle 50');

INSERT INTO persona (documento, nombre, edad)
VALUES ('9200000002', 'Aprendiz reprobado', 23);

SET @id_aprendiz_reprobado = LAST_INSERT_ID();

INSERT INTO aprendiz
    (id_persona, telefono, correo, direccion)
VALUES
    (@id_aprendiz_reprobado, '3101234567',
    'reprobado@example.com', 'Calle 51');

INSERT INTO persona (documento, nombre, edad)
VALUES ('9200000003', 'Aprendiz pendiente', 21);

SET @id_aprendiz_pendiente = LAST_INSERT_ID();

INSERT INTO aprendiz
    (id_persona, telefono, correo, direccion)
VALUES
    (@id_aprendiz_pendiente, '3201234567',
    'pendiente@example.com', 'Calle 52');

-- 3. Registrar curso de demostracion

INSERT INTO curso
    (codigo, nombre, descripcion, duracion_horas, id_modalidad)
VALUES
    ('CUR920', 'Programacion orientada a objetos',
    'Fundamentos de POO y SOLID', 120, @id_modalidad);

SET @id_curso = LAST_INSERT_ID();

-- 4. Registrar inscripciones

INSERT INTO inscripcion
    (codigo, id_aprendiz, id_curso)
VALUES
    ('INS920', @id_aprendiz_aprobado, @id_curso);

SET @id_inscripcion_aprobada = LAST_INSERT_ID();

INSERT INTO inscripcion
    (codigo, id_aprendiz, id_curso)
VALUES
    ('INS921', @id_aprendiz_reprobado, @id_curso);

SET @id_inscripcion_reprobada = LAST_INSERT_ID();

INSERT INTO inscripcion
    (codigo, id_aprendiz, id_curso)
VALUES
    ('INS922', @id_aprendiz_pendiente, @id_curso);

SET @id_inscripcion_pendiente = LAST_INSERT_ID();

-- 5. Registrar calificaciones

INSERT INTO calificacion (codigo, id_inscripcion, nota)
VALUES
    ('CAL920', @id_inscripcion_aprobada, 4.80),
    ('CAL921', @id_inscripcion_aprobada, 3.80),
    ('CAL922', @id_inscripcion_aprobada, 4.20),
    ('CAL923', @id_inscripcion_reprobada, 2.00),
    ('CAL924', @id_inscripcion_reprobada, 2.50),
    ('CAL925', @id_inscripcion_reprobada, 2.80),
    ('CAL926', @id_inscripcion_pendiente, 4.50),
    ('CAL927', @id_inscripcion_pendiente, 4.00);

-- 6. Calcular promedio por inscripcion

SELECT
    i.codigo AS inscripcion,
    COUNT(ca.id_calificacion) AS total_calificaciones,
    CASE
        WHEN COUNT(ca.id_calificacion) >= 3
        THEN CAST(
            (
                (2 * SUM(ca.nota * 100)
                + COUNT(ca.id_calificacion))
                DIV (2 * COUNT(ca.id_calificacion))
            ) / 100 AS DECIMAL(3,2)
        )
        ELSE NULL
    END AS promedio
FROM inscripcion AS i
LEFT JOIN calificacion AS ca
    ON i.id_inscripcion = ca.id_inscripcion
WHERE i.id_inscripcion = @id_inscripcion_aprobada
GROUP BY i.id_inscripcion, i.codigo;

-- 7. Consultar rendimiento por aprendiz

SELECT
    p.documento,
    p.nombre AS aprendiz,
    c.nombre AS curso,
    i.codigo AS inscripcion,
    COUNT(ca.id_calificacion) AS total_calificaciones,
    CASE
        WHEN COUNT(ca.id_calificacion) >= 3
        THEN CAST(
            (
                (2 * SUM(ca.nota * 100)
                + COUNT(ca.id_calificacion))
                DIV (2 * COUNT(ca.id_calificacion))
            ) / 100 AS DECIMAL(3,2)
        )
        ELSE NULL
    END AS promedio,
    CASE
        WHEN COUNT(ca.id_calificacion) < 3
            THEN 'Pendiente'
        WHEN SUM(ca.nota) * 200
             >= COUNT(ca.id_calificacion) * 599
            THEN 'Aprobado'
        ELSE 'Reprobado'
    END AS estado_academico
FROM inscripcion AS i
INNER JOIN persona AS p
    ON i.id_aprendiz = p.id_persona
INNER JOIN curso AS c
    ON i.id_curso = c.id_curso
LEFT JOIN calificacion AS ca
    ON i.id_inscripcion = ca.id_inscripcion
WHERE i.id_aprendiz = @id_aprendiz_aprobado
GROUP BY
    i.id_inscripcion,
    i.codigo,
    p.documento,
    p.nombre,
    c.nombre;

-- 8. Consultar rendimiento por curso

SELECT
    c.codigo AS codigo_curso,
    c.nombre AS curso,
    p.documento,
    p.nombre AS aprendiz,
    i.codigo AS inscripcion,
    COUNT(ca.id_calificacion) AS total_calificaciones,
    CASE
        WHEN COUNT(ca.id_calificacion) >= 3
        THEN CAST(
            (
                (2 * SUM(ca.nota * 100)
                + COUNT(ca.id_calificacion))
                DIV (2 * COUNT(ca.id_calificacion))
            ) / 100 AS DECIMAL(3,2)
        )
        ELSE NULL
    END AS promedio,
    CASE
        WHEN COUNT(ca.id_calificacion) < 3
            THEN 'Pendiente'
        WHEN SUM(ca.nota) * 200
             >= COUNT(ca.id_calificacion) * 599
            THEN 'Aprobado'
        ELSE 'Reprobado'
    END AS estado_academico
FROM inscripcion AS i
INNER JOIN persona AS p
    ON i.id_aprendiz = p.id_persona
INNER JOIN curso AS c
    ON i.id_curso = c.id_curso
LEFT JOIN calificacion AS ca
    ON i.id_inscripcion = ca.id_inscripcion
WHERE i.id_curso = @id_curso
GROUP BY
    i.id_inscripcion,
    i.codigo,
    c.codigo,
    c.nombre,
    p.documento,
    p.nombre
ORDER BY p.nombre;

-- 9. Consultar estadisticas de calificaciones

SELECT
    c.codigo,
    c.nombre AS curso,
    COUNT(ca.id_calificacion) AS total_calificaciones,
    ROUND(AVG(ca.nota), 2) AS promedio_general,
    MAX(ca.nota) AS nota_maxima,
    MIN(ca.nota) AS nota_minima
FROM curso AS c
INNER JOIN inscripcion AS i
    ON c.id_curso = i.id_curso
INNER JOIN calificacion AS ca
    ON i.id_inscripcion = ca.id_inscripcion
WHERE c.id_curso = @id_curso
GROUP BY
    c.id_curso,
    c.codigo,
    c.nombre;

-- Revertir los datos de demostracion

ROLLBACK;
