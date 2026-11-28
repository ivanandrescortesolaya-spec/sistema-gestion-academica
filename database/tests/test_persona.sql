
-- ============================================
-- PRUEBAS DE INTEGRIDAD: PERSONA
-- ============================================

USE sistema_gestion_academica_test;

DROP PROCEDURE IF EXISTS test_persona;

DELIMITER $$

CREATE PROCEDURE test_persona()
BEGIN
    DECLARE v_id_persona INT UNSIGNED;
    DECLARE v_error BOOLEAN DEFAULT FALSE;
    DECLARE v_total INT DEFAULT 0;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- PRUEBA 1: Registrar persona valida

    INSERT INTO persona (documento, nombre, edad)
    VALUES ('9900000001', 'Persona de prueba', 25);

    SET v_id_persona = LAST_INSERT_ID();

    SELECT COUNT(*) INTO v_total
    FROM persona
    WHERE id_persona = v_id_persona
      AND documento = '9900000001'
      AND nombre = 'Persona de prueba'
      AND edad = 25;

    IF v_total <> 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Registro de persona valida';
    END IF;

    SELECT 'PASS: Registro de persona valida' AS resultado;

    -- PRUEBA 2: Rechazar documento duplicado

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1062
            SET v_error = TRUE;

        INSERT INTO persona (documento, nombre, edad)
        VALUES ('9900000001', 'Persona duplicada', 30);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Documento duplicado';
    END IF;

    SELECT 'PASS: Documento duplicado rechazado' AS resultado;

    -- PRUEBA 3: Rechazar documento vacio

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        INSERT INTO persona (documento, nombre, edad)
        VALUES ('', 'Persona de prueba', 25);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Documento vacio';
    END IF;

    SELECT 'PASS: Documento vacio rechazado' AS resultado;

    -- PRUEBA 4: Rechazar documento con letras

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        INSERT INTO persona (documento, nombre, edad)
        VALUES ('ABC123', 'Persona de prueba', 25);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Documento con letras';
    END IF;

    SELECT 'PASS: Documento con letras rechazado' AS resultado;

    -- PRUEBA 5: Rechazar documento igual a cero

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        INSERT INTO persona (documento, nombre, edad)
        VALUES ('0000', 'Persona de prueba', 25);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Documento igual a cero';
    END IF;

    SELECT 'PASS: Documento igual a cero rechazado' AS resultado;

    -- PRUEBA 6: Rechazar nombre vacio

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        INSERT INTO persona (documento, nombre, edad)
        VALUES ('9900000002', '', 25);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Nombre vacio';
    END IF;

    SELECT 'PASS: Nombre vacio rechazado' AS resultado;

    -- PRUEBA 7: Rechazar edad negativa

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1264
            SET v_error = TRUE;

        INSERT INTO persona (documento, nombre, edad)
        VALUES ('9900000003', 'Persona de prueba', -5);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Edad negativa';
    END IF;

    SELECT 'PASS: Edad negativa rechazada' AS resultado;

    -- PRUEBA 8: Rechazar documento nulo

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1048
            SET v_error = TRUE;

        INSERT INTO persona (documento, nombre, edad)
        VALUES (NULL, 'Persona de prueba', 25);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Documento nulo';
    END IF;

    SELECT 'PASS: Documento nulo rechazado' AS resultado;

    -- Revertir datos de prueba

    ROLLBACK;

    SELECT '8 de 8 pruebas de persona superadas' AS resumen;

END$$

DELIMITER ;

CALL test_persona();

DROP PROCEDURE IF EXISTS test_persona;
