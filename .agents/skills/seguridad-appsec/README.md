# Skill local: seguridad-appsec

## Fuente reutilizable

`skills/seguridad-appsec` dentro de la libreria local de skills reutilizables
del mantenedor.

## Uso en este repositorio

Usar cuando la tarea involucre:

- consultas externas a NIC Chile;
- manejo de archivos historicos;
- checkpoints y reanudacion;
- procesamiento de entradas CSV/TXT;
- futuras integraciones DNS, HTTP, SEO o reputacion;
- riesgos de secretos, datos sensibles o abuso operacional.

## Reglas locales

- No guardar secretos, tokens ni credenciales en el repositorio.
- No imprimir datos sensibles en logs.
- No inventar reputacion, SEO, riesgo legal ni marcas.
- Documentar fuente, fecha y limitacion de cualquier enriquecimiento externo.
- Manejar fallas de red y timeouts sin corromper historicos.
- Crear respaldos antes de migraciones masivas.
- Validar entradas de archivos antes de escribir salidas.
- Mantener `--hilos` con criterio para no sobrecargar servicios externos.

## Focos de revision

- Path handling y escritura segura de archivos.
- Reintentos y fallas parciales.
- Duplicados e idempotencia.
- Exposicion accidental de rutas, datos o trazas.
- Integraciones futuras con APIs externas.
