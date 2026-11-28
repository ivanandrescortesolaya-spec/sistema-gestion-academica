
USE sistema_gestion_academica_test;

DROP PROCEDURE IF EXISTS test_reportes;

DELIMITER $$

CREATE PROCEDURE test_reportes()
BEGIN
    DECLARE v_total INT;
    DECLARE v_aprobadas INT;
    DECLARE v_reprobadas INT;
    DECLARE v_pendientes INT;
    DECLARE v_promedio DECIMAL(3,2);
    DECLARE v_maxima DECIMAL(3,2);
    DECLARE v_minima DECIMAL(3,2);
    DECLARE v_porcentaje DECIMAL(5,2);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        DROP TEMPORARY TABLE IF EXISTS tmp_reportes_test;
        RESIGNAL;
    END;

    DROP TEMPORARY TABLE IF EXISTS tmp_reportes_test;

    CREATE TEMPORARY TABLE tmp_reportes_test (
        id INT AUTO_INCREMENT PRIMARY KEY,
        promedio DECIMAL(3,2),
        estado VARCHAR(15) NOT NULL
    );

    INSERT INTO tmp_reportes_test (promedio, estado)
    VALUES
        (4.50, 'Aprobado'),
        (3.80, 'Aprobado'),
        (3.00, 'Aprobado'),
        (2.00, 'Reprobado'),
        (NULL, 'Pendiente');

    -- PRUEBA 1: Conteo general

    SELECT COUNT(*) INTO v_total
    FROM tmp_reportes_test;

    IF v_total <> 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Conteo general';
    END IF;

    SELECT 'PASS: Conteo general' AS resultado;

    -- PRUEBA 2: Conteo por estado academico

    SELECT
        COUNT(CASE WHEN estado = 'Aprobado' THEN 1 END),
        COUNT(CASE WHEN estado = 'Reprobado' THEN 1 END),
        COUNT(CASE WHEN estado = 'Pendiente' THEN 1 END)
    INTO v_aprobadas, v_reprobadas, v_pendientes
    FROM tmp_reportes_test;

    IF v_aprobadas <> 3
        OR v_reprobadas <> 1
        OR v_pendientes <> 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Conteo por estado';
    END IF;

    SELECT 'PASS: Conteo por estado' AS resultado;

    -- PRUEBA 3: Promedio general

    SELECT ROUND(AVG(promedio), 2)
    INTO v_promedio
    FROM tmp_reportes_test;

    IF NOT (v_promedio <=> 3.33) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Promedio general';
    END IF;

    SELECT 'PASS: Promedio general' AS resultado;

    -- PRUEBA 4: Promedio maximo

    SELECT MAX(promedio) INTO v_maxima
    FROM tmp_reportes_test;

    IF NOT (v_maxima <=> 4.50) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Promedio maximo';
    END IF;

    SELECT 'PASS: Promedio maximo' AS resultado;

    -- PRUEBA 5: Promedio minimo

    SELECT MIN(promedio) INTO v_minima
    FROM tmp_reportes_test;

    IF NOT (v_minima <=> 2.00) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Promedio minimo';
    END IF;

    SELECT 'PASS: Promedio minimo' AS resultado;

    -- PRUEBA 6: Porcentaje de aprobacion

    SELECT COALESCE(
        ROUND(
            100.0 * COUNT(
                CASE WHEN estado = 'Aprobado' THEN 1 END
            ) / NULLIF(
                COUNT(
                    CASE WHEN estado IN ('Aprobado', 'Reprobado')
                    THEN 1 END
                ), 0
            ), 2
        ), 0
    ) INTO v_porcentaje
    FROM tmp_reportes_test;

    IF NOT (v_porcentaje <=> 75.00) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Porcentaje de aprobacion';
    END IF;

    SELECT 'PASS: Porcentaje de aprobacion 75%' AS resultado;

    -- PRUEBA 7: Reporte sin registros

    DELETE FROM tmp_reportes_test;

    SELECT
        COUNT(*),
        COALESCE(
            ROUND(
                100.0 * COUNT(
                    CASE WHEN estado = 'Aprobado' THEN 1 END
                ) / NULLIF(
                    COUNT(
                        CASE WHEN estado IN ('Aprobado', 'Reprobado')
                        THEN 1 END
                    ), 0
                ), 2
            ), 0
        )
    INTO v_total, v_porcentaje
    FROM tmp_reportes_test;

    IF v_total <> 0 OR v_porcentaje <> 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'FAIL: Reporte vacio';
    END IF;

    SELECT 'PASS: Reporte vacio sin division por cero' AS resultado;

    DROP TEMPORARY TABLE tmp_reportes_test;

    SELECT '7 de 7 pruebas de reportes superadas' AS resumen;
END$$

DELIMITER ;

CALL test_reportes();

DROP PROCEDURE IF EXISTS test_reportes;
