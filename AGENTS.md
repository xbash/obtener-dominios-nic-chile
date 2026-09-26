# AGENTS.md

## Propósito y alcance

Este repositorio contiene herramientas CLI en Python para consultar información
pública de dominios `.cl` en NIC Chile, mantener históricos CSV locales y
revisar candidatos con expiración cercana.

Estas instrucciones regulan cambios persistentes en el repositorio. El uso
detallado de los comandos corresponde a `README.md`; las decisiones ya tomadas,
a `docs/DECISIONS.md`; y la continuidad, bitácoras, auditorías y planes, a los
documentos específicos bajo `docs/`.

## Arquitectura y convenciones

- El código de aplicación reside en `app/`.
- `dominios-nic.py` y `dominios-por-caducar.py` son wrappers delgados; conservar
  la lógica de negocio en `app/`.
- Usar la biblioteca estándar de Python salvo que una dependencia externa esté
  explícitamente justificada, evaluada y aprobada.
- Mantener `VERSION_PROYECTO` en `app/configuracion.py` como fuente única de la
  versión consumida por los CLI.
- Preferir nombres, mensajes y documentación en español, salvo convenciones del
  lenguaje, APIs o bibliotecas.
- No cambiar modos, flags, rutas por defecto o contratos de salida sin una
  necesidad explícita, análisis de compatibilidad y actualización de la
  documentación correspondiente.

## Contratos de datos

- Los históricos de registrados conservan el encabezado
  `fecha_consulta,dominio,fecha_registro`.
- Los históricos de eliminados conservan el encabezado
  `fecha_consulta,dominio`.
- La salida de caducidad y su compatibilidad histórica se definen en
  `app/salida_dominios.py` y se documentan en `README.md`.
- Antes de migrar, reescribir o deduplicar históricos en `archivo/`, crear un
  respaldo recuperable y registrar conteos antes y después.
- Mantener compatibilidad de lectura con históricos existentes cuando sea
  razonable y esté dentro del alcance del cambio.

Las columnas de enriquecimiento comercial son heurísticas locales. No
presentarlas como métricas SEO, valoración de mercado, reputación, verificación
de marcas ni evaluación legal.

## Datos locales, seguridad y operaciones externas

- `archivo/`, `entrada/`, `logs/` y `descargas/` pueden contener datos
  operacionales locales. Consultar `.gitignore` antes de añadir archivos.
- No versionar ni publicar históricos reales, candidatos locales, respaldos,
  checkpoints, logs, descargas, cachés, secretos o credenciales.
- No registrar en logs listas completas de dominios, respuestas completas de
  NIC, tokens, credenciales ni datos sensibles.
- Las consultas a NIC Chile son una integración externa: preservar validación de
  entrada, timeout, reintentos y manejo de errores existentes salvo justificación
  técnica explícita.
- Para pruebas contra NIC, usar un alcance pequeño y controlado. No ejecutar
  corridas masivas ni modificaciones de datos operacionales sin autorización.

## Forma de trabajar

Antes de editar:

1. Leer `README.md`, este archivo y los módulos directamente afectados.
2. Consultar `docs/DECISIONS.md` si el cambio toca contratos, arquitectura,
   persistencia, checkpoints o publicación.
3. Revisar cambios preexistentes y limitarse al alcance solicitado.
4. Elegir el cambio mínimo que preserve compatibilidad y legibilidad.

Para operaciones destructivas o de alto impacto —eliminaciones, migraciones de
datos, cambios de dependencias, refactorizaciones amplias o cambios de
configuración crítica— analizar impacto y dependencias antes de actuar. Si hay
incertidumbre relevante, presentar la acción propuesta y esperar aprobación.

No hacer commits, push, publicaciones, despliegues, merges ni pull requests
salvo solicitud explícita.

## Documentación

- Actualizar `README.md` solo cuando cambien instalación, uso, opciones,
  entradas, salidas o comportamiento observable.
- Actualizar `CHANGELOG.md` cuando corresponda a un cambio de versión o a
  cambios funcionales que el proyecto decida registrar.
- Registrar decisiones arquitectónicas nuevas en `docs/DECISIONS.md`; no
  reescribir decisiones históricas para documentar una tarea menor.
- Mantener planes, pendientes, auditorías, resultados y continuidad fuera de
  este archivo, en los documentos apropiados de `docs/`.
- No convertir `AGENTS.md` en una bitácora, changelog, plan ni resumen del
  proyecto.

## Validación

Aplicar validación proporcional al riesgo y declarar siempre qué se ejecutó.

Validación mínima sin generar bytecode:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -c "import app.consulta_dominios_core; import app.entrada_dominios; import app.dominios_por_caducar; print('imports ok')"
python -m app.main dominios-nic --help
python -m app.main dominios-por-caducar --help
```

Para cambios que afecten sintaxis, ejecutar además una validación estática de
los módulos modificados. Para cambios de lógica, preferir pruebas locales sin
red. Una prueba de humo contra NIC solo confirma la integración en el alcance
ejecutado; no sustituye pruebas deterministas.

No afirmar resultados, compatibilidades, métricas ni validaciones no verificadas.

## Política de selección de modelos

Usar el modelo menos costoso que pueda resolver correctamente la tarea. Distinguir
volumen de trabajo de complejidad cognitiva: muchos archivos no implican por sí
solos que se requiera un modelo de mayor capacidad.

- **Luna, esfuerzo bajo:** inventarios, búsquedas, cambios repetitivos ya
  especificados, formateo, renombres, movimientos aprobados, boilerplate y
  ejecución de comandos conocidos.
- **Luna, esfuerzo medio:** cambios relacionados y delimitados, refactorizaciones
  pequeñas, localización de referencias, correcciones simples o ejecución de un
  plan previamente aprobado.
- **Tierra, esfuerzo medio:** análisis arquitectónico, diseño, causa raíz
  compleja, evaluación de alternativas, estimación de impacto, revisión con
  dependencias no triviales y definición de planes.

Para trabajo complejo:

1. Usar Tierra para análisis y un plan verificable.
2. Dividir la ejecución en operaciones pequeñas.
3. Delegar operaciones mecánicas aprobadas a Luna.
4. Volver a Tierra solo si surge una decisión no prevista, ambigüedad relevante
   o riesgo arquitectónico.

Cuando esos nombres de modelo no estén disponibles, elegir el nivel equivalente
por capacidad y costo siguiendo el mismo criterio.

## Cierre de una tarea

Informar de forma separada:

- cambios realizados;
- validaciones ejecutadas y resultado;
- validaciones no ejecutadas y motivo;
- riesgos, supuestos y trabajo pendiente.

No inventar datos, resultados de NIC, métricas comerciales, estado legal,
reputación, resultados de mercado ni evidencia no observada.
