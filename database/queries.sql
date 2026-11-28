

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
