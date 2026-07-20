# Skill local: ingenieria-software

## Fuente reutilizable

`skills/ingenieria-software` dentro de la libreria local de skills reutilizables
del mantenedor.

## Uso en este repositorio

Usar cuando la tarea involucre:

- cambios en scripts Python bajo `app/`;
- formatos CSV historicos;
- migraciones de archivos en `archivo/`;
- mantenibilidad y modularizacion;
- validaciones de comandos;
- documentacion tecnica y continuidad para agentes.

## Reglas locales

- Mantener wrappers de raiz delgados: `dominios-nic.py` y `dominios-por-caducar.py`.
- Mantener logica de negocio en `app/`.
- No agregar dependencias externas sin justificacion.
- Mantener CSV como contrato principal:
  - registrados: `fecha_consulta,dominio,fecha_registro`;
  - eliminados: `fecha_consulta,dominio`;
  - caducidad: CSV enriquecido.
- Crear respaldo antes de migrar historicos en `archivo/`.
- Validar conteos antes y despues de cambios masivos.
- Preferir pruebas sin red para parser, salida y checkpoint.
- Usar corridas de humo acotadas cuando se consulte NIC.

## Comandos de referencia

```powershell
python -m app.main dominios-nic --modo registrados --periodo 1m
python -m app.main dominios-nic --modo eliminados --periodo 1s
python -m app.main dominios-por-caducar --modo descubrir --entrada archivo\dominios-nic-registrados-mes.csv --limite 1000 --hilos 18 --progreso si
```

## Validacion minima

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -c "import app.consulta_dominios_core; import app.entrada_dominios; import app.dominios_por_caducar; print('imports ok')"
```
