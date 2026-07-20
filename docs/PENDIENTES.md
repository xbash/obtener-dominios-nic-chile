# Pendientes

Fecha de consolidacion: 2026-07-20

## Alta prioridad

- Crear pruebas automatizadas sin red para parseo CSV, salida enriquecida, deduplicacion y checkpoint.
- Actualizar `AGENTS.md` para reflejar que las salidas principales ahora son CSV, no TSV/TXT.
- Revisar ejemplos antiguos en `AGENTS.md` que aun mencionan rutas o formatos anteriores.
- Antes de futuras migraciones masivas, registrar conteos previos y posteriores.
- Decidir si se eliminan las copias archivadas en `.agents/_copias-reutilizables-no-usar/`.

## Media prioridad

- Agregar post-procesamiento para enriquecer historicos con DNS, HTTP/HTTPS, titulo HTML, parking, redireccion y senales SEO/reputacion con fuente verificable.
- Evaluar `--checkpoint-cada N` para reducir bloqueos en Windows.
- Revisar si conviene separar `fecha_consulta` y `fecha_detectado` en futuros modelos.
- Revisar encoding/mojibake en documentos antiguos si se planea publicacion.
- Confirmar estado real de Git antes de publicar o versionar cambios.

## Baja prioridad

- Evaluar `pyproject.toml` solo si se decide convertir el proyecto en paquete instalable.
- Evaluar logs persistentes en `logs/` si el uso operacional crece.
- Evaluar un historico unificado con columna `tipo_evento`.

## Comandos utiles

```powershell
python -m app.main dominios-nic --modo registrados --periodo 1h
python -m app.main dominios-nic --modo registrados --periodo 1d
python -m app.main dominios-nic --modo registrados --periodo 1w
python -m app.main dominios-nic --modo registrados --periodo 1m
python -m app.main dominios-nic --modo eliminados --periodo 1d
python -m app.main dominios-nic --modo eliminados --periodo 1s
```

```powershell
python -m app.main dominios-por-caducar --modo descubrir --entrada archivo\dominios-nic-registrados-mes.csv --orden normal --limite 1000 --hilos 18 --progreso si --checkpoint archivo\checkpoint-registrados-mes.json
```

## Instrucciones candidatas para AGENTS.md

- Usar `PYTHONDONTWRITEBYTECODE=1` cuando `py_compile` falle por bloqueo de `__pycache__`.
- Validar cambios funcionales con imports y pruebas de humo acotadas.
- No ejecutar corridas grandes contra NIC sin justificar alcance y usar `--limite` cuando aplique.
- Mantener `.agents/skills` como adaptadores locales y referenciar las skills globales.
