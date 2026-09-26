# Obtener dominios de NiC Chile

Herramientas CLI en Python para consultar dominios `.cl` registrados o eliminados en NIC Chile, conservar históricos CSV locales y revisar candidatos próximos a caducar.

Las columnas comerciales son heurísticas locales. No representan métricas de mercado, SEO, reputación, marcas ni evaluación legal.

## Requisitos

- Python 3.10 o superior.
- Conexión a internet para consultar NIC Chile.
- No se requieren dependencias externas de Python.

## Uso básico

Ejecuta los comandos desde la raíz del repositorio.

### Dominios registrados

Períodos disponibles: `1h`, `1d`, `1w` y `1m`.

```powershell
python -m app.main dominios-nic --modo registrados --periodo 1d
```

La salida conserva el encabezado:

```csv
fecha_consulta,dominio,fecha_registro
```

### Dominios eliminados

Períodos disponibles: `1d` y `1s`.

```powershell
python -m app.main dominios-nic --modo eliminados --periodo 1s
```

La salida conserva el encabezado:

```csv
fecha_consulta,dominio
```

### Dominios por caducar

Usa un histórico CSV como entrada. Por ejemplo:

```powershell
python -m app.main dominios-por-caducar --modo descubrir --entrada archivo\dominios-nic-registrados-mes.csv --limite 1000 --progreso si
```

La salida es un CSV enriquecido con fechas, estado y heurísticas locales. Por defecto se escriben los estados relevantes para caducidad; `--incluir-todos` incluye también estados diagnósticos.

## Salidas y datos locales

Las rutas por defecto están bajo `archivo\`. Los históricos, checkpoints, logs, descargas y candidatos locales pueden contener datos operacionales y no deben publicarse sin revisión.

El CSV de caducidad incluye campos como `fecha_expiracion`, `dias_restantes`, `estado`, `longitud`, `keyword_principal`, `sector_probable` y `riesgo_reventa`. El encabezado completo se define en [app/salida_dominios.py](app/salida_dominios.py). Usa `--help` para ver opciones de filtrado y exclusión de campos.

## Ayuda y documentación

Consulta las opciones completas de cada CLI:

```powershell
python -m app.main dominios-nic --help
python -m app.main dominios-por-caducar --help
```

- [Decisiones técnicas](docs/DECISIONS.md)
- [Registro de cambios](CHANGELOG.md)
- [Guía de contribución](CONTRIBUTING.md) — nota: contiene referencias que pueden estar desactualizadas; los comandos actuales están en `--help`
- [Política de seguridad](SECURITY.md)
- [Licencia GPLv3](LICENSE)

## Validación local

Validación mínima sin escribir bytecode:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -c "import app.consulta_dominios_core; import app.entrada_dominios; import app.dominios_por_caducar; print('imports ok')"
python -m app.main dominios-nic --help
python -m app.main dominios-por-caducar --help
```
