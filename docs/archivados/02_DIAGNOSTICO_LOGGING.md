# Diagnostico del logging

## Clasificacion actual

**Logging parcial y transitorio por consola.** Hay mensajes con prefijos `[ok]`, `[warn]`, `[error]` e `[info]`, progreso por `stderr` y checkpoint para reanudacion. No hay evidencia de un mecanismo persistente que registre el ciclo completo de cada ejecucion.

## Evidencia tecnica

| Hallazgo | Evidencia estatica | Consecuencia |
| --- | --- | --- |
| No hay logging estructurado | No se encontro `import logging` ni uso de la biblioteca en los modulos Python. | No hay niveles, formato comun, handlers ni correlacion persistente. |
| No hay archivo de log generado por el codigo | `logs/` solo contiene `.gitkeep`; `DIRECTORIO_LOGS` se declara en `app/configuracion.py` sin uso observado. | Al cerrar la consola se pierde el registro de una ejecucion. |
| Registrados/eliminados entregan diagnostico util en consola | `ejecutar_tarea` informa fallback, fuente, conteos, archivo y resultado. | Ayuda durante una ejecucion interactiva, pero no deja auditoria recuperable. |
| Caducidad entrega progreso y resumen | `principal` controla `--progreso`, escribe a `stderr` y resume estados al terminar. | El progreso es transitorio y no identifica una corrida persistente. |
| Checkpoint no equivale a log | El JSON conserva metadata, conteos y ultimo dominio; se elimina al finalizar correctamente. | Sirve para reanudar, no para explicar inicio, fin, errores y resultado de cada corrida. |
| Los errores por dominio no quedan necesariamente visibles | `consultar_dominio` convierte excepciones en estado `error`; por defecto, `descubrir` puede omitir estados no relevantes de la salida CSV. | Puede faltar evidencia posterior sobre errores individuales o su distribucion. |

## Fortalezas

- Solo usa biblioteca estandar; una eventual solucion puede conservar esa restriccion.
- Los flujos ya producen conteos y estados de cierre reutilizables como eventos de log.
- La separacion actual entre resultados CSV, checkpoint y salida de consola facilita incorporar un adaptador localizado.
- `.gitignore` ya protege `logs/` y `*.log` de publicacion accidental.

## Brechas y severidad

| ID | Brecha | Severidad | Evidencia | Riesgo practico |
| --- | --- | --- | --- | --- |
| LOG-01 | No existe registro persistente de inicio, fin y resultado de las consultas registrados/eliminados. | Medio | Solo `print` y CSV de resultado. | No se puede auditar una corrida una vez cerrada la consola. |
| LOG-02 | No existe identificador de ejecucion ni duracion. | Medio | Los resúmenes no incluyen ambos datos. | Cuesta correlacionar fallas, reintentos y archivos generados. |
| LOG-03 | La caducidad no conserva de forma separada los errores por dominio ni un resumen persistente. | Medio | Errores se transforman en estado; la salida puede filtrarlos. | Diagnostico posterior incompleto, especialmente ante fallas de NIC o red. |
| LOG-04 | `DIRECTORIO_LOGS` esta declarado sin integracion observable. | Bajo | Declaracion en configuracion; directorio sin archivos generados. | Configuracion muerta o expectativa operativa no satisfecha. |
| LOG-05 | No hay politica implementada de retencion o rotacion. | Bajo hoy; Medio si aumenta el uso | No hay handler ni archivos de log. | Si se agregan logs sin limite, pueden crecer indefinidamente. |

No se identifico una brecha critica: el analisis estatico no demuestra perdida de datos CSV ni interrupcion funcional de las consultas por la ausencia de logs.

## Recomendacion de diseno

Adoptar, si el desarrollador confirma la necesidad, logging persistente local con la biblioteca estandar `logging`, un punto de configuracion comun y eventos acotados por ejecucion. Registrar metadata operacional minima: inicio, identificador de corrida, programa, modo, periodo o parametros no sensibles, fuente, ruta de salida relativa, conteos, resultado, duracion y errores resumidos. No registrar tokens, credenciales, respuestas completas de NIC ni listas completas de dominios.

La rotacion debe ser una decision posterior y proporcional. Para el uso actual, un archivo por dia o `RotatingFileHandler` con limites explicitos bastaria; no se justifica observabilidad distribuida, una base de datos ni dependencias externas.

## Aspectos pendientes de validacion

- Prueba de humo con una consulta controlada y revision de que el log se escribe, no duplica handlers y no expone datos innecesarios.
- Prueba de fallo de NIC/red y de interrupcion para verificar que se registra un cierre anomalo.
- Prueba de permisos/bloqueos Windows sobre `logs/`, dado el antecedente documentado de bloqueos de checkpoint.
