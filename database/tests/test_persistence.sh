
#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

set -a
source "$ROOT_DIR/infra/.env"
set +a

CONTAINER="academic-mysql"
DATABASE="sistema_gestion_academica_test"
DOCUMENT="9990000001"

: "${DB_TEST_USER:?Usuario de pruebas requerido}"
: "${DB_TEST_PASSWORD:?Contrasena de pruebas requerida}"

export MYSQL_PWD="$DB_TEST_PASSWORD"

run_sql() {
    docker exec -i -e MYSQL_PWD "$CONTAINER" \
        mysql --batch --skip-column-names \
        -u "$DB_TEST_USER" "$DATABASE" \
        -e "$1"
}

wait_mysql() {
    for ((attempt=1; attempt<=60; attempt++)); do

        if run_sql "SELECT 1;" >/dev/null 2>&1; then
            return 0
        fi

        sleep 2

    done

    echo "ERROR: MySQL no esta disponible."
    return 1
}

cleanup() {
    run_sql "DELETE FROM persona
             WHERE documento = '$DOCUMENT'
             AND nombre = 'Prueba persistencia';" \
             >/dev/null 2>&1 || {
        echo "ADVERTENCIA: No se pudo limpiar el registro de prueba."
    }
}

echo "============================================"
echo " PRUEBAS DE PERSISTENCIA DE DATOS"
echo "============================================"

wait_mysql

# Comprobar que no existe un registro previo

existing=$(run_sql "
    SELECT COUNT(*) FROM persona
    WHERE documento = '$DOCUMENT';
")

if [[ "$existing" != "0" ]]; then
    echo "ERROR: El documento de prueba ya existe."
    exit 1
fi

# PRUEBA 1: Insertar y confirmar un registro

run_sql "
    START TRANSACTION;

    INSERT INTO persona (documento, nombre, edad)
    VALUES ('$DOCUMENT', 'Prueba persistencia', 25);

    COMMIT;
"

trap cleanup EXIT

before=$(run_sql "
    SELECT COUNT(*) FROM persona
    WHERE documento = '$DOCUMENT'
      AND nombre = 'Prueba persistencia'
      AND edad = 25;
")

if [[ "$before" != "1" ]]; then
    echo "FAIL: Registro inicial"
    exit 1
fi

echo "PASS: Registro almacenado correctamente"

# PRUEBA 2: Reiniciar MySQL

echo "Reiniciando contenedor MySQL..."

docker restart "$CONTAINER" >/dev/null

wait_mysql

echo "PASS: MySQL reiniciado correctamente"

# PRUEBA 3: Verificar persistencia

after=$(run_sql "
    SELECT COUNT(*) FROM persona
    WHERE documento = '$DOCUMENT'
      AND nombre = 'Prueba persistencia'
      AND edad = 25;
")

if [[ "$after" != "1" ]]; then
    echo "FAIL: Los datos no permanecieron almacenados."
    exit 1
fi

echo "PASS: Datos conservados despues del reinicio"

# PRUEBA 4: Actualizar registro persistente

run_sql "
    UPDATE persona SET edad = 26
    WHERE documento = '$DOCUMENT';
"

updated=$(run_sql "
    SELECT edad FROM persona
    WHERE documento = '$DOCUMENT';
")

if [[ "$updated" != "26" ]]; then
    echo "FAIL: Actualizacion del registro"
    exit 1
fi

echo "PASS: Registro actualizado correctamente"

# PRUEBA 5: Eliminar datos de prueba

run_sql "
    DELETE FROM persona
    WHERE documento = '$DOCUMENT';
"

remaining=$(run_sql "
    SELECT COUNT(*) FROM persona
    WHERE documento = '$DOCUMENT';
")

if [[ "$remaining" != "0" ]]; then
    echo "FAIL: Limpieza de datos"
    exit 1
fi

trap - EXIT

echo "PASS: Datos de prueba eliminados"

echo ""
echo "============================================"
echo "Pruebas superadas: 5"
echo "Pruebas fallidas:  0"
echo "RESULTADO: PERSISTENCIA CORRECTA"
echo "============================================"
