
USE sistema_gestion_academica_test;

DROP PROCEDURE IF EXISTS test_rendimiento;

DELIMITER $$

CREATE PROCEDURE test_rendimiento()
BEGIN
    DECLARE v_promedio DECIMAL(3,2);
    DECLARE v_estado VARCHAR(15);
    DECLARE v_total INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        DROP TEMPORARY TABLE IF EXISTS tmp_notas_test;
        RESIGNAL;
    END;

    DROP TEMPORARY TABLE IF EXISTS tmp_notas_test;

    CREATE TEMPORARY TABLE tmp_notas_test (
        nota DECIMAL(3,2) NOT NULL
    );

    -- PRUEBA 1: Promedio aprobado

    INSERT INTO tmp_notas_test VALUES (4.80), (3.80), (4.20);

    SELECT CAST(
        ((2 * SUM(nota * 100) + COUNT(*))
        DIV (2 * COUNT(*))) / 100 AS DECIMAL(3,2)
    ) INTO v_promedio
    FROM tmp_notas_test;

    IF NOT (v_promedio <=> 4.27) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Promedio aprobado';
    END IF;

    SELECT 'PASS: Promedio aprobado 4.27' AS resultado;

    -- PRUEBA 2: Promedio reprobado

    DELETE FROM tmp_notas_test;

    INSERT INTO tmp_notas_test VALUES (2.00), (2.50), (2.80);

    SELECT CAST(
        ((2 * SUM(nota * 100) + COUNT(*))
        DIV (2 * COUNT(*))) / 100 AS DECIMAL(3,2)
    ) INTO v_promedio
    FROM tmp_notas_test;

    IF NOT (v_promedio <=> 2.43) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Promedio reprobado';
    END IF;

    SELECT 'PASS: Promedio reprobado 2.43' AS resultado;

    -- PRUEBA 3: Aprobacion exacta

    DELETE FROM tmp_notas_test;

    INSERT INTO tmp_notas_test VALUES (3.00), (3.00), (3.00);

    SELECT CASE
        WHEN COUNT(*) < 3 THEN 'Pendiente'
        WHEN SUM(nota) * 200 >= COUNT(*) * 599 THEN 'Aprobado'
        ELSE 'Reprobado'
    END INTO v_estado
    FROM tmp_notas_test;

    IF v_estado <> 'Aprobado' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Aprobacion exacta';
    END IF;

    SELECT 'PASS: Aprobacion con 3.00' AS resultado;

    -- PRUEBA 4: Reprobacion con 2.99

    DELETE FROM tmp_notas_test;

    INSERT INTO tmp_notas_test VALUES (2.99), (2.99), (2.99);

    SELECT CASE
        WHEN COUNT(*) < 3 THEN 'Pendiente'
        WHEN SUM(nota) * 200 >= COUNT(*) * 599 THEN 'Aprobado'
        ELSE 'Reprobado'
    END INTO v_estado
    FROM tmp_notas_test;

    IF v_estado <> 'Reprobado' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Reprobacion con 2.99';
    END IF;

    SELECT 'PASS: Reprobacion con 2.99' AS resultado;

    -- PRUEBA 5: Menos de tres notas

    DELETE FROM tmp_notas_test;

    INSERT INTO tmp_notas_test VALUES (4.50), (4.00);

    SELECT
        CASE WHEN COUNT(*) >= 3
            THEN ROUND(AVG(nota), 2)
            ELSE NULL
        END,
        CASE WHEN COUNT(*) < 3
            THEN 'Pendiente'
            WHEN SUM(nota) * 200 >= COUNT(*) * 599
            THEN 'Aprobado'
            ELSE 'Reprobado'
        END
    INTO v_promedio, v_estado
    FROM tmp_notas_test;

    IF v_promedio IS NOT NULL OR v_estado <> 'Pendiente' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Rendimiento pendiente';
    END IF;

    SELECT 'PASS: Rendimiento pendiente' AS resultado;

    -- PRUEBA 6: Sin calificaciones

    DELETE FROM tmp_notas_test;

    SELECT COUNT(*), AVG(nota)
    INTO v_total, v_promedio
    FROM tmp_notas_test;

    IF v_total <> 0 OR v_promedio IS NOT NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Sin calificaciones';
    END IF;

    SELECT 'PASS: Sin calificaciones' AS resultado;

    -- PRUEBA 7: Redondeo de 2.995 a 3.00

    INSERT INTO tmp_notas_test
    VALUES (2.99), (3.00), (2.99), (3.00);

    SELECT
        CAST(
            ((2 * SUM(nota * 100) + COUNT(*))
            DIV (2 * COUNT(*))) / 100 AS DECIMAL(3,2)
        ),
        CASE
            WHEN COUNT(*) < 3 THEN 'Pendiente'
            WHEN SUM(nota) * 200 >= COUNT(*) * 599
                THEN 'Aprobado'
            ELSE 'Reprobado'
        END
    INTO v_promedio, v_estado
    FROM tmp_notas_test;

    IF NOT (v_promedio <=> 3.00)
        OR v_estado <> 'Aprobado' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Redondeo de aprobacion';
    END IF;

    SELECT 'PASS: Redondeo de 2.995 a 3.00' AS resultado;

    DROP TEMPORARY TABLE tmp_notas_test;

    SELECT '7 de 7 pruebas de rendimiento superadas' AS resumen;
END$$

DELIMITER ;

CALL test_rendimiento();

DROP PROCEDURE IF EXISTS test_rendimiento;
