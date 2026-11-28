
#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TEST_DIR="$ROOT_DIR/database/tests"

CONTAINER="academic-mysql"
DATABASE="sistema_gestion_academica_test"

FILES=(
    test_persona.sql
    test_profesor.sql
    test_aprendiz.sql
    test_modalidad.sql
    test_curso.sql
    test_inscripcion.sql
    test_calificacion.sql
    test_rendimiento.sql
    test_reportes.sql
)

EXPECTED=(8 10 8 6 10 10 11 7 7)

TOTAL_FILES=0
PASSED_FILES=0
FAILED_FILES=0
TOTAL_TESTS=0

echo "============================================"
echo " SISTEMA DE GESTION ACADEMICA"
echo " PRUEBAS AUTOMATIZADAS DE BASE DE DATOS"
echo "============================================"

if [[ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER" 2>/dev/null)" != "true" ]]; then
    echo "ERROR: El contenedor MySQL no esta ejecutandose."
    exit 1
fi

for index in "${!FILES[@]}"; do

    file="${FILES[$index]}"
    expected="${EXPECTED[$index]}"
    TOTAL_FILES=$((TOTAL_FILES + 1))

    echo ""
    echo "--------------------------------------------"
    echo "Ejecutando: $file"
    echo "--------------------------------------------"

    if [[ ! -f "$TEST_DIR/$file" ]]; then
        echo "ERROR: Archivo no encontrado."
        FAILED_FILES=$((FAILED_FILES + 1))
        continue
    fi

    if output=$(docker exec -i "$CONTAINER" \
        sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql \
        --batch --skip-column-names -u root "$1"' \
        sh "$DATABASE" < "$TEST_DIR/$file" 2>&1); then

        printf '%s\n' "$output"

        count=$(printf '%s\n' "$output" | grep -c '^PASS:' || true)

        TOTAL_TESTS=$((TOTAL_TESTS + count))

        if [[ "$count" -eq "$expected" ]]; then
            PASSED_FILES=$((PASSED_FILES + 1))
            echo "OK: $file ($count/$expected)"
        else
            FAILED_FILES=$((FAILED_FILES + 1))
            echo "ERROR: Cantidad de pruebas inesperada."
        fi

    else
        printf '%s\n' "$output"
        count=$(printf '%s\n' "$output" | grep -c '^PASS:' || true)
        TOTAL_TESTS=$((TOTAL_TESTS + count))
        FAILED_FILES=$((FAILED_FILES + 1))
        echo "ERROR: $file"
    fi

done

echo ""
echo "============================================"
echo " RESUMEN FINAL"
echo "============================================"
echo "Archivos ejecutados: $TOTAL_FILES"
echo "Archivos superados:  $PASSED_FILES"
echo "Archivos fallidos:   $FAILED_FILES"
echo "Pruebas superadas:   $TOTAL_TESTS"
echo "============================================"

if [[ "$FAILED_FILES" -gt 0 ]]; then
    echo "RESULTADO: PRUEBAS FALLIDAS"
    exit 1
fi

echo "RESULTADO: TODAS LAS PRUEBAS SUPERADAS"

exit 0
