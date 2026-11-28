
-- Sistema de Gestion Academica
-- Fase 2: Implementacion de la base de datos
-- Motor: MySQL 8.4 LTS

-- ============================================
-- Tabla: persona
-- ============================================

CREATE TABLE IF NOT EXISTS persona (
    id_persona INT UNSIGNED AUTO_INCREMENT,
    documento VARCHAR(20) NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    edad INT UNSIGNED NOT NULL,

    CONSTRAINT pk_persona
        PRIMARY KEY (id_persona),

    CONSTRAINT uq_persona_documento
        UNIQUE (documento),

    CONSTRAINT chk_persona_documento
        CHECK (
            documento REGEXP '^[0-9]{1,20}$'
            AND documento REGEXP '[1-9]'
        ),

    CONSTRAINT chk_persona_nombre
        CHECK (CHAR_LENGTH(TRIM(nombre)) > 0),

    CONSTRAINT chk_persona_edad
        CHECK (edad >= 0)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;

