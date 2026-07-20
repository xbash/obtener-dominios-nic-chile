# Decisiones tecnicas

Fecha de consolidacion: 2026-07-20

Ultima actualizacion de sesion: 2026-07-20.

## CSV como formato historico principal

Decision: usar CSV para historicos y salidas principales.

- Registrados: `fecha_consulta,dominio,fecha_registro`
- Eliminados: `fecha_consulta,dominio`
- Caducidad: CSV enriquecido con estado, fechas y heuristicas locales.

Motivo: facilita post-procesamiento, analisis y enriquecimiento posterior.

Trade-off: requiere mantener compatibilidad de lectura con encabezados antiguos.

## Registrados usa CSV de NIC como fuente primaria

Decision: para `--modo registrados`, usar `https://www.nic.cl/registry/Ultimos.do?f=csv&t={periodo}`.

Motivo: NIC expone `Fecha Inscripcion`, lo que permite poblar `fecha_registro` sin consultar dominio por dominio.

Trade-off: si la fuente CSV falla y se usa fallback HTML, `fecha_registro` puede quedar aproximada a `fecha_consulta`.

## Eliminados conserva formato simple

Decision: para eliminados, mantener solo `fecha_consulta,dominio`.

Motivo: la fuente de eliminados no entrega una fecha de registro equivalente; agregar columnas vacias aumentaria ruido.

## `dominios-por-caducar` debe leer ambos historicos

Decision: `app/entrada_dominios.py` soporta CSV de registrados de 3 columnas y CSV de eliminados de 2 columnas.

Motivo: permite reutilizar historicos de registrados y eliminados como entrada del flujo de caducidad.

## Enriquecimiento local en salida de caducidad

Decision: agregar heuristicas locales en `app/enriquecimiento_dominios.py`.

Columnas: `longitud`, `contiene_guion`, `contiene_numero`, `solo_letras`, `keyword_principal`, `sector_probable`, `riesgo_reventa`.

Limitacion: son heuristicas simples; no representan valor de mercado, riesgo legal validado, SEO ni reputacion.

## Checkpoint tolerante a bloqueo de Windows

Decision: reintentar escritura/reemplazo del checkpoint y no abortar toda la corrida si el checkpoint no puede guardarse.

Motivo: se observaron `PermissionError` y bloqueos transitorios en Windows.

Trade-off: si el checkpoint no se guarda, la corrida puede continuar pero la reanudacion no queda garantizada.

## Paralelismo

Decision: mantener `--hilos` solo en `dominios-por-caducar`.

Motivo: ese flujo consulta dominio por dominio contra NIC. `dominios-nic` descarga listados por periodo y no necesita hilos.

## Respaldo antes de migrar historicos

Decision: crear respaldos `.bak` o equivalentes antes de migrar CSV historicos.

Motivo: las migraciones cambian encabezados y pueden afectar miles de filas.

## `.agents` como adaptadores locales

Decision: `.agents/skills/*` contiene adaptadores locales para este repositorio, no copias completas de skills globales.

Motivo: evitar duplicacion y mantener las skills reutilizables en su fuente global.

Trade-off: futuras sesiones deben leer tanto el adaptador local como la fuente global si requieren el detalle completo.

## Version centralizada del proyecto

Decision: usar `VERSION_PROYECTO = "v2.3"` en `app/configuracion.py` como fuente unica para los CLI y logs.

Motivo: varios modulos auxiliares mantenian `Version: v1.0` mientras los scripts principales estaban en `v2.3`.

Trade-off: los docstrings siguen siendo texto estatico y requieren cuidado al cambiar de version, pero los puntos de ejecucion consumen la constante comun.

## Preparacion para publicacion en GitHub

Decision: versionar codigo, documentacion, archivos de control, `.gitkeep` y ejemplos neutros; no versionar datos operacionales reales.

Archivos excluidos por regla:

- `archivo/*.csv`
- `archivo/*.txt`
- `archivo/*.bak`
- `entrada/candidatos.txt`
- `logs/`
- `descargas/`
- `__pycache__/`
- `.agents/_copias-reutilizables-no-usar/`

Motivo: esos archivos contienen historicos reales, respaldos o estado local de ejecucion que no debe publicarse por defecto.

## Licencia y seguridad para publicacion

Decision: dejar `LICENSE` con el texto completo GPLv3 y eliminar placeholders de contacto en `SECURITY.md`.

Motivo: GitHub y lectores externos deben encontrar terminos de licencia completos y una politica de reporte sin correos ficticios.

## Pendiente tecnico

- Crear tests automatizados para parser CSV, deduplicacion, salida enriquecida y checkpoint.
- Evaluar `--checkpoint-cada N` para reducir escrituras de checkpoint.
- Evaluar una herramienta de post-procesamiento para DNS/HTTP/SEO/reputacion.
- Decidir si borrar o conservar `_copias-reutilizables-no-usar/`.
- Definir un flujo estable de publicacion: GitHub CLI en `PATH` o comandos Git remotos manuales.
