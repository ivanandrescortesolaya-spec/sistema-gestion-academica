
USE sistema_gestion_academica_test;

DROP PROCEDURE IF EXISTS test_calificacion;

DELIMITER $$

CREATE PROCEDURE test_calificacion()
BEGIN
    DECLARE v_modalidad INT UNSIGNED;
    DECLARE v_aprendiz INT UNSIGNED;
    DECLARE v_curso INT UNSIGNED;
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
    VALUES ('9950000001', 'Aprendiz de prueba', 22);

    SET v_aprendiz = LAST_INSERT_ID();

    INSERT INTO aprendiz
    VALUES (
        v_aprendiz, '3001234567',
        'test@example.com', 'Calle 10'
    );

    INSERT INTO curso
        (codigo, nombre, descripcion, duracion_horas, id_modalidad)
    VALUES ('TEST-CAL-C1', 'Python', 'Prueba', 120, v_modalidad);

    SET v_curso = LAST_INSERT_ID();

    INSERT INTO inscripcion (codigo, id_aprendiz, id_curso)
    VALUES ('TEST-CAL-I1', v_aprendiz, v_curso);

    SET v_inscripcion = LAST_INSERT_ID();

    -- PRUEBA 1: Nota valida

    INSERT INTO calificacion (codigo, id_inscripcion, nota)
    VALUES ('TEST-CAL-01', v_inscripcion, 4.50);

    IF NOT EXISTS (
        SELECT 1 FROM calificacion
        WHERE codigo = 'TEST-CAL-01' AND nota = 4.50
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Nota valida';
    END IF;

    SELECT 'PASS: Nota valida' AS resultado;

    -- PRUEBA 2: Limite inferior

    INSERT INTO calificacion (codigo, id_inscripcion, nota)
    VALUES ('TEST-CAL-02', v_inscripcion, 0.00);

    SELECT 'PASS: Nota minima aceptada' AS resultado;

    -- PRUEBA 3: Limite superior

    INSERT INTO calificacion (codigo, id_inscripcion, nota)
    VALUES ('TEST-CAL-03', v_inscripcion, 5.00);

    SELECT 'PASS: Nota maxima aceptada' AS resultado;

    -- PRUEBA 4: Nota negativa

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        INSERT INTO calificacion (codigo, id_inscripcion, nota)
        VALUES ('TEST-CAL-04', v_inscripcion, -0.01);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Nota negativa';
    END IF;

    SELECT 'PASS: Nota negativa rechazada' AS resultado;

    -- PRUEBA 5: Nota superior a cinco

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 3819
            SET v_error = TRUE;

        INSERT INTO calificacion (codigo, id_inscripcion, nota)
        VALUES ('TEST-CAL-05', v_inscripcion, 5.01);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Nota superior a cinco';
    END IF;

    SELECT 'PASS: Nota superior a cinco rechazada' AS resultado;

    -- PRUEBA 6: Codigo duplicado

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1062
            SET v_error = TRUE;

        INSERT INTO calificacion (codigo, id_inscripcion, nota)
        VALUES ('TEST-CAL-01', v_inscripcion, 3.00);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Codigo duplicado';
    END IF;

    SELECT 'PASS: Codigo duplicado rechazado' AS resultado;

    -- PRUEBA 7: Inscripcion inexistente

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1452
            SET v_error = TRUE;

        INSERT INTO calificacion (codigo, id_inscripcion, nota)
        VALUES ('TEST-CAL-07', 4294967295, 4.00);
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Inscripcion inexistente';
    END IF;

    SELECT 'PASS: Inscripcion inexistente rechazada' AS resultado;

    -- PRUEBA 8: Modificar nota activa

    UPDATE calificacion AS ca
    INNER JOIN inscripcion AS i
        ON ca.id_inscripcion = i.id_inscripcion
    SET ca.nota = 4.80
    WHERE ca.codigo = 'TEST-CAL-01'
      AND i.estado = 'Activa';

    IF ROW_COUNT() <> 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Modificacion de nota';
    END IF;

    SELECT 'PASS: Modificacion permitida' AS resultado;

    UPDATE inscripcion SET estado = 'Finalizada'
    WHERE id_inscripcion = v_inscripcion
      AND estado = 'Activa';

    -- PRUEBA 9: Registrar nota en inscripcion finalizada

    INSERT INTO calificacion (codigo, id_inscripcion, nota)
    SELECT 'TEST-CAL-09', id_inscripcion, 5.00
    FROM inscripcion
    WHERE id_inscripcion = v_inscripcion
      AND estado = 'Activa';

    IF ROW_COUNT() <> 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Registro en inscripcion finalizada';
    END IF;

    SELECT 'PASS: Registro no permitido impedido' AS resultado;

    -- PRUEBA 10: Modificar nota en inscripcion finalizada

    UPDATE calificacion AS ca
    INNER JOIN inscripcion AS i
        ON ca.id_inscripcion = i.id_inscripcion
    SET ca.nota = 5.00
    WHERE ca.codigo = 'TEST-CAL-01'
      AND i.estado = 'Activa';

    IF ROW_COUNT() <> 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Modificacion en inscripcion finalizada';
    END IF;

    SELECT 'PASS: Modificacion no permitida impedida' AS resultado;

    -- PRUEBA 11: Eliminar inscripcion relacionada

    SET v_error = FALSE;

    BEGIN
        DECLARE CONTINUE HANDLER FOR 1451
            SET v_error = TRUE;

        DELETE FROM inscripcion
        WHERE id_inscripcion = v_inscripcion;
    END;

    IF NOT v_error THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Eliminacion de inscripcion';
    END IF;

    SELECT 'PASS: Eliminacion de inscripcion restringida' AS resultado;

    ROLLBACK;

    SELECT '11 de 11 pruebas de calificacion superadas' AS resumen;
END$$

DELIMITER ;

CALL test_calificacion();

DROP PROCEDURE IF EXISTS test_calificacion;
