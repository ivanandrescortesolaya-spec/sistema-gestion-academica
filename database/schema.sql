
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


-- ============================================
-- Tabla: aprendiz
-- ============================================

CREATE TABLE IF NOT EXISTS aprendiz (
    id_persona INT UNSIGNED NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(254) NOT NULL,
    direccion VARCHAR(200) NOT NULL,

    CONSTRAINT pk_aprendiz
        PRIMARY KEY (id_persona),

    CONSTRAINT fk_aprendiz_persona
        FOREIGN KEY (id_persona)
        REFERENCES persona (id_persona)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT chk_aprendiz_telefono
        CHECK (CHAR_LENGTH(TRIM(telefono)) > 0),

    CONSTRAINT chk_aprendiz_correo
        CHECK (CHAR_LENGTH(TRIM(correo)) > 0),

    CONSTRAINT chk_aprendiz_direccion
        CHECK (CHAR_LENGTH(TRIM(direccion)) > 0)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;


-- ============================================
-- Tabla: modalidad
-- ============================================

CREATE TABLE IF NOT EXISTS modalidad (
    id_modalidad INT UNSIGNED AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255) DEFAULT NULL,

    CONSTRAINT pk_modalidad
        PRIMARY KEY (id_modalidad),

    CONSTRAINT uq_modalidad_nombre
        UNIQUE (nombre),

    CONSTRAINT chk_modalidad_nombre
        CHECK (CHAR_LENGTH(TRIM(nombre)) > 0)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;


-- ============================================
-- Tabla: curso
-- ============================================

CREATE TABLE IF NOT EXISTS curso (
    id_curso INT UNSIGNED AUTO_INCREMENT,
    codigo VARCHAR(30) COLLATE utf8mb4_0900_bin NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    duracion_horas INT UNSIGNED NOT NULL,
    id_modalidad INT UNSIGNED NOT NULL,
    id_profesor INT UNSIGNED DEFAULT NULL,

    CONSTRAINT pk_curso
        PRIMARY KEY (id_curso),

    CONSTRAINT uq_curso_codigo
        UNIQUE (codigo),

    CONSTRAINT fk_curso_modalidad
        FOREIGN KEY (id_modalidad)
        REFERENCES modalidad (id_modalidad)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT fk_curso_profesor
        FOREIGN KEY (id_profesor)
        REFERENCES profesor (id_persona)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT chk_curso_codigo
        CHECK (CHAR_LENGTH(TRIM(codigo)) > 0),

    CONSTRAINT chk_curso_nombre
        CHECK (CHAR_LENGTH(TRIM(nombre)) > 0),

    CONSTRAINT chk_curso_descripcion
        CHECK (CHAR_LENGTH(TRIM(descripcion)) > 0),

    CONSTRAINT chk_curso_duracion
        CHECK (duracion_horas > 0),

    INDEX idx_curso_modalidad (id_modalidad),
    INDEX idx_curso_profesor (id_profesor)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;


-- ============================================
-- Tabla: inscripcion
-- ============================================

CREATE TABLE IF NOT EXISTS inscripcion (
    id_inscripcion INT UNSIGNED AUTO_INCREMENT,
    codigo VARCHAR(30) COLLATE utf8mb4_0900_bin NOT NULL,
    id_aprendiz INT UNSIGNED NOT NULL,
    id_curso INT UNSIGNED NOT NULL,
    fecha_inscripcion DATE NOT NULL DEFAULT (CURRENT_DATE),
    estado VARCHAR(15) COLLATE utf8mb4_0900_bin
        NOT NULL DEFAULT 'Activa',

    CONSTRAINT pk_inscripcion
        PRIMARY KEY (id_inscripcion),

    CONSTRAINT uq_inscripcion_codigo
        UNIQUE (codigo),

    CONSTRAINT uq_inscripcion_aprendiz_curso
        UNIQUE (id_aprendiz, id_curso),

    CONSTRAINT fk_inscripcion_aprendiz
        FOREIGN KEY (id_aprendiz)
        REFERENCES aprendiz (id_persona)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT fk_inscripcion_curso
        FOREIGN KEY (id_curso)
        REFERENCES curso (id_curso)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT chk_inscripcion_codigo
        CHECK (CHAR_LENGTH(TRIM(codigo)) > 0),

    CONSTRAINT chk_inscripcion_estado
        CHECK (estado IN ('Activa', 'Cancelada', 'Finalizada')),

    INDEX idx_inscripcion_curso (id_curso)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;


-- ============================================
-- Tabla: calificacion
-- ============================================

CREATE TABLE IF NOT EXISTS calificacion (
    id_calificacion INT UNSIGNED AUTO_INCREMENT,
    codigo VARCHAR(30) COLLATE utf8mb4_0900_bin NOT NULL,
    id_inscripcion INT UNSIGNED NOT NULL,
    nota DECIMAL(3,2) NOT NULL,
    fecha DATE NOT NULL DEFAULT (CURRENT_DATE),

    CONSTRAINT pk_calificacion
        PRIMARY KEY (id_calificacion),

    CONSTRAINT uq_calificacion_codigo
        UNIQUE (codigo),

    CONSTRAINT fk_calificacion_inscripcion
        FOREIGN KEY (id_inscripcion)
        REFERENCES inscripcion (id_inscripcion)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT chk_calificacion_codigo
        CHECK (CHAR_LENGTH(TRIM(codigo)) > 0),

    CONSTRAINT chk_calificacion_nota
        CHECK (nota BETWEEN 0.00 AND 5.00),

    INDEX idx_calificacion_inscripcion (id_inscripcion)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;
