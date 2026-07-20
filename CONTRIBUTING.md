# Contributing

Gracias por colaborar. Este proyecto mantiene una convencion simple:

## Principios

- Mantener nombres en espanol para scripts, funciones, variables y archivos de salida.
- No romper el formato TSV de salida ya definido.
- Evitar refactors amplios cuando un cambio puntual resuelve el problema.
- Seguir el estilo y la estructura ya existente antes de introducir nuevas capas.

## Flujo de trabajo

1. Crear una rama de trabajo si el repositorio ya esta versionado.
2. Hacer cambios pequenos y trazables.
3. Ejecutar verificacion local minima:
   - `python -m py_compile dominios-nic.py`
   - `python -m py_compile dominios-por-caducar.py`
   - una corrida de humo con pocos dominios
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

- `python -m py_compile dominios-nic.py`
- `python -m py_compile dominios-por-caducar.py`
- `python dominios-por-caducar.py --help`
- corrida de humo con `--limite` bajo y `--progreso si`

## Convenciones del proyecto

- Scripts:
  - `dominios-nic.py`
  - `dominios-por-caducar.py`
- Historicos:
  - `dominios-nic-registrados-mes.txt`
  - `dominios-nic-eliminados-semana.txt`
  - `dominios-por-caducar.txt`
- Checkpoint:
  - `dominios-por-caducar.checkpoint.json`

## Antes de abrir un PR

- Revisar que no haya archivos temporales.
- Confirmar que el changelog refleje el cambio.
- Asegurar que el README siga explicando como ejecutar los scripts.
