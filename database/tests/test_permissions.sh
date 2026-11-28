
#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

set -a
source "$ROOT_DIR/infra/.env"
set +a

CONTAINER="academic-mysql"
MAIN_DB="sistema_gestion_academica"
TEST_DB="sistema_gestion_academica_test"

: "${MYSQL_USER:?Usuario requerido}"
: "${MYSQL_PASSWORD:?Contrasena requerida}"
: "${DB_TEST_USER:?Usuario de pruebas requerido}"
: "${DB_TEST_PASSWORD:?Contrasena de pruebas requerida}"

PASSED=0
FAILED=0

run_mysql() {
    local user="$1"
    local password="$2"
    local database="$3"
    local query="$4"

    MYSQL_PWD="$password" docker exec -i -e MYSQL_PWD \
        "$CONTAINER" mysql \
        --batch --skip-column-names \
        -u "$user" "$database" -e "$query"
}

expect_success() {
    local description="$1"
    shift

    if output=$(run_mysql "$@" 2>&1); then
        echo "PASS: $description"
        PASSED=$((PASSED + 1))
    else
        echo "FAIL: $description"
        printf '%s\n' "$output"
        FAILED=$((FAILED + 1))
    fi
}

expect_denied() {
    local description="$1"
    shift

    if output=$(run_mysql "$@" 2>&1); then
        echo "FAIL: $description"
        FAILED=$((FAILED + 1))
    elif grep -Eq 'ERROR (1044|1142|1143|1227|1370)' <<< "$output"; then
        echo "PASS: $description"
        PASSED=$((PASSED + 1))
    else
        echo "FAIL: Error inesperado"
        printf '%s\n' "$output"
        FAILED=$((FAILED + 1))
    fi
}

echo "============================================"
echo " PRUEBAS DE SEGURIDAD Y PERMISOS"
echo "============================================"

# PRUEBA 1: Aplicacion accede a su base de datos

expect_success \
    "Aplicacion accede a la base principal" \
    "$MYSQL_USER" "$MYSQL_PASSWORD" "$MAIN_DB" \
    "SELECT COUNT(*) FROM persona;"

# PRUEBA 2: Aplicacion no accede a pruebas

expect_denied \
    "Aplicacion sin acceso a la base de pruebas" \
    "$MYSQL_USER" "$MYSQL_PASSWORD" "$TEST_DB" \
    "SELECT COUNT(*) FROM persona;"

# PRUEBA 3: Usuario de pruebas accede a su base

expect_success \
    "Usuario de pruebas accede a su base" \
    "$DB_TEST_USER" "$DB_TEST_PASSWORD" "$TEST_DB" \
    "SELECT COUNT(*) FROM persona;"

# PRUEBA 4: Usuario de pruebas no accede a produccion

expect_denied \
    "Usuario de pruebas sin acceso a la base principal" \
    "$DB_TEST_USER" "$DB_TEST_PASSWORD" "$MAIN_DB" \
    "SELECT COUNT(*) FROM persona;"

# PRUEBA 5: Aplicacion no administra usuarios

expect_denied \
    "Aplicacion sin acceso a usuarios de MySQL" \
    "$MYSQL_USER" "$MYSQL_PASSWORD" "$MAIN_DB" \
    "SELECT User FROM mysql.user;"

# PRUEBA 6: Usuario de pruebas no administra usuarios

expect_denied \
    "Usuario de pruebas sin acceso a usuarios de MySQL" \
    "$DB_TEST_USER" "$DB_TEST_PASSWORD" "$TEST_DB" \
    "SELECT User FROM mysql.user;"

# PRUEBA 7: Aplicacion puede realizar operaciones CRUD

expect_success \
    "Aplicacion puede realizar operaciones CRUD" \
    "$MYSQL_USER" "$MYSQL_PASSWORD" "$MAIN_DB" \
    "START TRANSACTION;
     INSERT INTO persona (documento, nombre, edad)
     VALUES ('9980000001', 'Prueba permisos', 25);
     SELECT * FROM persona WHERE documento = '9980000001';
     UPDATE persona SET edad = 26
     WHERE documento = '9980000001';
     DELETE FROM persona WHERE documento = '9980000001';
     ROLLBACK;"

# PRUEBA 8: Usuario de pruebas crea tablas temporales

expect_success \
    "Usuario de pruebas puede crear tablas temporales" \
    "$DB_TEST_USER" "$DB_TEST_PASSWORD" "$TEST_DB" \
    "CREATE TEMPORARY TABLE tmp_permissions_test (id INT);
     DROP TEMPORARY TABLE tmp_permissions_test;"

# PRUEBA 9: Aplicacion no crea tablas temporales

expect_denied \
    "Aplicacion sin permiso para crear tablas temporales" \
    "$MYSQL_USER" "$MYSQL_PASSWORD" "$MAIN_DB" \
    "CREATE TEMPORARY TABLE tmp_permissions_test (id INT);"

echo ""
echo "============================================"
echo "Pruebas superadas: $PASSED"
echo "Pruebas fallidas:  $FAILED"
echo "============================================"

if [[ "$FAILED" -gt 0 ]]; then
    exit 1
fi

echo "RESULTADO: PERMISOS CORRECTOS"
