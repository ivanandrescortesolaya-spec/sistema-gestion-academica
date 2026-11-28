-- ============================================
-- CONFIGURACION DE USUARIOS Y PRIVILEGIOS
-- ============================================

-- Usuario de la aplicacion

REVOKE ALL PRIVILEGES, GRANT OPTION
FROM 'academic_user'@'%';

GRANT SELECT, INSERT, UPDATE, DELETE
ON `sistema\_gestion\_academica`.*
TO 'academic_user'@'%';

-- Usuario de pruebas

REVOKE ALL PRIVILEGES, GRANT OPTION
FROM 'academic_test_user'@'%';

GRANT
    SELECT,
    INSERT,
    UPDATE,
    DELETE,
    CREATE ROUTINE,
    ALTER ROUTINE,
    EXECUTE,
    CREATE TEMPORARY TABLES
ON `sistema\_gestion\_academica\_test`.*
TO 'academic_test_user'@'%';

-- Verificar privilegios

SHOW GRANTS FOR 'academic_user'@'%';

SHOW GRANTS FOR 'academic_test_user'@'%';