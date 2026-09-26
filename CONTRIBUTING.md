# Contributing

Gracias por colaborar. Este proyecto mantiene una convencion simple:

## Principios

- Mantener nombres en español para scripts, funciones, variables y archivos de salida.
- No romper el formato CSV de salida ya definido.
- Evitar refactors amplios cuando un cambio puntual resuelve el problema.
- Seguir el estilo y la estructura ya existente antes de introducir nuevas capas.

## Flujo de trabajo

1. Crear una rama de trabajo si el repositorio ya esta versionado.
2. Hacer cambios pequenos y trazables.
3. Ejecutar verificacion local minima:
   - `python -m app.main dominios-nic --help`
   - `python -m app.main dominios-por-caducar --help`
   - una corrida de humo con pocos dominios (usar `--limite` bajo y `--progreso si`)
4. Actualizar `README.md` y `CHANGELOG.md` si cambia el uso o el comportamiento.
5. No dejar archivos temporales ni checkpoints en el repositorio.

## Estilo

- Python 3.10+.
- UTF-8.
- Comentarios solo cuando aclaren una decision o una restriccion real.
- Las versiones del script deben quedar visibles en el encabezado del archivo.
- Si se usa un LLM o agente para editar el archivo, dejarlo indicado en el comentario del encabezado.

## Reglas de cambio

- Mantener la compatibilidad con los modos y flags existentes salvo que el cambio lo justifique.
- Si agregas una opcion nueva, documentarla en el README y en el changelog.
- Si cambias un nombre de archivo, actualizar referencias internas, README y ejemplos.
- Si agregas un flujo que consulte NIC, validar primero con un lote pequeno.

## Verificacion sugerida

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m app.main dominios-nic --help
python -m app.main dominios-por-caducar --help
```

Luego una corrida de humo con `--limite` bajo y `--progreso si`.

## Convenciones del proyecto

- Puntos de entrada:
  - `python -m app.main dominios-nic`
  - `python -m app.main dominios-por-caducar`
- Historicos CSV:
  - `dominios-nic-registrados-mes.csv`
  - `dominios-nic-eliminados-semana.csv`
  - `dominios-por-caducar.csv`
- Checkpoint:
  - `dominios-por-caducar.checkpoint.json`

## Antes de abrir un PR

- Revisar que no haya archivos temporales, cachés, logs ni checkpoints locales.
- Confirmar que el changelog refleje el cambio.
- Asegurar que README y documentación relevante reflejen el cambio en uso, comportamiento u opciones.
