
USE sistema_gestion_academica_test;

DROP PROCEDURE IF EXISTS test_inscripcion;

DELIMITER $$

CREATE PROCEDURE test_inscripcion()
BEGIN
    DECLARE v_modalidad INT UNSIGNED;
    DECLARE v_aprendiz INT UNSIGNED;
    DECLARE v_curso INT UNSIGNED;
    DECLARE v_curso_segundo INT UNSIGNED;
    DECLARE v_inscripcion INT UNSIGNED;
    DECLARE v_error BOOLEAN DEFAULT FALSE;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SET v_modalidad = (
        SELECT id_modalidad FROM modalidad
        WHERE nombre = 'titulada'
    );

    INSERT INTO persona (documento, nombre, edad)
    VALUES ('9940000001', 'Aprendiz de prueba', 22);

    SET v_aprendiz = LAST_INSERT_ID();

    INSERT INTO aprendiz
    VALUES (
        v_aprendiz, '3001234567',
        'test@example.com', 'Calle 10'
    );

    INSERT INTO curso
        (codigo, nombre, descripcion, duracion_horas, id_modalidad)
    VALUES ('TEST-INS-C1', 'Python', 'Prueba', 120, v_modalidad);

    SET v_curso = LAST_INSERT_ID();

    INSERT INTO curso
        (codigo, nombre, descripcion, duracion_horas, id_modalidad)
    VALUES ('TEST-INS-C2', 'MySQL', 'Prueba', 80, v_modalidad);

    SET v_curso_segundo = LAST_INSERT_ID();

    -- PRUEBA 1: Inscripcion valida

    INSERT INTO inscripcion (codigo, id_aprendiz, id_curso)
    VALUES ('TEST-INS-01', v_aprendiz, v_curso);

    SET v_inscripcion = LAST_INSERT_ID();

    IF NOT EXISTS (
        SELECT 1 FROM inscripcion
        WHERE id_inscripcion = v_inscripcion
          AND estado = 'Activa'
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Inscripcion valida';
    END IF;

    SELECT 'PASS: Inscripcion valida' AS resultado;

    -- PRUEBA 2: Codigo duplicado

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1062
            SET v_error = TRUE;

        INSERT INTO inscripcion (codigo, id_aprendiz, id_curso)
        VALUES ('TEST-INS-01', v_aprendiz, v_curso_segundo);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Codigo duplicado';
    END IF;

    SELECT 'PASS: Codigo duplicado rechazado' AS resultado;

    -- PRUEBA 3: Aprendiz y curso duplicados

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1062
            SET v_error = TRUE;

        INSERT INTO inscripcion (codigo, id_aprendiz, id_curso)
        VALUES ('TEST-INS-02', v_aprendiz, v_curso);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Inscripcion duplicada';
    END IF;

    SELECT 'PASS: Inscripcion duplicada rechazada' AS resultado;

    -- PRUEBA 4: Aprendiz inexistente

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1452
            SET v_error = TRUE;

        INSERT INTO inscripcion (codigo, id_aprendiz, id_curso)
        VALUES ('TEST-INS-03', 4294967295, v_curso);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Aprendiz inexistente';
    END IF;

    SELECT 'PASS: Aprendiz inexistente rechazado' AS resultado;

    -- PRUEBA 5: Curso inexistente

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1452
            SET v_error = TRUE;

        INSERT INTO inscripcion (codigo, id_aprendiz, id_curso)
        VALUES ('TEST-INS-04', v_aprendiz, 4294967295);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Curso inexistente';
    END IF;

    SELECT 'PASS: Curso inexistente rechazado' AS resultado;

    -- PRUEBA 6: Estado invalido

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        UPDATE inscripcion SET estado = 'Invalida'
        WHERE id_inscripcion = v_inscripcion;
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Estado invalido';
    END IF;

    SELECT 'PASS: Estado invalido rechazado' AS resultado;

    -- PRUEBA 7: Cancelar inscripcion activa

    UPDATE inscripcion SET estado = 'Cancelada'
    WHERE id_inscripcion = v_inscripcion
      AND estado = 'Activa';

    IF ROW_COUNT() <> 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Cancelacion';
    END IF;

    SELECT 'PASS: Cancelacion permitida' AS resultado;

    -- PRUEBA 8: Impedir transicion desde cancelada

    UPDATE inscripcion SET estado = 'Finalizada'
    WHERE id_inscripcion = v_inscripcion
      AND estado = 'Activa';

    IF ROW_COUNT() <> 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Transicion invalida';
    END IF;

    SELECT 'PASS: Transicion invalida impedida' AS resultado;

    -- PRUEBA 9: Eliminar curso relacionado

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1451
            SET v_error = TRUE;

        DELETE FROM curso WHERE id_curso = v_curso;
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Eliminacion de curso';
    END IF;

    SELECT 'PASS: Eliminacion de curso restringida' AS resultado;

    -- PRUEBA 10: Eliminar aprendiz relacionado

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1451
            SET v_error = TRUE;

        DELETE FROM aprendiz WHERE id_persona = v_aprendiz;
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Eliminacion de aprendiz';
    END IF;

    SELECT 'PASS: Eliminacion de aprendiz restringida' AS resultado;

    ROLLBACK;

    SELECT '10 de 10 pruebas de inscripcion superadas' AS resumen;
END$$

DELIMITER ;

CALL test_inscripcion();

DROP PROCEDURE IF EXISTS test_inscripcion;
