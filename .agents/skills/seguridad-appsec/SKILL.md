# Aplicacion local: seguridad-appsec

## Checklist rapido AppSec

- Confirmar que no hay secretos en codigo, docs ni ejemplos.
- Confirmar que los errores esperados no rompen historicos.
- Confirmar que las corridas grandes usan limites o checkpoints cuando corresponde.
- Confirmar que cualquier fuente externa se documenta.
- Confirmar que las heuristicas comerciales no se presentan como hechos verificados.

## Riesgos especificos del proyecto

- Bloqueos de filesystem en Windows durante escritura de checkpoints o CSV.
- Corridas concurrentes sobre el mismo checkpoint o salida.
- Uso excesivo de hilos contra NIC Chile.
- Enriquecimientos futuros que mezclen datos no verificados con datos observados.
