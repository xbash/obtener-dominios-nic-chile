# Contexto vigente del proyecto

Última comprobación local: 2026-10-12 (America/Santiago).

## Propósito y contratos principales

Herramientas CLI en Python para consultar dominios `.cl` en NIC Chile, mantener históricos CSV locales y revisar candidatos próximos a caducar. El punto de entrada central es `python -m app.main <programa>`; los scripts de la raíz son wrappers de compatibilidad. `README.md` describe el uso y `AGENTS.md` fija las reglas persistentes.

- Versión de los CLI: `VERSION_PROYECTO = "v2.3"` en `app/configuracion.py`.
- Histórico de registrados: `fecha_consulta,dominio,fecha_registro`.
- Histórico de eliminados: `fecha_consulta,dominio`.
- Salida de caducidad: `app/salida_dominios.py` es la referencia de campos.
- Los campos comerciales son heurísticas locales, no métricas verificadas de mercado, SEO, reputación ni estado legal.

## Estado comprobado

La auditoría documental solicitada el 2026-10-11 concluyó **CON BRECHAS**. Fue una inspección estática y de Git; no se ejecutaron los CLI, no se consultó NIC ni se inspeccionó el contenido de los CSV. El informe íntegro quedó en la respuesta de esa sesión; este resumen permite retomar el trabajo sin depender de ella.

En la comprobación del 2026-10-12, `git status -sb` muestra `main...origin/main`, sin indicador de divergencia, con modificaciones preexistentes en `AGENTS.md`, tres documentos de continuidad y dos CSV operacionales; `docs/AUDITORIA_LIMPIEZA_PROYECTO.md` figura eliminado, y hay documentos nuevos sin seguimiento en `docs/` y `docs/archivados/`. No se verificó el estado remoto en red. `git ls-files` confirma que tres CSV bajo `archivo/` y `entrada/candidatos.txt` siguen rastreados, aunque las reglas del proyecto prohíben versionar datos operacionales reales. No se examinó si contienen datos reales ni si se publicaron.

## Fuentes y límites de continuidad

- `docs/DECISIONS.md`: decisiones técnicas registradas y decisión vigente de posponer acciones correctivas.
- `docs/HANDOFF.md`: pendientes, orden de revisión y criterios para retomar.
- `docs/CONTEXTO_PROYECTO.md`, `docs/DECISIONES_TECNICAS.md` y `docs/PENDIENTES.md` son archivos sin seguimiento con contenido parcialmente duplicado; su vigencia y destino requieren decisión. Los informes de logging anteriores a la implementación contienen diagnósticos históricos y no describen por sí solos el estado actual.
- La consolidación actualizó referencias de estado en estos documentos de continuidad. Las demás acciones de la auditoría siguen pendientes. No se hicieron commits, push ni cambios en datos operacionales.
