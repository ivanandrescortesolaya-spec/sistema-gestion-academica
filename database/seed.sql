
-- Sistema de Gestion Academica
-- Fase 2: Implementacion de la base de datos
-- Datos iniciales del sistema

-- ============================================
-- Catalogo de modalidades
-- ============================================

START TRANSACTION;

INSERT INTO modalidad (nombre, descripcion)
SELECT
    'titulada',
    'Formacion orientada a la obtencion de una titulacion'
WHERE NOT EXISTS (
    SELECT 1
    FROM modalidad
    WHERE nombre = 'titulada'
);

INSERT INTO modalidad (nombre, descripcion)
SELECT
    'complementaria',
    'Formacion orientada al fortalecimiento de competencias'
WHERE NOT EXISTS (
    SELECT 1
    FROM modalidad
    WHERE nombre = 'complementaria'
);

COMMIT;
