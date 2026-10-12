# Relevo operativo

Actualizado: 2026-10-12 (America/Santiago).

## Decisión de la sesión

El usuario indicó que las acciones correctivas de la auditoría de contratos del 2026-10-11 se aplicarán en otro momento. Esta consolidación registra el estado y los pendientes; no autoriza ejecutar esas acciones, publicar, hacer commit ni modificar los datos locales.

## Pendientes de la auditoría documental

1. **ACT-01 / DOC-01 — Prioridad P1, requiere decisión del usuario.** Revisar los archivos operacionales que Git ya rastrea: `archivo/dominios-nic-eliminados-semana.csv`, `archivo/dominios-nic-registrados-mes.csv`, `archivo/dominios-por-caducar.csv` y `entrada/candidatos.txt`. Clasificar su contenido y decidir su tratamiento en Git sin borrar copias locales. No se verificó su contenido ni publicación remota.
2. **ACT-02 / DOC-01 — P1, propuesta lista para revisión posterior.** Ajustar `.gitignore` para cubrir las clases de datos locales definidas en `AGENTS.md`, conservando `.gitkeep` y ejemplos neutros. Verificar con `git check-ignore`. Esto no deja de rastrear archivos ya incorporados.
3. **ACT-03 / DOC-02 — P1, propuesta lista para revisión posterior.** Corregir referencias y afirmaciones de estado Git en los documentos de continuidad. `CONTEXT.md` y este `HANDOFF.md` quedaron actualizados en esta consolidación; al retomar, comprobar el estado nuevamente y revisar referencias restantes antes de dar la acción por cerrada.
4. **ACT-04 / DOC-03 — P1, requiere decisión editorial.** Establecer la fuente vigente entre `docs/DECISIONS.md` y `docs/DECISIONES_TECNICAS.md`, y entre los pares de contexto y pendientes; decidir el destino de los documentos archivados y marcar como históricos los diagnósticos de logging previos a su implementación. No mover ni eliminar archivos por inferencia.
5. **ACT-05 / DOC-04 — P2, requiere decisión del mantenedor.** Definir un canal privado real para reportes en `SECURITY.md` y expectativas de respuesta sostenibles.
6. **ACT-06 / DOC-05 — P2, propuesta lista para revisión posterior.** Precisar en `CONTRIBUTING.md` la regla de versiones en encabezados frente a `VERSION_PROYECTO` como fuente única.

## Otros pendientes preexistentes

- Crear pruebas automatizadas sin red para parseo CSV, deduplicación, salida enriquecida y checkpoint.
- Decidir si conservar las copias de skills bajo `.agents/_copias-reutilizables-no-usar/`; no eliminarlas por esta consolidación.

## Antes de retomar o publicar

- Releer `AGENTS.md`, `README.md` y `docs/DECISIONS.md`; comprobar `git status -sb`, `git ls-files archivo entrada` y la diferencia real con `origin/main`. El estado anterior es una observación fechada, no una garantía futura.
- Mantener separados los cambios preexistentes del trabajo nuevo. No abrir ni transformar los CSV operacionales sin propósito y autorización específicos.
- Resolver el rastreo de datos y revisar el alcance de publicación antes de cualquier commit o push. El árbol ya tenía cambios preexistentes; no se preparó una publicación.

## Validación de esta consolidación

Solo lectura de contratos y estado Git antes de editar, seguida por revisión de los tres documentos de continuidad. No se ejecutaron pruebas Python, consultas a NIC ni comprobaciones del remoto en red porque no hubo cambios funcionales y los datos operacionales están fuera del alcance.
