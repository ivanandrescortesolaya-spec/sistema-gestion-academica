# Integración de Python con MySQL

## 1. Introducción

Este documento describe la configuración y ejecución
del Sistema de Gestión Académica con persistencia
relacional mediante MySQL.

## 2. Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python | Lenguaje de programación |
| MySQL 8.4 | Sistema gestor de base de datos |
| Docker | Ejecución del servidor MySQL |
| Docker Compose | Administración de infraestructura |
| mysql-connector-python | Conector de Python con MySQL |
| python-dotenv | Carga de variables de entorno |
| unittest | Pruebas automatizadas |
| Git y GitHub | Control de versiones |

## 3. Requisitos previos

- Python instalado.
- Git instalado.
- Docker instalado y operativo.
- Docker Compose disponible.
- Base de datos configurada según la fase 2.
- Credenciales de aplicación y pruebas configuradas.

## 4. Obtener el proyecto

```bash
git clone https://github.com/ivanandrescortesolaya-spec/sistema-gestion-academica.git

cd sistema-gestion-academica

git switch feature/database-persistence
```

Una vez integrada la rama, también podrá utilizarse
la rama que contenga estos cambios.

## 5. Crear el entorno virtual

```bash
python3 -m venv .vend
source .vend/bin/activate
```

## 6. Instalar dependencias

```bash
python3 -m pip install -r requirements.txt
python3 -m pip check
```

Dependencias registradas:

```text
mysql-connector-python==26.10.0
python-dotenv==1.2.4
```

## 7. Configuración del ambiente

El archivo infra/.env contiene la configuración
privada de la infraestructura.

Para una instalación nueva:

```bash
cp infra/.env.example infra/.env
chmod 600 infra/.env
```

No se debe sobrescribir un archivo .env existente.

Las contraseñas deben corresponder a los usuarios
realmente configurados en MySQL.

## 8. Variables de entorno

| Variable | Descripción |
|---|---|
| DB_HOST | Dirección del servidor |
| DB_PORT | Puerto de conexión |
| DB_NAME | Base de datos principal |
| DB_USER | Usuario de aplicación |
| MYSQL_PASSWORD | Contraseña de aplicación |
| DB_TEST_NAME | Base de datos de pruebas |
| DB_TEST_USER | Usuario de pruebas |
| DB_TEST_PASSWORD | Contraseña de pruebas |

Configuración local utilizada:

```text
Host: 127.0.0.1
Puerto: 3307
Base principal: sistema_gestion_academica
Base de pruebas: sistema_gestion_academica_test
Usuario principal: academic_user
Usuario de pruebas: academic_test_user
```

Las contraseñas no se incluyen en la documentación.

## 9. Iniciar MySQL

```bash
docker compose \
    --env-file infra/.env \
    -f infra/docker-compose.yml \
    up -d
```

Verificar el estado:

```bash
docker compose \
    --env-file infra/.env \
    -f infra/docker-compose.yml \
    ps
```

El contenedor debe encontrarse operativo.

En instalaciones nuevas deben ejecutarse los
procedimientos de inicialización, esquema, datos
iniciales y permisos descritos en la documentación
de la fase 2.

## 10. Configuración de Python

ConfiguracionBD carga las variables de entorno
y valida la configuración del ambiente.

La aplicación dispone de dos ambientes:

| Ambiente | Base de datos |
|---|---|
| Aplicación | sistema_gestion_academica |
| Pruebas | sistema_gestion_academica_test |

No se utiliza root como usuario del aplicativo.

## 11. Verificar la conexión

```bash
python3 - <<'PY'
from persistencia import ConfiguracionBD, ConexionMySQL

for pruebas in (False, True):
    config = ConfiguracionBD.desde_entorno(pruebas=pruebas)
    conexion = ConexionMySQL(config)

    print(config.base_datos, conexion.verificar_conexion())
PY
```

Ambas conexiones deben retornar True.

## 12. Ejecutar el aplicativo

```bash
python3 main.py
```

El aplicativo construye el sistema mediante
crear_sistema_mysql().

La fábrica verifica la conexión e inyecta los
repositorios persistentes en GestionAcademica.

## 13. Menú principal

```text
====================================
   SISTEMA DE GESTIÓN ACADÉMICA
====================================
1. Gestión de profesores
2. Gestión de aprendices
3. Gestión de cursos
4. Gestión de inscripciones
5. Gestión de calificaciones
6. Reportes académicos
0. Salir
```

## 14. Operaciones persistentes

El sistema permite:

- Registrar y consultar profesores.
- Registrar y consultar aprendices.
- Registrar y consultar cursos.
- Asignar profesores a cursos.
- Registrar inscripciones.
- Cancelar y finalizar inscripciones.
- Registrar y modificar calificaciones.
- Consultar promedios y rendimiento.
- Generar reportes académicos.

## 15. Verificar persistencia

1. Ejecutar el aplicativo.
2. Registrar información de prueba autorizada.
3. Salir del programa.
4. Ejecutar nuevamente el aplicativo.
5. Consultar la información registrada.
6. Comprobar que los datos permanecen almacenados.

Las pruebas automatizadas utilizan una base
independiente de la base principal.

## 16. Ejecutar pruebas originales

```bash
python3 -m unittest discover -s tests -v
```

Las pruebas MySQL se omiten cuando no se habilita
la variable RUN_MYSQL_TESTS.

## 17. Ejecutar todas las pruebas

```bash
RUN_MYSQL_TESTS=1 python3 -m unittest discover -s tests -v
```

Este comando ejecuta las pruebas originales
y las pruebas de integración.

## 18. Solución de problemas

| Problema | Verificación |
|---|---|
| Error de conexión | Revisar el contenedor MySQL. |
| Puerto ocupado | Revisar la configuración del puerto. |
| Acceso denegado | Verificar usuario y contraseña. |
| Base inexistente | Ejecutar la inicialización de fase 2. |
| Módulo no encontrado | Activar el entorno e instalar dependencias. |
| Pruebas omitidas | Habilitar RUN_MYSQL_TESTS=1. |

## 19. Detener MySQL

```bash
docker compose \
    --env-file infra/.env \
    -f infra/docker-compose.yml \
    stop
```

No utilizar down -v si se desea conservar
el volumen de datos.

## 20. Seguridad de la configuración

No deben publicarse:

- Archivos .env.
- Contraseñas.
- Entornos virtuales.
- Copias privadas de bases de datos.
- Información sensible de usuarios.

## 21. Conclusión

La integración permite ejecutar el aplicativo
Python con almacenamiento permanente mediante
MySQL, conservando la lógica académica y la
estructura modular del proyecto.