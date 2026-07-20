# Registro de cambios

Fecha de consolidacion: 2026-07-20

Este registro resume el trabajo reciente. Para versionado formal, revisar tambien `CHANGELOG.md` y el diff real del repositorio.

## Actualizacion final de sesion 2026-07-20

- Se ejecuto una revision prepublicacion del repositorio.
- Se reforzo `.gitignore` para excluir historicos reales, respaldos, candidatos locales, logs, descargas, caches y copias archivadas de skills.
- Se agrego `entrada/candidatos.example.txt` como ejemplo neutro y se dejo `entrada/candidatos.txt` fuera de versionamiento.
- Se reemplazo `LICENSE` por el texto completo GPLv3.
- Se elimino el placeholder de correo en `SECURITY.md`.
- Se eliminaron rutas locales absolutas de documentacion y adaptadores `.agents`.
- Se unifico la version del proyecto en `v2.3` y se centralizo en `VERSION_PROYECTO`.
- Se inicializo Git en `main`, se creo un commit inicial y posteriormente se observo el repositorio sincronizado con `origin/main`.
- Se constato que `gh` no estaba instalado o no estaba en `PATH`.

## Archivos de codigo modificados

- `dominios-nic.py`
- `dominios-por-caducar.py`
- `app/configuracion.py`
- `app/consulta_dominios.py`
- `app/consulta_dominios_core.py`
- `app/entrada_dominios.py`
- `app/dominios_por_caducar.py`
- `app/salida_dominios.py`
- `app/checkpoint_dominios.py`
- `app/enriquecimiento_dominios.py`

## Archivos de datos migrados o generados

- `archivo/dominios-nic-registrados-mes.csv` local, no versionable.
- `archivo/dominios-nic-eliminados-semana.csv` local, no versionable.
- `archivo/dominios-por-caducar.csv` local, no versionable.
- respaldos `.bak` y `dedup-bak` asociados a migraciones, no versionables.
- `entrada/candidatos.example.txt` versionable como ejemplo neutro.

## Archivos de agentes modificados

- `.agents/README.md`
- `.agents/skills/ingenieria-software/README.md`
- `.agents/skills/ingenieria-software/aplicacion-local.md`
- `.agents/skills/seguridad-appsec/README.md`
- `.agents/skills/seguridad-appsec/aplicacion-local.md`
- `.agents/_copias-reutilizables-no-usar/*`

## Cambios funcionales

- `dominios-nic` ahora genera CSV.
- Registrados usa encabezado `fecha_consulta,dominio,fecha_registro` para todos los periodos.
- Eliminados usa encabezado `fecha_consulta,dominio` para todos los periodos.
- `dominios-por-caducar` escribe CSV enriquecido.
- Se agregaron heuristicas locales para priorizacion comercial.
- Se agrego lectura compatible de CSV de 2 y 3 columnas.
- Se corrigio la deteccion de dominios existentes en CSV con encabezado.
- Se mejoro checkpoint para tolerar bloqueos de Windows.
- Se centralizo la version en `app/configuracion.py`.
- Los comandos `--version` reportan `v2.3`.

## Cambios en `.agents`

- Se detecto que `.agents/ingenieria-software` y `.agents/seguridad-appsec` eran copias identicas de skills globales.
- Se movieron a `.agents/_copias-reutilizables-no-usar/`.
- Se crearon adaptadores locales bajo `.agents/skills/`.

## Problemas corregidos

- `PermissionError` al reemplazar checkpoint en Windows.
- Bloqueos del sandbox al escribir en `archivo/` y `docs/`.
- Duplicacion accidental de registrados por parser que no reconocia CSV de 3 columnas.
- Documentacion previa indicaba formatos antiguos donde ahora corresponde CSV.
- Duplicacion de skills reutilizables completas dentro de `.agents`.
- `.git` estaba vacio/incompleto antes de inicializar el repositorio.
- `gh` no estaba disponible para crear/subir repositorios desde CLI.

## Validaciones ejecutadas

- Imports con `PYTHONDONTWRITEBYTECODE=1`.
- Pruebas de parseo de lineas CSV de registrados y eliminados.
- Corridas reales acotadas contra NIC con salidas temporales.
- Corrida real mensual de registrados contra NIC para validar `Fecha Inscripcion`.
- Lectura del historico principal desde el parser compartido.
- Comparacion de hashes para confirmar que las skills copiadas en `.agents` eran identicas a las globales.
- Busqueda acotada de secretos y placeholders antes de publicacion.
- `python -m app.main dominios-nic --version`.
- `python -m app.main dominios-por-caducar --version`.
- Parseo AST de 15 archivos Python.
- `git status -sb --ignored`.

## Validaciones no completas

- No se creo suite automatizada de tests.
- No se hizo escaneo externo especializado de secretos ni SAST.
- No se valido contenedor/WSL.
- No se instalo GitHub CLI.

## Instrucciones candidatas para AGENTS.md

- Documentar cambios de formato cuando cambien contratos CSV.
- No afirmar que el historico fue migrado sin conteos antes/despues.
- Mantener respaldos al modificar `archivo/*.csv`.
- No duplicar skills globales completas dentro de `.agents`; usar adaptadores locales.
