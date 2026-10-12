# Plan de ejecucion: logging persistente

## Estado de este documento

Es un plan no ejecutado. Ninguna etapa autoriza cambios hasta que el desarrollador seleccione una alternativa y solicite implementacion.

## Alternativas

| Alternativa | Descripcion | Ventaja | Limite |
| --- | --- | --- | --- |
| A. Operacional sin codigo | Redirigir manualmente `stdout` y `stderr` desde PowerShell en cada corrida. | Cero cambios al proyecto. | No es uniforme, depende del operador y no incorpora ID, duracion ni estructura. |
| B. Minima viable | Usar `logging` estandar con un logger comun y un archivo local por fecha o por ejecucion. Registrar inicio, fin, error y resumen. | Bajo riesgo, sin dependencias, trazabilidad suficiente. | Requiere decidir formato y retencion. |
| C. Ampliada | Agregar JSON Lines, rotacion configurable, mayor detalle por dominio y/o metricas de operacion. | Facilita analisis automatizado. | Mayor volumen, complejidad y riesgo de registrar datos innecesarios. |

**Alternativa minima viable y recomendada: B.** A solo sirve como contencion manual; C no se justifica con la evidencia disponible.

## Etapas propuestas

| Etapa | Objetivo | Archivos potencialmente afectados | Tipo | Complejidad | Riesgo | Beneficio | Dependencias | Validacion | Modelo minimo capaz / esfuerzo | Justificacion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0. Decision de contrato | Acordar formato, ubicacion, retencion, campos y tratamiento de errores. | `docs/`, posiblemente `README.md` | Diseno/documentacion | Baja | Bajo | Evita implementar supuestos. | Decisiones del desarrollador. | Revision del contrato de eventos. | Terra medio, si esta disponible. | Requiere trade-offs transversales; no hay datos para afirmar costos o calidad. |
| 1. Configuracion comun | Definir ruta local, nombre del logger y limites de retencion sin valores magicos dispersos. | `app/configuracion.py`, nuevo modulo localizado de logging | Codigo/configuracion | Baja | Bajo | Un punto unico de politica. | Etapa 0. | Importacion sin crear archivos hasta inicializacion explicita. | Luna medio, si esta disponible. | Cambio acotado y mecanico una vez fijado el contrato. |
| 2. Inicializacion y eventos de consulta | Crear logger estandar idempotente; registrar inicio, fallback, error final y resumen de registrados/eliminados. | Nuevo modulo, `app/consulta_dominios_core.py`, posiblemente `app/consulta_dominios.py` | Codigo | Media | Bajo-Medio | Audita ambos modos principales sin alterar CSV. | Etapa 1. | Humo controlado: exito, fallback/fallo y confirmacion de un solo handler. | Luna medio; escalar a Terra medio si el contrato se vuelve ambiguo. | Flujo delimitado, con razonamiento moderado para no duplicar mensajes ni handlers. |
| 3. Integracion de caducidad | Registrar inicio, parametros seleccionados, resumen de estados, interrupcion y estado del checkpoint. | `app/dominios_por_caducar.py`, `app/checkpoint_dominios.py` | Codigo | Media | Medio | Hace trazable el flujo concurrente y reanudable. | Etapas 0-1. | Humo pequeno con progreso desactivado y prueba de interrupcion controlada. | Terra medio. | Concurrencia, checkpoint y errores por dominio requieren revisar interacciones. |
| 4. Politica de retencion | Implementar o documentar rotacion acotada. | Modulo de logging, configuracion, `README.md` | Codigo/documentacion | Baja | Bajo | Evita crecimiento indefinido. | Etapas 1-3 y decision de volumen esperado. | Generar/rotar archivos de prueba sin datos operacionales. | Luna bajo o medio. | Aplicacion mecanica de una politica ya decidida. |
| 5. Pruebas y documentacion | Agregar pruebas sin red y actualizar comandos/limitaciones. | Pruebas nuevas si se decide crearlas, `README.md`, documentacion tecnica | Pruebas/documentacion | Media | Bajo | Evidencia repetible de que el logging funciona. | Etapas 1-4. | Casos exito, error, permisos insuficientes y no duplicacion de handlers. | Luna medio para pruebas acotadas; Terra medio para revision final. | La revision transversal comprueba que no se degradaron los contratos CSV ni el flujo CLI. |

## Contrato minimo sugerido

- Destino local: `logs/`, ignorado por Git.
- Formato inicial: texto legible con timestamp, nivel, ID de ejecucion y mensaje; JSON Lines solo si el desarrollador necesita procesarlo automaticamente.
- Eventos minimos: `inicio`, `fallback`, `advertencia`, `error`, `interrupcion`, `fin`.
- Datos permitidos: modo, periodo, conteos, estados agregados, duracion, origen y rutas relativas.
- Datos excluidos: credenciales, headers completos, respuestas de NIC, contenido completo de entradas, listas completas de dominios y trazas innecesarias.
- Retencion: debe definirse antes de la implementacion; no se propone un numero sin evidencia de volumen o uso.

## Criterios de aceptacion futuros

1. Cada ejecucion de registrados, eliminados y caducidad deja inicio y cierre persistentes.
2. Un fallo de fuente o una interrupcion queda registrado sin ocultar el codigo de salida actual.
3. Los CSV y checkpoints conservan sus contratos actuales.
4. El logger no duplica lineas al invocarse desde wrappers o `app.main`.
5. Los logs no se versionan y no incluyen datos prohibidos.
6. La politica de retencion evita crecimiento ilimitado.

## Nota sobre modelos y tokens

Las recomendaciones de Luna y Terra son cualitativas y condicionales: esta auditoria no verifico disponibilidad, ventana de contexto, precios, latencia, capacidad ni calidad de esos modelos. La asignacion busca usar el modelo minimo capaz: Luna para cambios locales con contrato cerrado; Terra para decisiones ambiguas, concurrencia, trade-offs y revision transversal. No constituye un benchmark ni una promesa de ahorro de tokens.
