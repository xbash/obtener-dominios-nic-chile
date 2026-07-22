---
name: inicializar-proyecto-codex
description: Usa esta skill para crear o revisar la estructura base de un proyecto Codex con AGENTS.md, docs persistentes, skills, .vscode, README, CHANGELOG y carpetas estándar.
---

# Inicializar proyecto Codex

## Reglas
1. Verificar si ya existe AGENTS.md.
2. Verificar docs/CONTEXTO_PROYECTO.md, DECISIONES_TECNICAS.md, PENDIENTES.md, BITACORA_CODEX.md y REGISTRO_CAMBIOS.md.
3. Verificar .agents/skills/*/SKILL.md.
4. No sobrescribir archivos existentes sin confirmación.
5. Si falta estructura, proponer comandos PowerShell o Python.
6. Si se crean archivos, usar tokens del proyecto: nombre, fecha, objetivo, stack y tipo de proyecto.
7. Al finalizar, sugerir git status, git diff y commit inicial.

## Trazabilidad de agentes

| Campo | Valor |
|---|---|
| Proyecto creado con | {{AGENTE_NOMBRE}} |
| Modelo/agente inicial | {{AGENTE_VERSION}} |
| Entorno inicial | {{AGENTE_ENTORNO}} |
| Fecha de creación | {{FECHA_CREACION}} |
| Plantilla utilizada | {{PLANTILLA_PROYECTO}} |
| Última actualización asistida por IA | {{ULTIMA_ACTUALIZACION_IA}} |

Para el historial completo de intervenciones asistidas por IA, revisar:
`docs/BITACORA_AGENTES.md`.

## Trazabilidad obligatoria
1. Crear o verificar `README.md` con sección `Trazabilidad de agentes`.
2. Crear o verificar `docs/BITACORA_AGENTES.md`.
3. Registrar agente, modelo/versión, entorno, fecha, plantilla y acción.
4. No inventar modelo/versión; usar `pendiente-de-verificación` si no está disponible.
5. No sobrescribir historial existente.
6. Si se modifica una regla persistente, actualizar `AGENTS.md`.
7. Si se modifica una decisión técnica, actualizar `docs/DECISIONES_TECNICAS.md`.