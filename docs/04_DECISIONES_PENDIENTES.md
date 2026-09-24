# Decisiones pendientes para implementar logging

Este documento contiene solo decisiones que debe tomar el desarrollador antes de iniciar cambios.

## Decisiones confirmadas (2026-09-13)

Todas las decisiones se cerraron con la alternativa recomendada, salvo D-09 (acotada al pedido actual):

D-01 auditoria local de cada corrida; D-02 `logging` estandar; D-03 `logs/` local; D-04 texto legible;
D-05 inicio/fin/resumen/fallback/error, sin evento por dominio; D-06 parametros/conteos/rutas relativas,
sin listas de dominios ni respuestas de NIC; D-07 politica por tamano; D-08 conteo por estado + error
resumido (criterio a futuro, no aplica aun porque no se cubre caducidad); D-09 cobertura inicial
limitada a registrados/eliminados (`app/consulta_dominios_core.py`, `app/consulta_dominios.py`);
D-10 `RotatingFileHandler` con `maxBytes=5MB`, `backupCount=3`; D-11 humo controlado + pruebas sin red.

Implementado en `app/configuracion.py` (constantes de logging), `app/logging_dominios.py` (logger
idempotente) y `app/consulta_dominios_core.py` (eventos `inicio`, `fallback`, `error`, `fin`).
Verificado con prueba de humo simulando fallo de red (sin tocar NIC Chile): logger no duplica
handlers y correlaciona eventos por `run_id`.

| ID | Decision | Alternativas | Recomendacion | Impacto |
| -- | -------- | ------------ | ------------- | ------- |
| D-01 | Objetivo del log | Solo diagnostico local; auditoria de cada corrida; analisis automatizado. | Auditoria local de cada corrida con diagnostico basico. | Define campos y complejidad. |
| D-02 | Estrategia inicial | A: redireccion manual; B: `logging` estandar; C: JSON Lines/observabilidad ampliada. | B. | Determina si hay cambios de codigo. |
| D-03 | Ubicacion | `logs/`; ruta configurable; destino externo. | `logs/` local y ya ignorado por Git. | Afecta permisos, despliegue y recuperacion. |
| D-04 | Formato | Texto legible; JSON Lines; ambos. | Texto legible inicialmente. | Afecta consumo, facilidad de lectura y automatizacion. |
| D-05 | Granularidad | Solo inicio/fin/resumen; incluir fallback y errores; evento por dominio. | Inicio/fin/resumen/fallback/error, sin evento por dominio por defecto. | Afecta volumen y utilidad de diagnostico. |
| D-06 | Datos permitidos | Parametros y conteos; rutas absolutas; listas de dominios; respuestas de NIC. | Parametros no sensibles, conteos y rutas relativas; excluir listas y respuestas. | Riesgo de privacidad y volumen. |
| D-07 | Retencion | Sin limite; por dias; por tamano; borrado manual. | Politica explicita por tamano o antiguedad tras medir uso. | Evita crecimiento ilimitado. |
| D-08 | Error por dominio en caducidad | Solo conteo; detalle resumido; detalle completo. | Conteo por estado y error resumido, sujeto a revision de datos expuestos. | Mejora diagnostico con posible aumento de volumen. |
| D-09 | Cobertura inicial | Solo registrados/eliminados; todos los CLI; tambien checkpoint. | Todos los CLI y eventos relevantes del checkpoint. | Define archivos y pruebas afectadas. |
| D-10 | Modelo para implementacion | Luna bajo/medio; Terra bajo/medio; otro disponible. | Luna medio para tareas locales con diseno cerrado y Terra medio para integracion concurrente/revision. | Afecta estrategia de trabajo, no el comportamiento de produccion. |
| D-11 | Validacion | Solo inspeccion; humo controlado; pruebas automatizadas sin red. | Humo controlado y pruebas sin red si se implementan cambios de codigo. | Determina nivel de evidencia antes de cierre. |
