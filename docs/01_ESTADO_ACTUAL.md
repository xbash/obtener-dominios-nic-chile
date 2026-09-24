# Estado actual: auditoria de logging

Fecha de auditoria: 2026-09-13.

## Alcance y trazabilidad

La auditoria fue estatica y en modo lectura. No se ejecutaron los comandos del proyecto, no se consulto NIC Chile, no se abrieron CSV operacionales y no se modifico codigo ni configuracion.

Archivos de contexto leidos: `AGENTS.md`, `README.md`, `docs/CONTEXTO_PROYECTO.md`, `docs/DECISIONES_TECNICAS.md`, `docs/PENDIENTES.md`, `docs/BITACORA_AGENTES.md`, `.gitignore` y los modulos Python implicados en los flujos de consulta, caducidad, progreso, checkpoint y salida.

Se observo un worktree con cambios preexistentes en dos CSV operacionales. No se inspeccionaron ni alteraron sus contenidos. `logs/` existe y contenia solamente `.gitkeep` al momento de la inspeccion.

## Objetivo funcional y arquitectura relevante

El proyecto Python consulta dominios `.cl` registrados o eliminados desde NIC Chile y mantiene historicos CSV. Un segundo flujo consulta candidatos para detectar expiracion cercana.

Flujo resumido:

```text
dominios-nic.py o python -m app.main dominios-nic
  -> app.main.ejecutar
  -> app.consulta_dominios.principal
  -> app.consulta_dominios_core.ejecutar_tarea
  -> NIC Chile (TXT/CSV; fallback HTML) -> archivo/*.csv -> consola

dominios-por-caducar.py o python -m app.main dominios-por-caducar
  -> app.main.ejecutar
  -> app.dominios_por_caducar.principal
  -> consultas concurrentes a NIC Chile -> archivo/*.csv
  -> checkpoint JSON transitorio + progreso/consola
```

## Componentes observados

| Componente | Responsabilidad relevante |
| --- | --- |
| `app/main.py` | Despacha ambos programas y escribe el error de uso en `stderr`. |
| `app/consulta_dominios.py` | Valida argumentos para registrados y eliminados. |
| `app/consulta_dominios_core.py` | Descarga, aplica fallback, deduplica, persiste CSV y emite resumen de consulta. |
| `app/dominios_por_caducar.py` | Orquesta lectura, consultas concurrentes, resultados, checkpoint y resumen de caducidad. |
| `app/progreso_dominios.py` | Emite progreso transitorio por `stderr`. |
| `app/checkpoint_dominios.py` | Mantiene estado de reanudacion en JSON; no es una bitacora. |
| `app/configuracion.py` | Declara `DIRECTORIO_LOGS`, pero no se observo consumo de esa constante. |
| `app/salida_dominios.py` | Escribe CSV de resultados de caducidad. |

## Mecanismo actual de registro

### Evidencia encontrada

- No se encontro `import logging`, uso de `logging.*`, handler, formatter, rotacion ni apertura de archivos `.log` en los modulos Python revisados.
- `app/consulta_dominios_core.py` emite advertencias y errores de fallback a `stderr`, y al finalizar imprime un resumen de modo, periodo, fuente, conteos y archivo de salida.
- `app/dominios_por_caducar.py` emite advertencias a `stderr`, un indicador de progreso transitorio y un resumen final con conteos y estados.
- `app/checkpoint_dominios.py` imprime advertencias relacionadas con lectura, guardado o borrado del checkpoint; el JSON conserva progreso para reanudar, no una secuencia de eventos de auditoria.
- `.gitignore` excluye `logs/` y `*.log`; esto es consistente con reservar esos artefactos para uso local, no con una implementacion activa.
- `docs/PENDIENTES.md` ya registra como tarea de baja prioridad evaluar logs persistentes si aumenta el uso operacional.

### Interpretacion

El sistema posee diagnostico parcial y transitorio por consola, no logging persistente ni estructurado. Los CSV son resultados/historicos y el checkpoint es estado de reanudacion: ninguno permite reconstruir con fiabilidad una ejecucion completa tras cerrar la consola.

## Incertidumbres y limites

- No se verifico en ejecucion si los mensajes de consola aparecen exactamente como indica el flujo estatico.
- No se inspeccionaron procesos externos, tareas programadas, redirecciones de shell ni artefactos operacionales fuera del codigo; no hay evidencia estatica de que los cree el proyecto.
- No se evaluaron permisos de escritura ni comportamiento de bloqueo de `logs/` en Windows.
