# Aplicacion local: ingenieria-software

## Checklist rapido para cambios

- Revisar archivos relacionados antes de editar.
- Identificar si el cambio toca contrato CSV.
- Evitar refactors no solicitados.
- Mantener compatibilidad de lectura con historicos existentes cuando sea razonable.
- Documentar decisiones en `docs/DECISIONES_TECNICAS.md`.
- Documentar pendientes en `docs/PENDIENTES.md`.
- No afirmar validaciones que no fueron ejecutadas.

## Riesgos tecnicos frecuentes

- Duplicar dominios por parseo incorrecto de CSV.
- Perder trazabilidad al migrar historicos sin respaldo.
- Bloqueos de Windows en `archivo/`, `docs/` o `__pycache__`.
- Confundir `fecha_consulta` con `fecha_registro`.
