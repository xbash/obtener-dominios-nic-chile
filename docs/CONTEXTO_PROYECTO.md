# Contexto del proyecto

Fecha de consolidacion: 2026-07-20

Ultima actualizacion de sesion: 2026-07-20, posterior a preparacion de publicacion en GitHub.

## Objetivo actual

`obtener-dominios-nic-chile` es un conjunto de scripts Python para recolectar y mantener historicos de dominios `.cl` recientemente registrados o eliminados desde NIC Chile, revisar candidatos proximos a caducar y preparar una base historica util para analisis posterior de venta, reventa, subasta o priorizacion comercial.

El proyecto debe distinguir datos observados desde NIC, supuestos historicos y heuristicas locales. No debe inventar valor comercial, metricas SEO, estado legal, marcas, reputacion ni resultados de mercado.

Estado actual de publicacion: el repositorio Git local fue inicializado en `main`, existe remoto `origin` y el ultimo estado observado esta sincronizado con `origin/main`. Los datos operacionales reales deben permanecer ignorados y fuera del repositorio publico.

## Flujos principales

- `dominios-nic.py`: consulta dominios registrados o eliminados.
- `dominios-por-caducar.py`: consulta candidatos dominio por dominio y detecta expiracion cercana.
- `python -m app.main <programa>`: despachador central alternativo.

## Formatos de salida vigentes

Registrados, para `1h`, `1d`, `1w`, `1m`:

```csv
fecha_consulta,dominio,fecha_registro
```

Eliminados, para `1d`, `1s`:

```csv
fecha_consulta,dominio
```

Caducidad:

```csv
fecha_consulta,fuente,fecha_registro,dominio,fecha_expiracion,dias_restantes,estado,longitud,contiene_guion,contiene_numero,solo_letras,keyword_principal,sector_probable,riesgo_reventa
```

## Archivos modificados o relevantes

Codigo:

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

Datos y documentacion:

- `archivo/.gitkeep`
- `entrada/.gitkeep`
- `entrada/candidatos.example.txt`
- `docs/*.md`
- `README.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `LICENSE`
- `.gitignore`
- `.agents/README.md`
- `.agents/skills/ingenieria-software/*`
- `.agents/skills/seguridad-appsec/*`

Archivos locales no versionables:

- `archivo/*.csv`
- `archivo/*.txt`
- `archivo/*.bak`
- `entrada/candidatos.txt`
- `logs/`
- `descargas/`
- `__pycache__/`
- `.agents/_copias-reutilizables-no-usar/`

## Agentes locales

`.agents` quedo como capa local de adaptacion, no como copia activa de skills reutilizables completas.

Estructura activa:

```text
.agents/
  README.md
  skills/
    ingenieria-software/
      README.md
      aplicacion-local.md
    seguridad-appsec/
      README.md
      aplicacion-local.md
```

Las copias identicas de skills globales fueron movidas a:

```text
.agents/_copias-reutilizables-no-usar/
```

Fuentes reutilizables externas:

- `skills/ingenieria-software` en la libreria local de skills reutilizables del mantenedor.
- `skills/seguridad-appsec` en la libreria local de skills reutilizables del mantenedor.

## Supuestos vigentes

- Version actual del proyecto: `v2.3`, centralizada en `app/configuracion.py` como `VERSION_PROYECTO`.
- NIC Chile puede cambiar respuestas, campos o formato.
- Para registrados, `fecha_registro` debe venir desde el CSV de NIC cuando este disponible.
- Para historicos antiguos de registrados, la antigua columna `fecha` se uso como `fecha_consulta` y como base inicial de `fecha_registro`, por decision del usuario.
- Para eliminados no se agrega `fecha_registro`; solo se usa `fecha_consulta`.
- Las columnas comerciales son heuristicas locales, no metricas de mercado.

## Problemas encontrados

- La carpeta `.git` existia pero estaba vacia/incompleta; se inicializo Git en `main`.
- `gh` no estaba instalado o no estaba en `PATH`, por lo que la publicacion se termino mediante flujo Git/remoto externo.
- Antes de publicar se detectaron historicos reales, backups y candidatos locales que no debian versionarse; se reforzo `.gitignore` y se agrego `entrada/candidatos.example.txt`.
- `SECURITY.md` tenia un placeholder de correo de seguridad; fue reemplazado por una instruccion sin correo ficticio.
- `LICENSE` no tenia el texto completo GPLv3; se reemplazo por el texto oficial GPLv3.
- Algunos scripts indicaban `Version: v1.0`; se unifico todo a `v2.3`.
- Windows/sandbox nego escritura en `archivo/`, `docs/` y `__pycache__` en varias validaciones.
- El checkpoint fallaba ante `PermissionError`; se agregaron reintentos y advertencia no fatal.
- Una corrida agrego duplicados al no reconocer CSV de 3 columnas; se corrigio el parser y se reparo el historico.
- Habia copias completas de skills reutilizables en `.agents`; se archivaron y se crearon adaptadores locales.

## Comandos utiles

```powershell
python -m app.main dominios-nic --modo registrados --periodo 1m
python -m app.main dominios-nic --modo eliminados --periodo 1s
python -m app.main dominios-por-caducar --modo descubrir --entrada archivo\dominios-nic-registrados-mes.csv --limite 1000 --hilos 18 --progreso si
python -m app.main dominios-nic --version
python -m app.main dominios-por-caducar --version
git status -sb --ignored
git push -u origin main
```

## Instrucciones candidatas para AGENTS.md

- Mantener los formatos CSV vigentes por modo y periodo.
- Antes de modificar `archivo/*.csv`, crear respaldo o validar conteos.
- No versionar historicos reales, respaldos, candidatos locales, logs, descargas ni `__pycache__`.
- Mantener `VERSION_PROYECTO` como fuente unica para version del proyecto.
- Distinguir datos observados desde NIC de heuristicas locales.
- No inferir valor comercial, marcas, SEO ni riesgo legal sin fuente externa verificable.
- Mantener `.agents` como adaptadores locales; no duplicar skills globales completas salvo copia congelada justificada.
