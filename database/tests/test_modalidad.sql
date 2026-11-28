
USE sistema_gestion_academica_test;

DROP PROCEDURE IF EXISTS test_modalidad;

DELIMITER $$

CREATE PROCEDURE test_modalidad()
BEGIN
    DECLARE v_id INT UNSIGNED;
    DECLARE v_error BOOLEAN DEFAULT FALSE;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- PRUEBA 1: Modalidades iniciales

    IF (
        SELECT COUNT(*)
        FROM modalidad
        WHERE nombre IN ('titulada', 'complementaria')
    ) <> 2 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Modalidades iniciales';
    END IF;

    SELECT 'PASS: Modalidades iniciales' AS resultado;

    -- PRUEBA 2: Registro valido

    INSERT INTO modalidad (nombre, descripcion)
    VALUES ('modalidad_test', 'Modalidad de prueba');

    SET v_id = LAST_INSERT_ID();

    IF NOT EXISTS (
        SELECT 1 FROM modalidad WHERE id_modalidad = v_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Registro de modalidad';
    END IF;

    SELECT 'PASS: Registro valido' AS resultado;

    -- PRUEBA 3: Nombre duplicado

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1062
            SET v_error = TRUE;

        INSERT INTO modalidad (nombre)
        VALUES ('modalidad_test');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Modalidad duplicada';
    END IF;

    SELECT 'PASS: Modalidad duplicada rechazada' AS resultado;

    -- PRUEBA 4: Nombre vacio

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        INSERT INTO modalidad (nombre) VALUES ('');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Nombre vacio';
    END IF;

    SELECT 'PASS: Nombre vacio rechazado' AS resultado;

    -- PRUEBA 5: Nombre nulo

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1048
            SET v_error = TRUE;

        INSERT INTO modalidad (nombre) VALUES (NULL);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Nombre nulo';
    END IF;

    SELECT 'PASS: Nombre nulo rechazado' AS resultado;

    -- PRUEBA 6: Descripcion opcional

    UPDATE modalidad
    SET descripcion = NULL
    WHERE id_modalidad = v_id;

    IF NOT EXISTS (
        SELECT 1 FROM modalidad
        WHERE id_modalidad = v_id
          AND descripcion IS NULL
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Descripcion opcional';
    END IF;

    SELECT 'PASS: Descripcion opcional' AS resultado;

    ROLLBACK;

    SELECT '6 de 6 pruebas de modalidad superadas' AS resumen;
END$$

DELIMITER ;

CALL test_modalidad();

DROP PROCEDURE IF EXISTS test_modalidad;
