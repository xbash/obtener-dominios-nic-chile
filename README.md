# obtener-dominios-nic-chile

Herramientas en Python para consultar dominios `.cl` recientemente registrados o eliminados en NIC Chile, mantener historicos CSV y revisar candidatos con expiracion cercana.

El proyecto esta orientado a analisis operativo de dominios para seguimiento, priorizacion comercial, reventa o subasta. Las columnas comerciales incluidas son heuristicas locales; no son metricas de mercado, SEO, reputacion ni revision legal o de marcas.

## Que incluye

- `dominios-nic.py`: consulta dominios registrados o eliminados.
- `dominios-por-caducar.py`: revisa dominios con expiracion cercana.
- `app/main.py`: despachador central para ambos comandos.
- `app/consulta_dominios_core.py`: consulta NIC y persistencia de historicos.
- `app/entrada_dominios.py`: lectura de entradas CSV/TXT.
- `app/salida_dominios.py`: escritura de resultados enriquecidos.
- `app/enriquecimiento_dominios.py`: heuristicas locales de priorizacion.
- `app/checkpoint_dominios.py`: checkpoint para corridas largas.

## Requisitos

- Python 3.10 o superior.
- Conexion a internet para consultar NIC Chile.
- No requiere dependencias externas de Python.

## Uso rapido

Desde la raiz del proyecto:

```powershell
cd obtener-dominios-nic-chile
```

### Dominios registrados

Periodos soportados: `1h`, `1d`, `1w`, `1m`.

```powershell
python dominios-nic.py --modo registrados --periodo 1d
python -m app.main dominios-nic --modo registrados --periodo 1m
```

Salida CSV:

```csv
fecha_consulta,dominio,fecha_registro
```

Para registrados, `fecha_registro` se obtiene desde el CSV de NIC Chile cuando esta disponible.

### Dominios eliminados

Periodos soportados: `1d`, `1s`.

```powershell
python dominios-nic.py --modo eliminados --periodo 1d
python -m app.main dominios-nic --modo eliminados --periodo 1s
```

Salida CSV:

```csv
fecha_consulta,dominio
```

### Dominios por caducar

```powershell
python dominios-por-caducar.py --modo descubrir --entrada archivo\dominios-nic-registrados-mes.csv --orden normal --limite 1000 --hilos 18 --progreso si --checkpoint archivo\checkpoint-registrados-mes.json
```

Tambien puede tomar dominios eliminados:

```powershell
python -m app.main dominios-por-caducar --modo descubrir --entrada archivo\dominios-nic-eliminados-semana.csv --orden inverso --limite 1000 --hilos 18 --progreso si
```

Salida CSV:

```csv
fecha_consulta,fuente,fecha_registro,dominio,fecha_expiracion,dias_restantes,estado,longitud,contiene_guion,contiene_numero,solo_letras,keyword_principal,sector_probable,riesgo_reventa
```

Estados posibles:

- `por_vencer`
- `vence_hoy`
- `caducado`
- `fuera_de_umbral`
- `sin_fecha`
- `no_renovable`
- `error`

Por defecto se escriben solo resultados relevantes para caducidad (`por_vencer`, `vence_hoy`, `caducado`). Usa `--incluir-todos` para diagnosticar tambien `sin_fecha`, `no_renovable`, `fuera_de_umbral` y `error`.

## Flujo recomendado

1. Actualizar registrados o eliminados:

```powershell
python -m app.main dominios-nic --modo registrados --periodo 1m
python -m app.main dominios-nic --modo eliminados --periodo 1s
```

2. Revisar caducidad por lotes:

```powershell
python -m app.main dominios-por-caducar --modo descubrir --entrada archivo\dominios-nic-registrados-mes.csv --orden normal --limite 10000 --hilos 18 --progreso si --checkpoint archivo\checkpoint-registrados-mes.json
```

3. Post-procesar el CSV resultante en planilla, Python, base de datos u otra herramienta.

## Archivos generados

- `archivo\dominios-nic-registrados-hora.csv`
- `archivo\dominios-nic-registrados-dia.csv`
- `archivo\dominios-nic-registrados-semana.csv`
- `archivo\dominios-nic-registrados-mes.csv`
- `archivo\dominios-nic-eliminados-dia.csv`
- `archivo\dominios-nic-eliminados-semana.csv`
- `archivo\dominios-por-caducar.csv`
- `archivo\dominios-por-caducar.checkpoint.json`

## Versiones actuales

- `dominios-nic.py`: `v2.3`
- `dominios-por-caducar.py`: `v2.3`

## Validacion local

Validacion minima sin escribir bytecode:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -c "import app.consulta_dominios_core; import app.entrada_dominios; import app.dominios_por_caducar; print('imports ok')"
```

Ayuda de comandos:

```powershell
python -m app.main dominios-nic --help
python -m app.main dominios-por-caducar --help
```

## Notas antes de publicar

- Revisar que no se incluyan secretos, tokens, logs, checkpoints, respaldos o historicos privados.
- Revisar `.gitignore` antes de subir a GitHub.
- Las salidas historicas en `archivo/` pueden contener datos operacionales; decide si deben publicarse completas, como muestra o no publicarse.
- No presentar las heuristicas comerciales como valores comprobados.

## Documentacion adicional

- `docs/CONTEXTO_PROYECTO.md`
- `docs/DECISIONES_TECNICAS.md`
- `docs/PENDIENTES.md`
- `docs/REGISTRO_CAMBIOS.md`
- `docs/BITACORA_CODEX.md`

## Colaboracion

Ver [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Seguridad

Ver [`SECURITY.md`](SECURITY.md).

## Licencia

Este proyecto se distribuye bajo GNU GPLv3. Ver [`LICENSE`](LICENSE).
