
USE sistema_gestion_academica_test;

DROP PROCEDURE IF EXISTS test_aprendiz;

DELIMITER $$

CREATE PROCEDURE test_aprendiz()
BEGIN
    DECLARE v_id INT UNSIGNED;
    DECLARE v_id_segundo INT UNSIGNED;
    DECLARE v_error BOOLEAN DEFAULT FALSE;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    INSERT INTO persona (documento, nombre, edad)
    VALUES ('9920000001', 'Aprendiz de prueba', 22);

    SET v_id = LAST_INSERT_ID();

    INSERT INTO persona (documento, nombre, edad)
    VALUES ('9920000002', 'Segunda persona', 23);

    SET v_id_segundo = LAST_INSERT_ID();

    -- PRUEBA 1: Registro valido

    INSERT INTO aprendiz
        (id_persona, telefono, correo, direccion)
    VALUES
        (v_id, '3001234567', 'test@example.com', 'Calle 10');

    IF NOT EXISTS (
        SELECT 1 FROM aprendiz WHERE id_persona = v_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Registro de aprendiz';
    END IF;

    SELECT 'PASS: Registro valido' AS resultado;

    -- PRUEBA 2: Clave primaria duplicada

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1062
            SET v_error = TRUE;

        INSERT INTO aprendiz
        VALUES (v_id, '3001234567', 'test@example.com', 'Calle 10');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Aprendiz duplicado';
    END IF;

    SELECT 'PASS: Aprendiz duplicado rechazado' AS resultado;

    -- PRUEBA 3: Persona inexistente

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1452
            SET v_error = TRUE;

        INSERT INTO aprendiz
        VALUES (
            4294967295, '3001234567',
            'test@example.com', 'Calle 10'
        );
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Persona inexistente';
    END IF;

    SELECT 'PASS: Persona inexistente rechazada' AS resultado;

    -- PRUEBA 4: Telefono vacio

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        INSERT INTO aprendiz
        VALUES (v_id_segundo, '', 'test@example.com', 'Calle 10');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Telefono vacio';
    END IF;

    SELECT 'PASS: Telefono vacio rechazado' AS resultado;

    -- PRUEBA 5: Correo vacio

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        INSERT INTO aprendiz
        VALUES (v_id_segundo, '3001234567', '', 'Calle 10');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Correo vacio';
    END IF;

    SELECT 'PASS: Correo vacio rechazado' AS resultado;

    -- PRUEBA 6: Direccion vacia

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        INSERT INTO aprendiz
        VALUES (v_id_segundo, '3001234567', 'test@example.com', '');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Direccion vacia';
    END IF;

    SELECT 'PASS: Direccion vacia rechazada' AS resultado;

    -- PRUEBA 7: Correo nulo

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1048
            SET v_error = TRUE;

        INSERT INTO aprendiz
        VALUES (v_id_segundo, '3001234567', NULL, 'Calle 10');
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Correo nulo';
    END IF;

    SELECT 'PASS: Correo nulo rechazado' AS resultado;

    -- PRUEBA 8: Eliminacion restringida

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1451
            SET v_error = TRUE;

        DELETE FROM persona WHERE id_persona = v_id;
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Eliminacion de persona';
    END IF;

    SELECT 'PASS: Eliminacion restringida' AS resultado;

    ROLLBACK;

    SELECT '8 de 8 pruebas de aprendiz superadas' AS resumen;
END$$

DELIMITER ;

CALL test_aprendiz();

DROP PROCEDURE IF EXISTS test_aprendiz;
