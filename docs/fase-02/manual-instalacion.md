
# Manual de instalación de la base de datos

## 1. Objetivo

Documentar el procedimiento necesario para instalar,
configurar y verificar la infraestructura de base de datos
del Sistema de Gestión Académica.

## 2. Requisitos

- Sistema operativo compatible con Docker.
- Git.
- Docker Engine o Docker Desktop.
- Docker Compose.
- Python 3.10 o superior.
- Bash para ejecutar los scripts automatizados.

El ambiente utilizado durante el desarrollo fue Linux Kubuntu.

## 3. Clonar el repositorio

```bash
git clone https://github.com/ivanandrescortesolaya-spec/sistema-gestion-academica.git

cd sistema-gestion-academica
```

Durante el desarrollo de la fase 2, seleccionar la rama:

```bash
git switch feature/database-implementation
```

Después de integrar la fase, se podrá utilizar la rama
que contenga los cambios aprobados.

## 4. Verificar las herramientas

```bash
git --version
python3 --version
docker --version
docker compose version
```

## 5. Crear el entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Si existe el archivo requirements.txt:

```bash
pip install -r requirements.txt
```

## 6. Configurar variables de entorno

```bash
cp infra/.env.example infra/.env
chmod 600 infra/.env
```

Editar el archivo infra/.env y reemplazar las contraseñas
de ejemplo por valores privados y seguros.

Las variables principales son:

| Variable | Descripción |
|---|---|
| MYSQL_ROOT_PASSWORD | Contraseña administrativa |
| MYSQL_DATABASE | Base principal |
| MYSQL_USER | Usuario de aplicación |
| MYSQL_PASSWORD | Contraseña de aplicación |
| MYSQL_TEST_DATABASE | Nombre de la base de pruebas |
| DB_HOST | Dirección del servidor |
| DB_PORT | Puerto del servidor |
| DB_NAME | Base principal |
| DB_USER | Usuario de conexión |
| DB_TEST_NAME | Base de pruebas |
| DB_TEST_USER | Usuario de pruebas |
| DB_TEST_PASSWORD | Contraseña de pruebas |

Los scripts Bash cargan el archivo .env mediante source.

Las contraseñas deben utilizar una sintaxis compatible
con Bash y Docker Compose.

No publicar las credenciales reales.

## 7. Validar Docker Compose

```bash
docker compose --env-file infra/.env \
    -f infra/docker-compose.yml config --quiet
```

## 8. Descargar la imagen de MySQL

```bash
docker compose --env-file infra/.env \
    -f infra/docker-compose.yml pull
```

## 9. Iniciar el servidor

```bash
docker compose --env-file infra/.env \
    -f infra/docker-compose.yml up -d
```

## 10. Verificar el contenedor

```bash
docker compose --env-file infra/.env \
    -f infra/docker-compose.yml ps
```

Esperar hasta que MySQL esté disponible.

## 11. Crear las bases de datos

```bash
docker exec -i academic-mysql \
    sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -u root' \
    < database/init.sql
```

## 12. Implementar las tablas

Base principal:

```bash
docker exec -i academic-mysql \
    sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -u root sistema_gestion_academica' \
    < database/schema.sql
```

Base de pruebas:

```bash
docker exec -i academic-mysql \
    sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -u root sistema_gestion_academica_test' \
    < database/schema.sql
```

## 13. Cargar los datos iniciales

```bash
docker exec -i academic-mysql \
    sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -u root sistema_gestion_academica' \
    < database/seed.sql

docker exec -i academic-mysql \
    sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -u root sistema_gestion_academica_test' \
    < database/seed.sql
```

## 14. Crear el usuario de pruebas

Ingresar a MySQL:

```bash
docker exec -it academic-mysql \
    sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -u root'
```

Ejecutar:

```sql
CREATE USER IF NOT EXISTS 'academic_test_user'@'%'
IDENTIFIED BY RANDOM PASSWORD;
```

Guardar de forma privada la contraseña generada en
DB_TEST_PASSWORD dentro de infra/.env.

Si el usuario ya existe, conservar su contraseña vigente
o realizar una rotación controlada.

Salir de MySQL:

```sql
EXIT;
```

## 15. Configurar privilegios

```bash
docker exec -i academic-mysql \
    sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -u root' \
    < database/permissions.sql
```

## 16. Verificar las bases de datos

```bash
docker exec -it academic-mysql \
    sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -u root'
```

```sql
SHOW DATABASES;

USE sistema_gestion_academica;

SHOW TABLES;

SELECT * FROM modalidad;
```

Deben existir las siete tablas y las dos modalidades
académicas iniciales.

## 17. Ejecutar las pruebas

```bash
chmod +x database/tests/*.sh

./database/tests/test_permissions.sh &&
./database/tests/run_tests.sh &&
./database/tests/test_persistence.sh &&
python3 -m unittest discover -s tests -v
```

Resultado esperado: 273 comprobaciones superadas.

La prueba de persistencia reinicia temporalmente MySQL.

## 18. Ejecutar el aplicativo original

```bash
python3 main.py
```

Durante la fase 2, el aplicativo original continúa
utilizando almacenamiento en memoria.

La conexión permanente con MySQL corresponde a la fase 3.

## 19. Detener los servicios

```bash
docker compose --env-file infra/.env \
    -f infra/docker-compose.yml stop
```

## 20. Reiniciar los servicios

```bash
docker compose --env-file infra/.env \
    -f infra/docker-compose.yml start
```

## 21. Solución de problemas

### Error 1045

Indica un problema de autenticación.

Verificar que las contraseñas de infra/.env coincidan
con las contraseñas almacenadas en MySQL.

Modificar el archivo .env no actualiza automáticamente
las credenciales de una base previamente inicializada.

### Error de permisos de Docker

Verificar que el servicio Docker esté iniciado y que
el usuario tenga permisos para utilizarlo.

### Puerto ocupado

Verificar la disponibilidad del puerto 3307.

Si es necesario modificarlo, actualizar DB_PORT.

### Error al cargar .env

Verificar que las asignaciones no tengan espacios
incorrectos y que las contraseñas estén correctamente
delimitadas.

## 22. Advertencias

No ejecutar docker compose down -v si se desea conservar
la información almacenada.

No eliminar manualmente el volumen persistente.

No publicar archivos con contraseñas reales.

Los cambios de contraseña deben realizarse en MySQL y
sincronizarse con la configuración privada.

## 23. Conclusión

Este procedimiento permite preparar la infraestructura
de MySQL, implementar las tablas, configurar los permisos
y ejecutar las pruebas automatizadas del proyecto.
