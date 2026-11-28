

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
