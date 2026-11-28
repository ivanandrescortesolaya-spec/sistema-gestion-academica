# Manual de ejecución de la API REST

## 1. Introducción

Este documento describe el procedimiento para ejecutar y consumir la API REST del Sistema de Gestión Académica.

La API utiliza Python, la biblioteca estándar HTTP y una base de datos MySQL administrada mediante Docker Compose.

## 2. Requisitos

- Linux o sistema compatible.
- Python 3.14.4, versión utilizada durante el desarrollo.
- Git.
- Docker.
- Docker Compose.
- Entorno virtual de Python.
- Dependencias de requirements.txt.
- curl o Postman.
- Base de datos MySQL configurada.

## 3. Clonar el repositorio

```bash
git clone https://github.com/ivanandrescortesolaya-spec/sistema-gestion-academica.git

cd sistema-gestion-academica
```

Durante el desarrollo de la fase 4:

```bash
git switch feature/rest-api
```

Después de integrar la fase en develop:

```bash
git switch develop
git pull origin develop
```

## 4. Preparar el entorno virtual

Si todavía no existe:

```bash
python3 -m venv .vend
```

Activar el entorno:

```bash
source .vend/bin/activate
```

Verificar la versión:

```bash
python3 --version
```

Instalar dependencias:

```bash
python3 -m pip install -r requirements.txt
```

Verificar dependencias:

```bash
python3 -m pip check
```

## 5. Configuración de MySQL

Si el archivo de configuración todavía no existe:

```bash
cp infra/.env.example infra/.env
chmod 600 infra/.env
```

Configurar las credenciales privadas correspondientes.

No publicar infra/.env en GitHub.

Para una instalación nueva, completar previamente la inicialización de esquemas, modalidades y permisos siguiendo los manuales de las fases 2 y 3.

La creación del contenedor no garantiza por sí sola la existencia de todas las tablas y usuarios de pruebas.

## 6. Iniciar MySQL

```bash
docker compose --env-file infra/.env \
    -f infra/docker-compose.yml up -d
```

Consultar el estado:

```bash
docker compose --env-file infra/.env \
    -f infra/docker-compose.yml ps
```

Consultar los registros:

```bash
docker logs --tail 50 academic-mysql
```

## 7. Ambientes de ejecución

### Ambiente principal

```bash
python3 main_api.py
```

Base de datos:

```text
sistema_gestion_academica
```

### Ambiente de pruebas

```bash
python3 main_api.py --pruebas
```

Base de datos:

```text
sistema_gestion_academica_test
```

Se recomienda utilizar el ambiente de pruebas durante las demostraciones que registren o modifiquen información.

### Puerto alternativo

```bash
python3 main_api.py --pruebas --puerto 8001
```

### Consultar argumentos disponibles

```bash
python3 main_api.py --help
```

## 8. Inicio del servidor

Salida ilustrativa esperada:

```text
============================================================
API REST - SISTEMA DE GESTIÓN ACADÉMICA
============================================================
Conexión con MySQL: establecida
Ambiente: PRUEBAS
URL base: http://127.0.0.1:8000/api/v1
Endpoints: 34
Estado del servidor: http://127.0.0.1:8000/api/v1/salud
Presiona Ctrl+C para detener el servidor
============================================================
```

Mantener esta terminal abierta mientras se realizan las solicitudes.

## 9. Comprobar el servidor

Desde una segunda terminal:

```bash
curl -i http://127.0.0.1:8000/api/v1/salud
```

Visualizar JSON:

```bash
curl -sS http://127.0.0.1:8000/api/v1/salud |
    python3 -m json.tool
```

## 10. Consultar los módulos

```bash
for ruta in \
    salud \
    profesores \
    aprendices \
    cursos \
    inscripciones \
    calificaciones \
    reportes/resumen \
    reportes/calificaciones
do
    echo
    echo "===== $ruta ====="

    curl -sS \
        "http://127.0.0.1:8000/api/v1/$ruta" |
        python3 -m json.tool
done
```

## 11. Demostración de operaciones académicas

Ejecutar los siguientes ejemplos exclusivamente en el ambiente de pruebas.

Los identificadores son ilustrativos y deben estar disponibles antes de realizar el registro.

Las operaciones crean registros persistentes. No se eliminan automáticamente al detener el servidor.

### Registrar profesor

```bash
curl -i -X POST \
    http://127.0.0.1:8000/api/v1/profesores \
    -H "Content-Type: application/json" \
    -d '{
        "nombre": "Profesor Demo",
        "documento": 1000000001,
        "edad": 35,
        "profesion": "Ingeniero",
        "codigo": 1001,
        "especialidad": "Python"
    }'
```

### Registrar aprendiz

```bash
curl -i -X POST \
    http://127.0.0.1:8000/api/v1/aprendices \
    -H "Content-Type: application/json" \
    -d '{
        "nombre": "Aprendiz Demo",
        "documento": 1000000002,
        "edad": 22,
        "telefono": "3001234567",
        "correo": "aprendiz@example.com",
        "direccion": "Dirección de ejemplo"
    }'
```

### Registrar curso

```bash
curl -i -X POST \
    http://127.0.0.1:8000/api/v1/cursos \
    -H "Content-Type: application/json" \
    -d '{
        "codigo": "CUR-DEMO",
        "nombre": "Python",
        "descripcion": "Curso de demostración",
        "duracion_horas": 48,
        "modalidad": "complementaria"
    }'
```

### Asignar profesor

```bash
curl -i -X PUT \
    http://127.0.0.1:8000/api/v1/cursos/CUR-DEMO/profesor \
    -H "Content-Type: application/json" \
    -d '{"documento": 1000000001}'
```

### Registrar inscripción

```bash
curl -i -X POST \
    http://127.0.0.1:8000/api/v1/inscripciones \
    -H "Content-Type: application/json" \
    -d '{
        "codigo": "INS-DEMO",
        "documento_aprendiz": 1000000002,
        "codigo_curso": "CUR-DEMO"
    }'
```

### Registrar tres calificaciones

```bash
for numero in 1 2 3
do
    nota=$((numero + 2))

    curl -i -X POST \
        http://127.0.0.1:8000/api/v1/calificaciones \
        -H "Content-Type: application/json" \
        -d "{
            \"codigo\": \"NOT-DEMO-$numero\",
            \"codigo_inscripcion\": \"INS-DEMO\",
            \"nota\": $nota
        }"

    echo
done
```

### Consultar promedio

```bash
curl -sS \
    http://127.0.0.1:8000/api/v1/inscripciones/INS-DEMO/promedio |
    python3 -m json.tool
```

Promedio esperado: 4.00.

### Modificar calificación

```bash
curl -i -X PATCH \
    http://127.0.0.1:8000/api/v1/calificaciones/NOT-DEMO-1 \
    -H "Content-Type: application/json" \
    -d '{"nota": 4.0}'
```

Consultar nuevamente el promedio.

Resultado esperado: 4.33.

### Finalizar inscripción

```bash
curl -i -X PATCH \
    http://127.0.0.1:8000/api/v1/inscripciones/INS-DEMO/estado \
    -H "Content-Type: application/json" \
    -d '{"estado": "Finalizada"}'
```

### Comprobar restricción académica

```bash
curl -i -X PATCH \
    http://127.0.0.1:8000/api/v1/calificaciones/NOT-DEMO-1 \
    -H "Content-Type: application/json" \
    -d '{"nota": 5.0}'
```

Resultado esperado: HTTP 409.

## 12. Consumir la API mediante Postman

1. Abrir Postman.
2. Crear una nueva solicitud HTTP.
3. Seleccionar el método correspondiente.
4. Introducir la URL del endpoint.
5. Para POST, PUT o PATCH, seleccionar Body.
6. Seleccionar raw y JSON.
7. Introducir el objeto JSON.
8. Presionar Send.
9. Revisar el código HTTP y la respuesta.

Puede configurarse una variable base_url con el valor:

```text
http://127.0.0.1:8000/api/v1
```

Ejemplo:

```text
{{base_url}}/profesores
```

## 13. Ejecutar el aplicativo de consola

La interfaz de consola continúa disponible:

```bash
python3 main.py
```

La consola y la API reutilizan la lógica académica y la persistencia.

## 14. Ejecutar pruebas de regresión

Validar sintaxis:

```bash
python3 -m compileall -q api main_api.py
```

Ejecutar pruebas automatizadas:

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest discover -s tests -v
```

Ejecución resumida:

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest discover -s tests -q
```

## 15. Solución de problemas

| Problema | Acción recomendada |
|---|---|
| ModuleNotFoundError | Activar entorno virtual e instalar dependencias |
| Error de conexión MySQL | Verificar contenedor y configuración |
| Puerto ocupado | Utilizar --puerto 8001 |
| HTTP 400 | Revisar estructura JSON |
| HTTP 404 | Revisar ruta e identificador |
| HTTP 405 | Revisar método HTTP |
| HTTP 409 | Revisar duplicados o estado del recurso |
| HTTP 415 | Utilizar application/json |
| HTTP 422 | Revisar campos y valores |
| HTTP 500 | Consultar registros del servidor |
| HTTP 503 | Verificar disponibilidad de MySQL |

Consultar puertos locales:

```bash
ss -ltnp
```

## 16. Detener la API

En la terminal del servidor, presionar Ctrl+C.

El servidor cerrará su socket mediante server_close.

## 17. Detener MySQL

```bash
docker compose --env-file infra/.env \
    -f infra/docker-compose.yml stop
```

Los datos persistentes se conservan.

No utilizar docker compose down -v si se desea conservar el volumen de MySQL.

## 18. Consideraciones de seguridad

- Utilizar localhost.
- No publicar credenciales.
- Utilizar la base de datos de pruebas para demostraciones.
- No exponer el servidor directamente a Internet.
- No utilizar información personal real en pruebas.
- No considerar el servidor una implementación de producción.

## 19. Conclusión

La API permite consultar y gestionar información académica mediante solicitudes HTTP, manteniendo la persistencia en MySQL y la separación de responsabilidades del aplicativo.