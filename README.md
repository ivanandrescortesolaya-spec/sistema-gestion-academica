# Sistema de Gestión Académica

## Descripción

Sistema de gestión académica desarrollado en Python mediante
Programación Orientada a Objetos (POO), siguiendo los principios
SOLID y utilizando una interfaz interactiva por consola.

El sistema permite administrar profesores, aprendices y cursos.
También contempla la gestión de inscripciones, calificaciones
y reportes académicos.

La información se almacena temporalmente en memoria, sin utilizar
bases de datos ni frameworks externos.

## Objetivo general

Desarrollar un sistema académico modular que permita gestionar
información académica mediante buenas prácticas de programación,
aplicando los pilares de POO y los principios SOLID.

## Tecnologías utilizadas

- Python 3.10 o superior.
- Programación Orientada a Objetos.
- Unittest.
- Git.
- GitHub.
- Visual Studio Code.

## Funcionalidades implementadas

### Gestión de profesores

- Registrar profesores.
- Buscar profesores por documento.
- Listar profesores registrados.
- Validar información personal y profesional.
- Evitar registros duplicados.
- Consultar cursos asignados.

### Gestión de aprendices

- Registrar aprendices.
- Buscar aprendices por documento.
- Listar aprendices registrados.
- Validar información personal y de contacto.
- Evitar registros duplicados.

### Gestión de cursos

- Registrar cursos.
- Buscar cursos por código.
- Listar cursos registrados.
- Gestionar modalidades titulada y complementaria.
- Asignar profesores registrados.
- Validar duración y datos del curso.
- Evitar códigos duplicados.

### Gestión de inscripciones

Módulo a cargo del integrante 2, pendiente de integración.

### Gestión de calificaciones

Módulo a cargo del integrante 2, pendiente de integración.

### Reportes académicos

- Cantidad de profesores registrados.
- Cantidad de aprendices registrados.
- Cantidad de cursos registrados.
- Consulta de cursos asignados a profesores.

## Estructura del proyecto

```text
sistema-gestion-academica/
│
├── personas/
│   ├── __init__.py
│   ├── personas.py
│   ├── profesores.py
│   ├── gestion_profesores.py
│   ├── aprendices.py
│   └── gestion_aprendices.py
│
├── cursos/
│   ├── __init__.py
│   ├── curso.py
│   └── gestion_cursos.py
│
├── inscripciones/
│
├── calificaciones/
│
├── tests/
│   ├── __init__.py
│   ├── test_personas.py
│   ├── test_profesores.py
│   ├── test_aprendices.py
│   ├── test_cursos.py
│   ├── test_gestion_academica.py
│   └── test_main.py
│
├── gestion_academica.py
├── main.py
├── .gitignore
└── README.md
```

## Programación Orientada a Objetos

### Encapsulamiento

Se utilizan atributos privados, propiedades y métodos de
validación para controlar el acceso a la información.

### Abstracción

La clase Persona define una estructura común mediante
clases y métodos abstractos.

### Herencia

Las clases Profesor y Aprendiz heredan los atributos y
comportamientos de la clase Persona.

### Polimorfismo

Las clases Profesor y Aprendiz implementan sus propias
versiones de los métodos:

- mostrar_informacion()
- obtener_rol()

## Principios SOLID

### S - Single Responsibility Principle (SRP)

Cada clase tiene una responsabilidad definida.

Las entidades representan información académica, los gestores
administran las operaciones y el menú controla la interacción
con el usuario.

### O - Open/Closed Principle (OCP)

La estructura modular facilita la incorporación de nuevas
funcionalidades.

La extensibilidad de las modalidades de cursos está pendiente
de revisión.

### L - Liskov Substitution Principle (LSP)

Las clases Profesor y Aprendiz pueden utilizarse mediante
el contrato definido por la clase Persona.

### I - Interface Segregation Principle (ISP)

Se busca mantener contratos pequeños y específicos para
evitar dependencias innecesarias.

Pendiente de revisión final.

### D - Dependency Inversion Principle (DIP)

Se utiliza la clase GestionAcademica para centralizar las
operaciones del sistema.

La dependencia de abstracciones de almacenamiento está
pendiente de revisión.

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/ivanandrescortesolaya-spec/sistema-gestion-academica.git
```

Ingresar al directorio:

```bash
cd sistema-gestion-academica
```

Cambiar a la rama de desarrollo:

```bash
git switch develop
```

Verificar la versión de Python:

```bash
python3 --version
```

No es necesario instalar dependencias externas.

## Ejecución

```bash
python3 main.py
```

## Menú principal

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

Las opciones de inscripciones y calificaciones están
pendientes de integración.

## Pruebas automatizadas

El proyecto utiliza unittest, perteneciente a la biblioteca
estándar de Python.

Para ejecutar todas las pruebas:

```bash
python3 -m unittest discover -s tests -v
```

### Distribución de pruebas

| Módulo | Pruebas |
|--------|--------:|
| Persona | 6 |
| Profesores | 8 |
| Aprendices | 12 |
| Cursos | 20 |
| GestionAcademica | 10 |
| Menú interactivo | 8 |
| Total | 64 |

## Control de versiones

El proyecto utiliza Git y GitHub mediante una estrategia
de ramas de desarrollo.

### Ramas principales

- main
- develop

### Ramas de funcionalidades

- feature/gestion-profesores
- feature/gestion-aprendices
- feature/gestion-cursos
- feature/inscripciones
- feature/calificaciones
- feature/tests
- feature/gestion-academica
- feature/menu-consola
- feature/documentation

Los cambios se integran mediante Pull Requests y commits
descriptivos en inglés.

## Distribución de responsabilidades

### Integrante 1

- Clase abstracta Persona.
- Gestión de profesores.
- Gestión de aprendices.
- Gestión de cursos.
- GestionAcademica.
- Menú interactivo.
- Pruebas automatizadas.
- Documentación.

### Integrante 2

- Gestión de inscripciones.
- Gestión de calificaciones.
- Consultas académicas.
- Reportes de calificaciones.

## Almacenamiento de información

El sistema utiliza almacenamiento temporal en memoria mediante
estructuras de datos de Python.

Los registros permanecen disponibles durante la ejecución
del programa y se eliminan al finalizarlo.

No se utilizan bases de datos ni mecanismos de persistencia
permanente.

## Estado del proyecto

- [x] Gestión de profesores.
- [x] Gestión de aprendices.
- [x] Gestión de cursos.
- [x] Gestión académica centralizada.
- [x] Menú interactivo.
- [x] Pruebas unitarias y de integración.
- [ ] Integración de inscripciones.
- [ ] Integración de calificaciones.
- [ ] Reportes académicos completos.
- [ ] Revisión final de SOLID.

## Contexto académico

- Institución: SENA.
- Programa: Análisis y Desarrollo de Software (ADSO).
- Tipo de proyecto: Actividad académica colaborativa.