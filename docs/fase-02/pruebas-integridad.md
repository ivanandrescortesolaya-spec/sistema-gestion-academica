
# Pruebas de integridad de la base de datos

## 1. Objetivo

Verificar que la base de datos cumple las restricciones
estructurales y las operaciones académicas evaluadas
durante la fase de implementación.

## 2. Estrategia de pruebas

Se implementaron pruebas positivas y negativas.

Las pruebas positivas verifican operaciones válidas.

Las pruebas negativas comprueban que las restricciones
rechazan registros incorrectos o inconsistentes.

## 3. Ambiente de ejecución

- MySQL 8.4.
- Motor InnoDB.
- Contenedor academic-mysql.
- Base sistema_gestion_academica_test.
- Usuario academic_test_user.
- Scripts SQL y Bash.

## 4. Organización de archivos

```text
database/tests/
├── run_tests.sh
├── test_persona.sql
├── test_profesor.sql
├── test_aprendiz.sql
├── test_modalidad.sql
├── test_curso.sql
├── test_inscripcion.sql
├── test_calificacion.sql
├── test_rendimiento.sql
├── test_reportes.sql
├── test_permissions.sh
└── test_persistence.sh
```

## 5. Pruebas de persona

| Caso | Resultado |
|---|---|
| Registro válido | PASS |
| Documento duplicado | PASS |
| Documento vacío | PASS |
| Documento con letras | PASS |
| Documento igual a cero | PASS |
| Nombre vacío | PASS |
| Edad negativa | PASS |
| Documento nulo | PASS |

Total: 8 de 8.

## 6. Pruebas de profesor

| Caso | Resultado |
|---|---|
| Registro válido | PASS |
| Código duplicado | PASS |
| Clave primaria duplicada | PASS |
| Persona inexistente | PASS |
| Código igual a cero | PASS |
| Código negativo | PASS |
| Profesión vacía | PASS |
| Especialidad vacía | PASS |
| Profesión nula | PASS |
| Eliminación de persona relacionada | PASS |

Total: 10 de 10.

## 7. Pruebas de aprendiz

| Caso | Resultado |
|---|---|
| Registro válido | PASS |
| Aprendiz duplicado | PASS |
| Persona inexistente | PASS |
| Teléfono vacío | PASS |
| Correo vacío | PASS |
| Dirección vacía | PASS |
| Correo nulo | PASS |
| Eliminación restringida | PASS |

Total: 8 de 8.

## 8. Pruebas de modalidad

| Caso | Resultado |
|---|---|
| Modalidades iniciales | PASS |
| Registro válido | PASS |
| Modalidad duplicada | PASS |
| Nombre vacío | PASS |
| Nombre nulo | PASS |
| Descripción opcional | PASS |

Total: 6 de 6.

## 9. Pruebas de curso

| Caso | Resultado |
|---|---|
| Curso sin profesor | PASS |
| Asignación de profesor | PASS |
| Código duplicado | PASS |
| Duración igual a cero | PASS |
| Duración negativa | PASS |
| Modalidad inexistente | PASS |
| Profesor inexistente | PASS |
| Nombre vacío | PASS |
| Eliminación de modalidad restringida | PASS |
| Eliminación de profesor restringida | PASS |

Total: 10 de 10.

## 10. Pruebas de inscripción

| Caso | Resultado |
|---|---|
| Inscripción válida | PASS |
| Código duplicado | PASS |
| Inscripción duplicada | PASS |
| Aprendiz inexistente | PASS |
| Curso inexistente | PASS |
| Estado inválido | PASS |
| Cancelación permitida | PASS |
| Transición inválida impedida | PASS |
| Eliminación de curso restringida | PASS |
| Eliminación de aprendiz restringida | PASS |

Total: 10 de 10.

## 11. Pruebas de calificación

| Caso | Resultado |
|---|---|
| Nota válida | PASS |
| Nota mínima | PASS |
| Nota máxima | PASS |
| Nota negativa | PASS |
| Nota superior a cinco | PASS |
| Código duplicado | PASS |
| Inscripción inexistente | PASS |
| Modificación permitida | PASS |
| Registro no permitido impedido | PASS |
| Modificación no permitida impedida | PASS |
| Eliminación de inscripción restringida | PASS |

Total: 11 de 11.

## 12. Pruebas de rendimiento

| Caso | Resultado |
|---|---|
| Promedio aprobado 4.27 | PASS |
| Promedio reprobado 2.43 | PASS |
| Aprobación con 3.00 | PASS |
| Reprobación con 2.99 | PASS |
| Rendimiento pendiente | PASS |
| Ausencia de calificaciones | PASS |
| Redondeo de 2.995 a 3.00 | PASS |

Total: 7 de 7.

## 13. Pruebas de reportes

| Caso | Resultado |
|---|---|
| Conteo general | PASS |
| Conteo por estado | PASS |
| Promedio general | PASS |
| Promedio máximo | PASS |
| Promedio mínimo | PASS |
| Porcentaje de aprobación del 75 % | PASS |
| Reporte vacío sin división por cero | PASS |

Total: 7 de 7.

## 14. Resumen de integridad

| Módulo | Pruebas | Superadas |
|---|---:|---:|
| Persona | 8 | 8 |
| Profesor | 10 | 10 |
| Aprendiz | 8 | 8 |
| Modalidad | 6 | 6 |
| Curso | 10 | 10 |
| Inscripción | 10 | 10 |
| Calificación | 11 | 11 |
| Rendimiento | 7 | 7 |
| Reportes | 7 | 7 |
| Total | 77 | 77 |

## 15. Manejo de errores SQL

Las pruebas verifican errores asociados con:

| Código | Descripción |
|---|---|
| 1048 | Valor nulo no permitido |
| 1062 | Registro duplicado |
| 1264 | Valor fuera de rango |
| 1451 | Eliminación restringida por clave foránea |
| 1452 | Referencia inexistente |
| 3819 | Incumplimiento de restricción CHECK |

## 16. Manejo de transacciones

Se utilizan transacciones para controlar los datos
generados durante las pruebas.

Las operaciones de prueba sobre registros se revierten
mediante ROLLBACK cuando corresponde.

Los identificadores AUTO_INCREMENT pueden presentar
saltos después de una transacción revertida.

## 17. Automatización

El archivo run_tests.sh ejecuta los nueve archivos SQL,
cuenta los resultados PASS y verifica que coincidan
con la cantidad esperada.

El script devuelve un código de salida diferente de cero
cuando detecta errores o resultados inesperados.

## 18. Ejecución

```bash
./database/tests/run_tests.sh
```

Resultado obtenido:

```text
Archivos ejecutados: 9
Archivos superados:  9
Archivos fallidos:   0
Pruebas superadas:   77

RESULTADO: TODAS LAS PRUEBAS SUPERADAS
```

## 19. Alcance de las pruebas

Las pruebas verifican restricciones de tablas y operaciones
SQL específicas.

Las transiciones de estado y las modificaciones de notas
se prueban mediante consultas condicionadas. Esto no
significa que todas esas reglas estén impuestas mediante
restricciones globales del servidor.

Las pruebas de rendimiento y reportes verifican cálculos
con datos controlados, sin cubrir necesariamente todas
las consultas de reportes del aplicativo.

## 20. Conclusión

Las 77 pruebas SQL fueron superadas satisfactoriamente.

Los resultados respaldan la integridad de las estructuras
implementadas y permiten continuar con la integración
de la base de datos en Python.
