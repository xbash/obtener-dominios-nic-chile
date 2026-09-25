# Auditoría de limpieza del proyecto

Fecha de revisión: 2026-09-25  
Alcance: inspección estática y de solo lectura del repositorio local  
Proyecto: `obtener-dominios-nic-chile`

## 1. Criterio y límites

El objetivo de esta revisión es identificar archivos y directorios residuales de iteraciones de desarrollo, especialmente análisis, planes, borradores, reportes, temporales y documentación obsoleta generados durante el trabajo asistido por IA.

Se revisaron el inventario recursivo del proyecto, el estado Git, `.gitignore`, `README.md`, `AGENTS.md`, `docs/CONTEXTO_PROYECTO.md`, la documentación de continuidad, `.agents/`, las referencias estáticas en código y los artefactos locales visibles. No se ejecutaron consultas contra NIC Chile ni se modificaron, movieron o eliminaron archivos operacionales.

La clasificación es conservadora:

- `MANTENER`: tiene uso actual o valor técnico/operacional claro.
- `REVISAR`: tiene valor posible, pero está obsoleto, duplicado, ambiguo o requiere una decisión humana.
- `ELIMINAR`: no tiene uso actual ni valor histórico/técnico suficiente, y es un residuo generado o un directorio vacío sin contrato operativo demostrado. La eliminación queda solo propuesta; no se ejecutó.

## 2. Estado observado antes de esta auditoría

- `git status --short` mostraba cambios preexistentes en `archivo/dominios-nic-eliminados-semana.csv` y `archivo/dominios-nic-registrados-mes.csv`.
- Esos CSV no fueron inspeccionados en contenido ni modificados.
- `logs/consulta_dominios.log` existe y contiene ejecuciones recientes. Por tanto, el logging persistente sí está activo actualmente.
- Existen bytecode `.pyc` en `__pycache__/` y `app/__pycache__/`; ambos directorios están excluidos por `.gitignore`.
- `.codex/` existe, pero está vacío.
- No existe actualmente `.agents/_copias-reutilizables-no-usar/`, aunque varios documentos todavía la mencionan.
- La documentación `docs/01_ESTADO_ACTUAL.md` y `docs/02_DIAGNOSTICO_LOGGING.md` afirma que no existe logging persistente; esa afirmación contradice el código actual (`app/logging_dominios.py`) y el log observado.

## 3. Matriz de candidatos y controles relevantes

| Ruta | Tipo | Uso actual | Evidencia | Propósito original | Clasificación | Riesgo | Acción propuesta |
|---|---|---|---|---|---|---|---|
| `.codex/` | Directorio vacío | No observado | Inventario recursivo: 0 archivos; no hay referencias estáticas | Posible espacio de configuración o estado local de una herramienta | `ELIMINAR` | Bajo; una herramienta externa podría esperar el directorio, aunque no hay evidencia | Eliminar solo después de confirmar que ningún flujo local lo crea o espera; no requiere preservar contenido porque está vacío |
| `__pycache__/` | Bytecode generado | No participa en el código fuente | Contiene cuatro `.pyc`; `.gitignore` excluye `__pycache__/` | Cache local creado por Python durante iteraciones o ejecuciones | `ELIMINAR` | Bajo; Python lo puede regenerar | Eliminar la carpeta completa en una acción de limpieza posterior |
| `app/__pycache__/` | Bytecode generado | No participa en el código fuente | Contiene bytecode de módulos en Python 3.12, 3.13 y 3.14; está ignorado por Git | Cache local de importaciones y pruebas | `ELIMINAR` | Bajo; Python lo puede regenerar | Eliminar la carpeta completa; conservar los `.py` de `app/` |
| `logs/consulta_dominios.log` | Log operacional local | Sí | `app/configuracion.py` define `ARCHIVO_LOG`; `app/logging_dominios.py` crea un `RotatingFileHandler`; el archivo tiene eventos recientes | Registro persistente de ejecuciones de consultas | `MANTENER` | Medio: contiene rutas locales, conteos y actividad operacional; puede crecer hasta los límites configurados | Mantener fuera de Git; aplicar la política de rotación ya configurada y no tratarlo como documentación histórica canónica |
| `logs/` | Directorio operacional | Sí | Es el destino de `DIRECTORIO_LOGS` y está excluido por `.gitignore` | Destino local de logs y marcador `.gitkeep` | `MANTENER` | Bajo-Medio; borrar el directorio rompe o retrasa la creación del log hasta que el código lo regenere | Mantener; revisar retención solo si cambia el uso operacional |
| `archivo/dominios-nic-eliminados-semana.csv` | Histórico CSV operacional | Sí | Es salida del flujo `dominios-nic`; también es entrada documentada para caducidad; tiene cambio preexistente en Git | Histórico local de dominios eliminados | `MANTENER` | Alto si se elimina o sobrescribe: pérdida de datos operacionales y cambios del usuario | No tocar durante la limpieza; respaldar y validar conteos antes de cualquier migración |
| `archivo/dominios-nic-registrados-mes.csv` | Histórico CSV operacional | Sí | Es salida del flujo `dominios-nic`; también es entrada documentada para caducidad; tiene cambio preexistente en Git | Histórico local de dominios registrados | `MANTENER` | Alto si se elimina o sobrescribe: pérdida de datos operacionales y cambios del usuario | No tocar durante la limpieza; respaldar y validar conteos antes de cualquier migración |
| `archivo/dominios-por-caducar.csv` | Resultado CSV operacional | Sí | Está definido como salida por `app/configuracion.py` y documentado en `README.md` | Resultado enriquecido del análisis de caducidad | `MANTENER` | Alto si se elimina: pérdida del resultado local; las columnas comerciales son heurísticas y no deben tratarse como fuente externa verificada | Mantener fuera de Git; conservar el contrato CSV y separar resultados nuevos de respaldos |
| `entrada/candidatos.txt` | Entrada local de datos | Potencialmente sí | `app/configuracion.py` define la ruta y `app/entrada_dominios.py` la usa si está disponible; el archivo existe y está ignorado | Lista local para el modo de vigilancia o corridas operacionales | `MANTENER` | Medio-Alto: puede contener datos operacionales o candidatos privados | Mantener local; no versionar ni incluir contenido en reportes públicos; revisar manualmente su vigencia cuando cambie el flujo |
| `entrada/candidatos.example.txt` | Ejemplo de entrada | Sí como documentación/ejemplo | README y la documentación de continuidad lo presentan como ejemplo neutro; no contiene datos operacionales observados | Sustituir de forma segura el ejemplo de candidatos reales | `MANTENER` | Bajo; podría confundirse con una entrada ejecutable si se copia sin revisar | Mantener; conservar la distinción entre `.example.txt` y `candidatos.txt` |
| `descargas/` | Directorio local vacío con marcador | No observado en el flujo actual | `DIRECTORIO_DESCARGAS` está definido, pero no se encontraron consumidores en el código revisado; contiene solo `.gitkeep` | Reservar un espacio para descargas locales futuras | `REVISAR` | Bajo; eliminarlo puede afectar convenciones de estructura, pero no hay uso actual demostrado | Decidir si sigue siendo parte del contrato de estructura base; si no, retirar el marcador y actualizar la documentación |
| `.agents/README.md` | Adaptador/documentación local | Sí, como guía de agentes | Define como activas las skills de ingeniería y seguridad, pero menciona un directorio archivado que ya no existe | Explicar la capa local de adaptadores y las copias archivadas | `REVISAR` | Medio; la referencia inexistente puede inducir a buscar o conservar residuos ausentes | Actualizar en una futura intervención autorizada para indicar que la carpeta archivada ya no está presente |
| `.agents/skills/ingenieria-software/` | Adaptador local de skill | Sí | Está declarado como parte de la estructura activa en `.agents/README.md`; contiene reglas específicas del proyecto | Aplicar reglas locales para cambios Python, CSV y documentación | `MANTENER` | Bajo; eliminarlo quitaría contexto operativo local | Mantener; no reemplazarlo por una copia completa de la skill global |
| `.agents/skills/seguridad-appsec/` | Adaptador local de skill | Sí | Está declarado como parte de la estructura activa en `.agents/README.md`; contiene reglas específicas de seguridad | Aplicar controles locales sobre datos, red, checkpoints y secretos | `MANTENER` | Bajo; eliminarlo reduce la cobertura de seguridad contextual | Mantener |
| `.agents/skills/inicializar-proyecto-codex/SKILL.md` | Skill local de inicialización | No se observó uso actual | No figura entre las dos skills activas declaradas en `.agents/README.md`; las referencias encontradas son históricas o documentales | Asistir la creación inicial de la estructura Codex | `ELIMINAR` | Bajo-Medio; podría ser útil si se pretende repetir la inicialización desde este repositorio, aunque la skill existe fuera del proyecto | Confirmar que no exista un flujo local que la cargue; si no existe, eliminarla como residuo de bootstrap o conservarla fuera del repositorio |
| `docs/01_ESTADO_ACTUAL.md` | Reporte de auditoría puntual | No como instrucción o flujo | No hay referencias de código; describe una auditoría de logging del 2026-09-13 y afirma que `logs/` solo tenía `.gitkeep` | Estado previo a la implementación del logging persistente | `REVISAR` | Medio; puede inducir a diagnósticos incorrectos si se lee como estado vigente | Marcarlo explícitamente como histórico o retirar el reporte después de conservar sus decisiones relevantes |
| `docs/02_DIAGNOSTICO_LOGGING.md` | Diagnóstico puntual | No como instrucción o flujo | No hay referencias de código; afirma que no hay `import logging` ni archivo de log, contradicho por el código y `logs/consulta_dominios.log` actuales | Diagnosticar la brecha de logging antes de implementarla | `REVISAR` | Medio-Alto; es técnicamente obsoleto y puede provocar decisiones equivocadas | Archivar fuera de la documentación activa o eliminarlo tras verificar que sus decisiones estén cubiertas por `docs/04_DECISIONES_PENDIENTES.md` y la bitácora |
| `docs/03_PLAN_EJECUCION.md` | Plan de implementación | No como flujo ejecutable | El documento se declara “no ejecutado”, pero `docs/04_DECISIONES_PENDIENTES.md`, `app/logging_dominios.py` y el log muestran que parte del plan sí fue implementada | Plan por etapas para agregar logging persistente | `REVISAR` | Medio; conserva trazabilidad, pero su estado puede confundirse con trabajo pendiente | Convertirlo en registro histórico de plan ejecutado parcialmente o retirarlo después de conservar los criterios de aceptación útiles |
| `docs/04_DECISIONES_PENDIENTES.md` | Contrato/decisiones de logging | Sí | `app/configuracion.py` y `app/logging_dominios.py` lo citan; registra decisiones confirmadas e implementación | Documentar el contrato de logging y sus decisiones | `REVISAR` | Medio; el nombre “pendientes” ya no refleja que varias decisiones están confirmadas; además contiene una tensión entre D-09 resumida y la fila detallada | Mantener por ahora; en una futura edición autorizada separar decisiones confirmadas de pendientes y renombrar solo si se preservan las referencias del código |
| `docs/BITACORA_AGENTES.md` | Bitácora canónica de agentes | Sí | `AGENTS.md` exige registrar intervenciones relevantes aquí; `README.md` la identifica como historial completo | Trazabilidad de intervenciones LLM/Codex/ChatGPT | `MANTENER` | Bajo; eliminarla rompe la trazabilidad exigida por el proyecto | Mantener y agregar futuras entradas solo cuando corresponda |
| `docs/BITACORA_CODEX.md` | Bitácora detallada de una etapa | Referenciada por README, pero no por código | README la enlaza; contiene un cierre detallado, propuestas de memoria y decisiones ya consolidadas también presentes en otros documentos | Registrar el trabajo de Codex durante la creación y consolidación del proyecto | `REVISAR` | Medio; posible duplicación con `BITACORA_AGENTES.md`, y contiene referencias a la carpeta archivada ausente | Decidir si se conserva como historial detallado; si se elimina, trasladar primero cualquier hecho no cubierto por la bitácora canónica |
| `docs/CONTEXTO_PROYECTO.md` | Contexto persistente | Sí | Es lectura obligatoria según `AGENTS.md`; resume arquitectura, contratos, datos operacionales y reglas de continuidad | Mantener contexto para futuras sesiones | `REVISAR` | Medio; conserva valor, pero menciona el estado de julio y la carpeta archivada ausente, y no refleja completamente el logging actual | Mantener; actualizar sus hechos temporales y referencias obsoletas en una intervención documental separada |
| `docs/DECISIONES_TECNICAS.md` | Decisiones técnicas | Sí | Es parte de la documentación canónica y contiene contratos CSV, checkpoint, agentes y reglas de datos | Registrar decisiones de diseño y trade-offs | `MANTENER` | Bajo; eliminarla perdería contexto técnico y restricciones | Mantener; corregir solo referencias obsoletas cuando se autorice una limpieza documental |
| `docs/PENDIENTES.md` | Backlog y pendientes | Sí | Es leído por agentes y contiene tareas todavía abiertas, aunque incluye la decisión pendiente sobre una carpeta que ya no existe | Registrar trabajo futuro y riesgos abiertos | `MANTENER` | Medio; algunos pendientes están desactualizados y pueden duplicar decisiones cerradas | Mantener como backlog; retirar o actualizar únicamente los ítems ya resueltos |
| `docs/REGISTRO_CAMBIOS.md` | Registro de cambios | Sí | Forma parte de la documentación de continuidad y registra modificaciones del proyecto | Mantener trazabilidad resumida de cambios | `MANTENER` | Bajo; perderlo reduce la reconstrucción histórica | Mantener |
| `.vscode/settings.json` | Configuración de editor | Sí como configuración local/proyecto | Está versionado y pertenece a la estructura base documentada; no es un artefacto temporal | Ajustar el entorno de edición | `MANTENER` | Bajo; retirarlo puede cambiar la experiencia del proyecto en VS Code | Mantener; revisar solo si contiene preferencias ya inválidas |
| `tools/` | Directorio reservado, actualmente vacío | No hay scripts auxiliares activos | Contiene únicamente `.gitkeep`; la estructura base del proyecto lo contempla | Reservar scripts auxiliares futuros | `MANTENER` | Bajo; quitarlo rompe la estructura esperada, aunque no la ejecución actual | Mantener mientras la estructura de plantilla siga siendo contrato del proyecto |

## 4. Principales residuos detectados

1. **Caches generados:** `__pycache__/` y `app/__pycache__/` contienen bytecode de varias versiones de Python. Son residuos regenerables y no deben conservarse como parte del proyecto.
2. **Bootstrap local fuera de la estructura activa:** `.agents/skills/inicializar-proyecto-codex/SKILL.md` parece provenir de la inicialización del proyecto y no participa en los dos adaptadores locales declarados como activos.
3. **Documentación de logging obsoleta:** `docs/01_ESTADO_ACTUAL.md`, `docs/02_DIAGNOSTICO_LOGGING.md` y `docs/03_PLAN_EJECUCION.md` describen el estado anterior a la implementación de `logging`. Mantienen valor histórico, pero no deberían presentarse como estado actual.
4. **Duplicación de trazabilidad:** `docs/BITACORA_CODEX.md` y `docs/BITACORA_AGENTES.md` se solapan parcialmente. La segunda es la bitácora canónica exigida por `AGENTS.md`; la primera requiere decisión humana antes de retirar o consolidar.
5. **Referencias a contenido ausente:** `.agents/README.md`, `docs/CONTEXTO_PROYECTO.md`, `docs/PENDIENTES.md`, `docs/DECISIONES_TECNICAS.md` y `docs/BITACORA_CODEX.md` mencionan `.agents/_copias-reutilizables-no-usar/`, pero ese directorio no existe en el inventario actual. El residuo aquí es documental, no una carpeta presente.
6. **Directorio reservado sin consumidor actual:** `descargas/` existe como parte de la estructura, pero `DIRECTORIO_DESCARGAS` no tiene consumidores observados. No es un residuo inequívoco porque forma parte del esqueleto del proyecto.

## 5. Resumen cuantitativo

El conteo considera las 26 filas de la matriz, incluyendo controles de archivos y directorios que no son residuos para evitar confundirlos con candidatos de eliminación.

| Categoría | Cantidad | Interpretación |
|---|---:|---|
| `MANTENER` | 13 | Código, adaptadores activos, contratos, bitácoras canónicas, datos operacionales, logs y estructura con uso o valor demostrado |
| `REVISAR` | 10 | Documentación histórica/obsoleta, duplicaciones, directorios reservados o archivos cuyo retiro requiere confirmar contexto |
| `ELIMINAR` | 3 | `.codex/`, caches `__pycache__/` y la skill local de inicialización no activa, siempre con la confirmación indicada en la matriz |
| **Total** | **26** | Candidatos y controles evaluados |

## 6. Casos ambiguos que requieren decisión humana

- Si `.codex/` debe existir por una herramienta local externa no visible en el repositorio.
- Si `descargas/` seguirá siendo parte de la estructura base aunque no tenga consumidor actual.
- Si `.agents/skills/inicializar-proyecto-codex/SKILL.md` se desea conservar como copia congelada para futuras inicializaciones.
- Si los reportes `docs/01` a `docs/03` deben conservarse como historial de la implementación de logging o retirarse después de consolidar sus hechos.
- Si `docs/BITACORA_CODEX.md` debe permanecer como bitácora detallada o quedar absorbida por `docs/BITACORA_AGENTES.md`.
- Si se autoriza una actualización documental para eliminar las referencias a `.agents/_copias-reutilizables-no-usar/`, que actualmente apuntan a una ruta inexistente.
- Si el log local debe conservarse por su valor operacional actual, y cuál debe ser su retención más allá de la rotación técnica configurada.

## 7. Plan de acción propuesto, sin ejecutar

### Fase 1: limpieza segura de residuos inequívocos

Con autorización explícita, eliminar únicamente `.codex/`, `__pycache__/` y `app/__pycache__/`. Antes de eliminar la skill de inicialización, confirmar que no exista un flujo externo que la cargue.

### Fase 2: decisión documental

Decidir el tratamiento de `docs/01_ESTADO_ACTUAL.md`, `docs/02_DIAGNOSTICO_LOGGING.md`, `docs/03_PLAN_EJECUCION.md` y `docs/BITACORA_CODEX.md`. La opción de menor pérdida histórica es conservarlos como documentos históricos claramente etiquetados; la opción de menor acumulación es retirar los reportes redundantes después de consolidar los hechos en la documentación canónica.

### Fase 3: corrección de referencias obsoletas

En una intervención separada, actualizar referencias a `.agents/_copias-reutilizables-no-usar/`, revisar el nombre y estado de `docs/04_DECISIONES_PENDIENTES.md`, y actualizar el contexto de proyecto para reflejar el logging persistente actual. Esta fase no debe mezclarse con la eliminación física de datos operacionales.

### Fase 4: validación posterior

Después de cualquier cambio autorizado:

1. revisar `git status --short --ignored`;
2. verificar que no se hayan tocado los CSV operacionales preexistentes;
3. buscar referencias rotas a las rutas eliminadas;
4. ejecutar la validación AST/imports indicada por `AGENTS.md` sin generar bytecode, usando `PYTHONDONTWRITEBYTECODE=1`;
5. comprobar que el flujo de logging siga creando `logs/consulta_dominios.log` sin duplicar handlers;
6. revisar el diff y confirmar que la limpieza no cambió contratos CSV ni configuración operacional.

## 8. Conclusión

Hay residuos inequívocos y regenerables, pero la mayor parte del material sospechoso es documentación histórica o dato operacional, no basura segura de eliminar. La recomendación es retirar solo los caches y el directorio vacío después de la confirmación mínima, y resolver por separado las decisiones humanas sobre documentación histórica, la skill de inicialización y las referencias a carpetas archivadas ausentes.

Esta auditoría no ejecuta el plan de acción.
