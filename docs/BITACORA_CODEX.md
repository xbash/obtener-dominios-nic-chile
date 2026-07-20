# Bitacora Codex

Fecha de consolidacion: 2026-07-20

## Rol aplicado

Se trabajo como agente de codigo con criterio de ingenieria aplicada: cambios localizados, validacion con evidencia y separacion entre datos observados, supuestos y heuristicas.

## Trabajo realizado

1. Se cambio la salida de `dominios-por-caducar` a CSV.
2. Se agrego enriquecimiento local para priorizacion comercial.
3. Se convirtieron historicos de registrados y eliminados a CSV.
4. Se cambio `dominios-nic` para generar CSV por defecto.
5. Se ajusto `registrados` para guardar `fecha_consulta,dominio,fecha_registro`.
6. Se uso la fuente CSV de NIC para extraer `Fecha Inscripcion`.
7. Se ajusto `eliminados` a `fecha_consulta,dominio`.
8. Se aseguro que `dominios-por-caducar` pueda leer ambos formatos.
9. Se mejoro el checkpoint ante bloqueos de Windows.
10. Se reparo duplicacion accidental en `dominios-nic-registrados-mes.csv`.
11. Se reorganizo `.agents`: copias reutilizables archivadas y adaptadores locales activos.

## Hechos verificados

- NIC Chile expone ultimos dominios inscritos en formato CSV.
- La fuente CSV de inscritos incluye `Nombre Dominio` y `Fecha Inscripcion`.
- `dominios-por-caducar` usa `ThreadPoolExecutor` y `--hilos`.
- `dominios-nic` no usa hilos porque descarga listados por periodo.
- El parser actual lee correctamente CSV de registrados de 3 columnas y eliminados de 2 columnas.
- Las copias previas en `.agents` eran identicas a las skills globales de ingenieria de software y seguridad AppSec.

## Supuestos activos

- Para historicos antiguos de registrados, la antigua columna `fecha` representa una fecha real de consulta y se uso como base inicial de `fecha_registro`.
- Para eliminados, la fecha disponible representa `fecha_consulta`.
- `riesgo_reventa` es una heuristica local, no una evaluacion legal.
- `sector_probable` y `keyword_principal` son clasificaciones simples, no resultados de modelo ni benchmark.
- `.agents/_copias-reutilizables-no-usar/` se conserva temporalmente hasta confirmacion del usuario.

## Problemas encontrados

- Bloqueos de Windows/sandbox al escribir en `archivo/`, `docs/` y `__pycache__`.
- `py_compile` puede fallar por bloqueo de `__pycache__`.
- El parser inicial de existentes no reconocia CSV con 3 columnas y genero duplicados en una corrida.
- Evitar paralelizar acciones dependientes como leer y borrar archivos temporales.
- Duplicar skills globales completas dentro de `.agents` aumenta riesgo de divergencia.

## Proximos pasos

- Crear tests automatizados.
- Implementar post-procesamiento externo para DNS/HTTP/SEO/reputacion.
- Evaluar frecuencia configurable de checkpoint.
- Actualizar `AGENTS.md` con formatos CSV vigentes y regla de `.agents`.
- Revisar `CHANGELOG.md` si se quiere versionar formalmente estos cambios.
- Decidir si borrar `.agents/_copias-reutilizables-no-usar/`.

## Instrucciones que deberian persistir en AGENTS.md

- Mantener formatos CSV actuales por modo y periodo.
- Tratar `fecha_registro` de registrados como dato proveniente de NIC cuando este disponible.
- No mezclar enriquecimiento externo futuro con la consulta base sin documentar fuente, fecha y limitaciones.
- No presentar heuristicas comerciales como metricas verificadas.
- Crear respaldo antes de migrar historicos.
- Validar con conteos antes/despues en cambios masivos.
- Usar pruebas de humo acotadas con `--limite` para evitar consultas grandes innecesarias.
- Mantener `.agents/skills` como adaptadores locales; las skills completas deben vivir en `gen-ai-skills`.

## Memories durables propuestas

### Propuesta 1

- Memory propuesta: En `obtener-dominios-nic-chile`, los historicos principales son CSV: registrados usa `fecha_consulta,dominio,fecha_registro`; eliminados usa `fecha_consulta,dominio`; caducidad usa CSV enriquecido.
- Motivo: Es un contrato de datos central para futuras modificaciones.
- Alcance: Solo este repositorio.
- Riesgo si se guarda: Puede quedar obsoleto si se redisenan los formatos.
- Alternativa si debe ir mejor en AGENTS.md o docs/: Debe estar en `docs/DECISIONES_TECNICAS.md` y conviene agregarlo a `AGENTS.md`.

### Propuesta 2

- Memory propuesta: Para registrados, `fecha_registro` debe venir del CSV de NIC (`Fecha Inscripcion`) cuando este disponible; para historicos antiguos se uso la antigua columna `fecha` como base inicial por decision del usuario.
- Motivo: Evita confundir fecha de consulta con fecha real de registro en futuras sesiones.
- Alcance: Solo flujo `dominios-nic --modo registrados`.
- Riesgo si se guarda: Medio; depende de que NIC mantenga el CSV actual.
- Alternativa si debe ir mejor en AGENTS.md o docs/: Mejor en `docs/CONTEXTO_PROYECTO.md` y `docs/DECISIONES_TECNICAS.md`; memory pendiente de confirmacion del usuario.

### Propuesta 3

- Memory propuesta: `dominios-por-caducar` debe leer tanto CSV de registrados de 3 columnas como CSV de eliminados de 2 columnas; usa `--hilos` para consultas dominio por dominio.
- Motivo: Es un requisito operacional recurrente.
- Alcance: Solo este repositorio.
- Riesgo si se guarda: Bajo a medio si cambia el parser.
- Alternativa si debe ir mejor en AGENTS.md o docs/: Mejor en `AGENTS.md` si debe cumplirse siempre.

### Propuesta 4

- Memory propuesta: En Windows, se observaron bloqueos de escritura en `archivo/`, `docs/` y `__pycache__`; usar respaldos, `PYTHONDONTWRITEBYTECODE=1` y validaciones acotadas.
- Motivo: Ahorra diagnostico en futuras sesiones.
- Alcance: Este entorno/repositorio.
- Riesgo si se guarda: Puede ser temporal o propio del sandbox.
- Alternativa si debe ir mejor en AGENTS.md o docs/: Mejor en `docs/BITACORA_CODEX.md`; memory pendiente de confirmacion.

### Propuesta 5

- Memory propuesta: No inferir valor comercial, riesgo legal, SEO, reputacion ni marcas desde heuristicas locales; documentar fuente y limitaciones en cualquier enriquecimiento futuro.
- Motivo: Alinea el proyecto con uso de dominios para reventa/subasta sin inventar datos.
- Alcance: Este repositorio y tareas relacionadas con analisis de dominios.
- Riesgo si se guarda: Bajo.
- Alternativa si debe ir mejor en AGENTS.md o docs/: Debe ir en `AGENTS.md`; tambien documentado en `docs/CONTEXTO_PROYECTO.md`.

### Propuesta 6

- Memory propuesta: En este repositorio, `.agents/skills` debe contener adaptadores locales y no copias completas de skills globales; las fuentes reutilizables viven en `gen-ai-skills`.
- Motivo: Evita divergencia entre skills globales y adaptaciones locales.
- Alcance: Este repositorio y repos similares que usen `gen-ai-skills`.
- Riesgo si se guarda: Bajo; puede cambiar si se decide versionar skills congeladas dentro de cada repo.
- Alternativa si debe ir mejor en AGENTS.md o docs/: Debe ir en `AGENTS.md` como regla del repositorio; tambien esta en `docs/DECISIONES_TECNICAS.md`.
