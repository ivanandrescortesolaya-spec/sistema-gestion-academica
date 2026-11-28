
-- ============================================
-- PRUEBAS DE INTEGRIDAD: PROFESOR
-- ============================================

USE sistema_gestion_academica_test;

DROP PROCEDURE IF EXISTS test_profesor;

DELIMITER $$

CREATE PROCEDURE test_profesor()
BEGIN
    DECLARE v_id_profesor INT UNSIGNED;
    DECLARE v_id_persona INT UNSIGNED;
    DECLARE v_error BOOLEAN DEFAULT FALSE;
    DECLARE v_total INT DEFAULT 0;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Preparar personas de demostracion

    INSERT INTO persona (documento, nombre, edad)
    VALUES ('9910000001', 'Profesor de prueba', 35);

    SET v_id_profesor = LAST_INSERT_ID();

    INSERT INTO persona (documento, nombre, edad)
    VALUES ('9910000002', 'Segunda persona', 30);

    SET v_id_persona = LAST_INSERT_ID();

    -- PRUEBA 1: Registrar profesor valido

    INSERT INTO profesor
        (id_persona, codigo, profesion, especialidad)
    VALUES
        (v_id_profesor, 991, 'Ingeniero de sistemas',
        'Programacion');

    SELECT COUNT(*) INTO v_total
    FROM profesor
    WHERE id_persona = v_id_profesor
      AND codigo = 991
      AND profesion = 'Ingeniero de sistemas'
      AND especialidad = 'Programacion';

    IF v_total <> 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Registro de profesor valido';
    END IF;

    SELECT 'PASS: Registro de profesor valido' AS resultado;

    -- PRUEBA 2: Rechazar codigo duplicado

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1062
            SET v_error = TRUE;

        INSERT INTO profesor
            (id_persona, codigo, profesion, especialidad)
        VALUES
            (v_id_persona, 991, 'Ingeniero',
            'Bases de datos');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Codigo duplicado';
    END IF;

    SELECT 'PASS: Codigo duplicado rechazado' AS resultado;

    -- PRUEBA 3: Rechazar clave primaria duplicada

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1062
            SET v_error = TRUE;

        INSERT INTO profesor
            (id_persona, codigo, profesion, especialidad)
        VALUES
            (v_id_profesor, 992, 'Ingeniero',
            'Redes');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Clave primaria duplicada';
    END IF;

    SELECT 'PASS: Clave primaria duplicada rechazada'
        AS resultado;

    -- PRUEBA 4: Rechazar persona inexistente

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1452
            SET v_error = TRUE;

        INSERT INTO profesor
            (id_persona, codigo, profesion, especialidad)
        VALUES
            (4294967295, 993, 'Ingeniero',
            'Programacion');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Persona inexistente';
    END IF;

    SELECT 'PASS: Persona inexistente rechazada'
        AS resultado;

    -- PRUEBA 5: Rechazar codigo igual a cero

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        INSERT INTO profesor
            (id_persona, codigo, profesion, especialidad)
        VALUES
            (v_id_persona, 0, 'Ingeniero',
            'Programacion');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Codigo igual a cero';
    END IF;

    SELECT 'PASS: Codigo igual a cero rechazado'
        AS resultado;

    -- PRUEBA 6: Rechazar codigo negativo

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1264
            SET v_error = TRUE;

        INSERT INTO profesor
            (id_persona, codigo, profesion, especialidad)
        VALUES
            (v_id_persona, -10, 'Ingeniero',
            'Programacion');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Codigo negativo';
    END IF;

    SELECT 'PASS: Codigo negativo rechazado' AS resultado;

    -- PRUEBA 7: Rechazar profesion vacia

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        INSERT INTO profesor
            (id_persona, codigo, profesion, especialidad)
        VALUES
            (v_id_persona, 994, '', 'Programacion');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Profesion vacia';
    END IF;

    SELECT 'PASS: Profesion vacia rechazada' AS resultado;

    -- PRUEBA 8: Rechazar especialidad vacia

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        INSERT INTO profesor
            (id_persona, codigo, profesion, especialidad)
        VALUES
            (v_id_persona, 994, 'Ingeniero', '');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Especialidad vacia';
    END IF;

    SELECT 'PASS: Especialidad vacia rechazada'
        AS resultado;

    -- PRUEBA 9: Rechazar profesion nula

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1048
            SET v_error = TRUE;

        INSERT INTO profesor
            (id_persona, codigo, profesion, especialidad)
        VALUES
            (v_id_persona, 994, NULL, 'Programacion');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Profesion nula';
    END IF;

    SELECT 'PASS: Profesion nula rechazada' AS resultado;

    -- PRUEBA 10: Impedir eliminar persona relacionada

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1451
            SET v_error = TRUE;

        DELETE FROM persona
        WHERE id_persona = v_id_profesor;
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Eliminacion de persona relacionada';
    END IF;

    SELECT 'PASS: Eliminacion de persona relacionada rechazada'
        AS resultado;

    -- Revertir datos de prueba

    ROLLBACK;

    SELECT '10 de 10 pruebas de profesor superadas' AS resumen;

END$$

DELIMITER ;

CALL test_profesor();

DROP PROCEDURE IF EXISTS test_profesor;
