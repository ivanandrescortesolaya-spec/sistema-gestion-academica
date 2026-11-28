
USE sistema_gestion_academica_test;

DROP PROCEDURE IF EXISTS test_curso;

DELIMITER $$

CREATE PROCEDURE test_curso()
BEGIN
    DECLARE v_modalidad INT UNSIGNED;
    DECLARE v_profesor INT UNSIGNED;
    DECLARE v_curso INT UNSIGNED;
    DECLARE v_error BOOLEAN DEFAULT FALSE;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    INSERT INTO modalidad (nombre)
    VALUES ('modalidad_curso_test');

    SET v_modalidad = LAST_INSERT_ID();

    INSERT INTO persona (documento, nombre, edad)
    VALUES ('9930000001', 'Profesor de prueba', 35);

    SET v_profesor = LAST_INSERT_ID();

    INSERT INTO profesor
        (id_persona, codigo, profesion, especialidad)
    VALUES (v_profesor, 9930, 'Ingeniero', 'Python');

    -- PRUEBA 1: Curso sin profesor

    INSERT INTO curso
        (codigo, nombre, descripcion, duracion_horas, id_modalidad)
    VALUES
        ('TEST-CUR-01', 'Python', 'Curso de prueba', 120, v_modalidad);

    SET v_curso = LAST_INSERT_ID();

    IF NOT EXISTS (
        SELECT 1 FROM curso
        WHERE id_curso = v_curso
          AND id_profesor IS NULL
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Curso sin profesor';
    END IF;

    SELECT 'PASS: Curso sin profesor' AS resultado;

    -- PRUEBA 2: Asignar profesor

    UPDATE curso
    SET id_profesor = v_profesor
    WHERE id_curso = v_curso;

    IF NOT EXISTS (
        SELECT 1 FROM curso
        WHERE id_curso = v_curso
          AND id_profesor = v_profesor
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Asignacion de profesor';
    END IF;

    SELECT 'PASS: Asignacion de profesor' AS resultado;

    -- PRUEBA 3: Codigo duplicado

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1062
            SET v_error = TRUE;

        INSERT INTO curso
            (codigo, nombre, descripcion, duracion_horas, id_modalidad)
        VALUES
            ('TEST-CUR-01', 'SQL', 'Prueba', 80, v_modalidad);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Codigo duplicado';
    END IF;

    SELECT 'PASS: Codigo duplicado rechazado' AS resultado;

    -- PRUEBA 4: Duracion igual a cero

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        UPDATE curso
        SET duracion_horas = 0
        WHERE id_curso = v_curso;
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Duracion igual a cero';
    END IF;

    SELECT 'PASS: Duracion igual a cero rechazada' AS resultado;

    -- PRUEBA 5: Duracion negativa

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1264
            SET v_error = TRUE;

        UPDATE curso
        SET duracion_horas = -10
        WHERE id_curso = v_curso;
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Duracion negativa';
    END IF;

    SELECT 'PASS: Duracion negativa rechazada' AS resultado;

    -- PRUEBA 6: Modalidad inexistente

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1452
            SET v_error = TRUE;

        UPDATE curso
        SET id_modalidad = 4294967295
        WHERE id_curso = v_curso;
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Modalidad inexistente';
    END IF;

    SELECT 'PASS: Modalidad inexistente rechazada' AS resultado;

    -- PRUEBA 7: Profesor inexistente

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1452
            SET v_error = TRUE;

        UPDATE curso
        SET id_profesor = 4294967295
        WHERE id_curso = v_curso;
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Profesor inexistente';
    END IF;

    SELECT 'PASS: Profesor inexistente rechazado' AS resultado;

    -- PRUEBA 8: Nombre vacio

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        UPDATE curso SET nombre = ''
        WHERE id_curso = v_curso;
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Nombre vacio';
    END IF;

    SELECT 'PASS: Nombre vacio rechazado' AS resultado;

    -- PRUEBA 9: Eliminar modalidad relacionada

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1451
            SET v_error = TRUE;

        DELETE FROM modalidad
        WHERE id_modalidad = v_modalidad;
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Eliminacion de modalidad';
    END IF;

    SELECT 'PASS: Eliminacion de modalidad restringida' AS resultado;

    -- PRUEBA 10: Eliminar profesor relacionado

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1451
            SET v_error = TRUE;

        DELETE FROM profesor
        WHERE id_persona = v_profesor;
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Eliminacion de profesor';
    END IF;

    SELECT 'PASS: Eliminacion de profesor restringida' AS resultado;

    ROLLBACK;

    SELECT '10 de 10 pruebas de curso superadas' AS resumen;
END$$

DELIMITER ;

CALL test_curso();

DROP PROCEDURE IF EXISTS test_curso;
