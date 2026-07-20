# Changelog

Todos los cambios relevantes de este proyecto se documentan aqui.

## [Unreleased]

### Pendiente
- Crear pruebas automatizadas sin red para parseo CSV, salida enriquecida, checkpoint y deduplicacion.
- Ejecutar revision pre-publicacion antes de subir a GitHub.
- Decidir que historicos de `archivo/` deben publicarse, omitirse o reemplazarse por muestras.

## [v2.3] - 2026-07-20

### Agregado
- Salidas CSV para dominios registrados, eliminados y dominios por caducar.
- `fecha_registro` para dominios registrados usando la fuente CSV de NIC Chile cuando esta disponible.
- Enriquecimiento local en `dominios-por-caducar.csv`: longitud, guion, numeros, solo letras, keyword principal, sector probable y riesgo de reventa.
- Compatibilidad de lectura para CSV de registrados de 3 columnas y eliminados de 2 columnas.
- Skill local de proyecto bajo `.agents/skills/` para ingenieria de software y seguridad AppSec.

### Cambiado
- `dominios-nic.py` pasa a `v2.3`.
- `dominios-por-caducar.py` pasa a `v2.3`.
- Registrados usa encabezado `fecha_consulta,dominio,fecha_registro` para `1h`, `1d`, `1w`, `1m`.
- Eliminados usa encabezado `fecha_consulta,dominio` para `1d`, `1s`.
- `dominios-por-caducar.py` escribe CSV enriquecido en vez de TSV.
- README actualizado para reflejar comandos, formatos CSV y cautelas de publicacion.

### Corregido
- Parser de dominios existentes para CSV con encabezado.
- Duplicacion accidental en historico de registrados despues de migracion de formato.
- Checkpoint mas tolerante a bloqueos transitorios de Windows.

### Notas
- Las columnas comerciales son heuristicas locales; no son metricas de mercado, SEO, reputacion ni revision legal.
- Antes de publicar en GitHub se debe revisar secretos, respaldos, checkpoints e historicos reales.

## [v2.2] - 2026-07-19

### Agregado
- `dominios-por-caducar.py` con `--orden`, `--desde-fecha`, `--limite`, `--checkpoint`, `--progreso` y `--progreso-cada`.
- Procesamiento en flujo con concurrencia acotada para historicos grandes.
- Reanudacion por checkpoint en JSON.

### Cambiado
- El script de dominios por caducar paso a una version orientada a lotes y reanudacion.

### Notas
- Esta version esta pensada para recorrer historicos extensos sin cargar todo el trabajo de una sola vez.

## [v2.1] - 2026-07-19

### Agregado
- `--orden normal|inverso` para recorrer historicos de atras hacia adelante.

### Cambiado
- El flujo de lectura de entrada permitio priorizar lo mas reciente en historicos con fecha.

## [v2.0] - 2026-07-19

### Agregado
- Unificacion de modo `vigilar` y `descubrir` en un solo script.
- Salida tabular con estado de expiracion.

### Cambiado
- Se estandarizo el uso de nombres en espanol y el criterio de archivos historicos separados.

## [v1.0] - 2026-07-19

### Agregado
- Primera version funcional del flujo para revisar dominios por caducar.
- Consulta individual de la pagina de renovacion de NIC Chile para extraer fecha de expiracion.
