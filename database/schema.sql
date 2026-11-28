
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


-- ============================================
-- Tabla: profesor
-- ============================================

CREATE TABLE IF NOT EXISTS profesor (
    id_persona INT UNSIGNED NOT NULL,
    codigo INT UNSIGNED NOT NULL,
    profesion VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100) NOT NULL,

    CONSTRAINT pk_profesor
        PRIMARY KEY (id_persona),

    CONSTRAINT uq_profesor_codigo
        UNIQUE (codigo),

    CONSTRAINT fk_profesor_persona
        FOREIGN KEY (id_persona)
        REFERENCES persona (id_persona)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT chk_profesor_codigo
        CHECK (codigo > 0),

    CONSTRAINT chk_profesor_profesion
        CHECK (CHAR_LENGTH(TRIM(profesion)) > 0),

    CONSTRAINT chk_profesor_especialidad
        CHECK (CHAR_LENGTH(TRIM(especialidad)) > 0)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;
