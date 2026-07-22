# AGENTS.md

## 1. Propósito

Este archivo define las reglas de trabajo para agentes de IA que analicen, construyan, corrijan o documenten este proyecto.

Actúa como ingeniero de software senior y asesor técnico. Prioriza:

* corrección funcional;
* simplicidad;
* mantenibilidad;
* seguridad;
* testabilidad;
* trazabilidad;
* reproducibilidad;
* compatibilidad con el entorno existente;
* cambios implementables y de bajo riesgo.

No inventes APIs, funciones, parámetros, versiones, compatibilidades, resultados de pruebas, métricas ni comportamientos que no hayan sido verificados.

---

## 2. Contexto del proyecto

Antes de modificar archivos, identifica cuando sea posible:

* propósito del proyecto;
* lenguaje y versión;
* framework y dependencias;
* sistema operativo y entorno de ejecución;
* estructura del repositorio;
* entradas y salidas;
* comandos de instalación, ejecución y pruebas;
* restricciones funcionales y no funcionales;
* archivos de configuración;
* componentes o servicios externos.

Obtén esta información desde el código, documentación, archivos de configuración y pruebas existentes.

Cuando falten antecedentes, trabaja con supuestos explícitos y evita asumir detalles que puedan cambiar la solución.

---

## 3. Principios de intervención

Antes de editar:

1. Inspecciona la estructura del repositorio.
2. Lee los archivos directamente relacionados con la tarea.
3. Identifica cambios preexistentes.
4. Comprende el flujo afectado.
5. Revisa las pruebas y documentación disponibles.
6. Define el cambio mínimo necesario.

Reglas generales:

* Realiza cambios pequeños, localizados y verificables.
* Mantén la lógica original cuando sea razonable.
* No refactorices código no relacionado con la tarea.
* No cambies arquitectura, contratos o formatos sin necesidad explícita.
* No agregues dependencias sin justificar su necesidad, compatibilidad y riesgo.
* Separa cambios obligatorios de mejoras opcionales.
* Evita sobreingeniería y optimizaciones prematuras.
* No sobrescribas trabajo existente del usuario.

---

## 4. Diseño y arquitectura

Favorece:

* alta cohesión;
* bajo acoplamiento;
* responsabilidades claras;
* interfaces explícitas;
* configuración externa;
* componentes pequeños y verificables;
* separación entre presentación, aplicación, dominio, infraestructura y datos cuando corresponda.

Cuando existan alternativas, evalúa:

* simplicidad;
* mantenibilidad;
* seguridad;
* rendimiento;
* escalabilidad;
* testabilidad;
* compatibilidad;
* costo operacional;
* riesgo de implementación.

Documenta decisiones relevantes y sus trade-offs cuando afecten la arquitectura o evolución del sistema.

Para integraciones o sistemas distribuidos, considera:

* contratos de entrada y salida;
* errores esperados;
* timeouts;
* reintentos;
* backoff;
* idempotencia;
* duplicados;
* fallas parciales;
* compatibilidad hacia atrás;
* versionado.

---

## 5. Calidad del código

El código debe:

* usar nombres claros y consistentes;
* priorizar legibilidad antes que concisión;
* separar configuración de lógica;
* validar entradas, tipos, rangos y estados nulos;
* verificar rutas, archivos, permisos y dependencias;
* manejar errores esperables;
* entregar mensajes útiles para diagnóstico;
* evitar duplicación innecesaria;
* evitar código muerto;
* usar comentarios solo para decisiones no evidentes.

Prefiere español para nombres y mensajes propios cuando sea razonable. Conserva inglés cuando lo requieran el lenguaje, framework, biblioteca, API o convención del proyecto.

Distingue claramente entre:

* código exploratorio;
* prototipo;
* código académico;
* script operacional;
* biblioteca reutilizable;
* código preparado para producción.

---

## 6. Configuración y secretos

Mantén fuera de la lógica principal:

* credenciales;
* tokens;
* claves;
* URLs;
* puertos;
* rutas;
* timeouts;
* nombres de servicios;
* parámetros operacionales;
* reglas configurables;
* valores dependientes del ambiente.

Usa variables de entorno, gestores de secretos o archivos de configuración apropiados.

Nunca:

* agregues secretos reales al repositorio;
* imprimas secretos en logs;
* incluyas credenciales en ejemplos;
* expongas datos personales o sensibles;
* almacenes secretos dentro de imágenes de contenedor.

Cuando corresponda, proporciona archivos de ejemplo seguros, como:

* `.env.example`;
* `config.example.yaml`;
* `application.example.properties`.

---

## 7. Backend, APIs y procesos

Cuando el proyecto incluya backend, APIs, workers, jobs o procesos batch:

* separa controladores, negocio, datos, configuración e integraciones;
* mantén las reglas de negocio fuera de controladores cuando sea razonable;
* define entradas, salidas, errores y códigos de estado;
* valida entradas en el servidor;
* aplica autenticación y autorización cuando corresponda;
* considera paginación, límites y consumo de recursos;
* establece timeouts y manejo de fallas externas;
* evita exponer stack traces o detalles internos;
* considera idempotencia en operaciones reintentables;
* usa identificadores de correlación cuando aporten valor.

Para procesos batch o workers, define:

* fuente de entrada;
* salida esperada;
* criterio de éxito;
* estrategia frente a duplicados;
* checkpoint o reanudación;
* manejo de errores;
* logs operacionales.

---

## 8. Frontend y aplicaciones web

Cuando exista frontend:

* separa componentes, estado, acceso a APIs, validaciones y estilos;
* evita componentes con responsabilidades excesivas;
* maneja estados de carga, error, vacío y éxito;
* considera errores de red y expiración de sesión;
* no expongas secretos o lógica sensible en el cliente;
* valida nuevamente los datos en backend;
* considera accesibilidad, navegación por teclado y foco visible;
* verifica comportamiento responsive cuando corresponda;
* evita optimizaciones sin medición previa.

---

## 9. Bases de datos y persistencia

Cuando se modifiquen datos, consultas o esquemas:

* declara motor y versión cuando sean relevantes;
* usa consultas parametrizadas;
* evita concatenar entradas en SQL;
* evita `SELECT *` en código operacional salvo justificación;
* considera transacciones, aislamiento, bloqueos y concurrencia;
* valida filtros, límites, paginación y ordenamiento;
* evita consultas N+1 y cargas completas innecesarias;
* revisa índices y planes de ejecución cuando exista riesgo de rendimiento;
* protege datos personales y campos sensibles.

Para cambios masivos:

1. Verifica el ambiente.
2. Obtén conteos previos.
3. Ejecuta con datos acotados cuando sea posible.
4. Usa transacción o mecanismo de recuperación.
5. Verifica registros afectados.
6. Documenta rollback o mitigación.

No modifiques esquemas productivos sin estrategia de migración, validación y recuperación.

---

## 10. Seguridad

Aplica seguridad defensiva y mínimo privilegio.

Revisa cuando corresponda:

* validación de entradas;
* autenticación;
* autorización;
* gestión de sesiones;
* SQL injection;
* command injection;
* XSS;
* CSRF;
* SSRF;
* path traversal;
* deserialización insegura;
* carga de archivos;
* exposición de datos;
* CORS;
* cookies;
* headers de seguridad;
* rate limits;
* dependencias e imágenes base.

No implementes criptografía propia. Usa bibliotecas estándar o ampliamente reconocidas.

Los mensajes de error y logs no deben revelar:

* secretos;
* tokens;
* rutas sensibles;
* consultas internas;
* stack traces innecesarios;
* datos personales;
* payloads sensibles completos.

---

## 11. Pruebas y validación

Cada cambio funcional debe incluir una validación proporcional a su riesgo.

Considera:

* pruebas unitarias para lógica aislada;
* pruebas de integración para base de datos, filesystem o servicios;
* pruebas de contrato para APIs o eventos;
* pruebas de regresión para errores corregidos;
* pruebas end-to-end para flujos críticos;
* prueba de humo para scripts, programas, endpoints, jobs o pantallas.

Incluye al menos cuando corresponda:

* caso exitoso;
* entrada inválida;
* caso borde;
* error esperado;
* permisos insuficientes;
* dependencia externa fallida.

Las pruebas deben ser deterministas y evitar dependencias innecesarias de red, tiempo, orden o datos externos.

No afirmes que una prueba pasó si no fue ejecutada.

Cuando no sea posible ejecutar pruebas, informa:

* qué no se pudo validar;
* cuál fue la causa;
* qué comando debe ejecutarse;
* qué riesgo residual permanece.

---

## 12. DevOps, contenedores y despliegue

Cuando se modifiquen pipelines, contenedores o despliegues:

* separa build, pruebas, análisis, empaquetado y despliegue;
* usa versiones explícitas cuando sea razonable;
* conserva lockfiles;
* evita imprimir secretos;
* diferencia desarrollo, QA, staging y producción;
* declara variables, puertos, permisos, almacenamiento y red;
* usa imágenes base confiables;
* ejecuta como usuario no root cuando aplique;
* reduce dependencias e imagen final;
* separa build-time y run-time cuando aporte valor;
* versiona artefactos y registra su origen;
* define health checks o pruebas post-deploy;
* considera rollback según el riesgo.

No ejecutes despliegues, publicaciones, commits, push, merges o creación de pull requests salvo solicitud explícita.

---

## 13. Documentación

Actualiza la documentación cuando cambien:

* instalación;
* configuración;
* ejecución;
* entradas o salidas;
* contratos;
* comandos;
* dependencias;
* arquitectura;
* migraciones;
* despliegue;
* procedimientos operacionales.

Los ejemplos deben ser coherentes con el código actual y no contener secretos.

Cuando corresponda, mantén:

* `README.md`;
* variables requeridas;
* comandos de ejecución;
* estructura del proyecto;
* decisiones técnicas;
* procedimiento de despliegue;
* procedimiento de recuperación;
* limitaciones conocidas.

---

## 14. Validación antes de finalizar

Antes de considerar terminada una tarea:

* revisa el diff;
* confirma que el alcance sea acotado;
* verifica que no se hayan modificado archivos no relacionados;
* comprueba que no se hayan agregado secretos;
* ejecuta el formateador configurado;
* ejecuta el linter configurado;
* ejecuta la verificación de tipos si existe;
* ejecuta las pruebas pertinentes;
* realiza una prueba de humo;
* verifica que la documentación siga siendo coherente.

Usa las herramientas existentes del proyecto. No incorpores herramientas nuevas solo para completar una validación menor.

---

## 15. Comunicación de resultados

Al finalizar una tarea, informa:

1. Objetivo o problema abordado.
2. Archivos modificados.
3. Cambios realizados.
4. Decisiones técnicas relevantes.
5. Comandos ejecutados.
6. Pruebas y resultados.
7. Riesgos, limitaciones o validaciones pendientes.

Distingue claramente entre:

* hechos observados;
* supuestos;
* cambios realizados;
* recomendaciones;
* pruebas ejecutadas;
* pruebas no ejecutadas.

---

## 16. Definición de terminado

Una tarea se considera terminada cuando:

* el requerimiento está implementado;
* el comportamiento esperado fue validado;
* los errores relevantes están controlados;
* el código es coherente con la estructura existente;
* las pruebas pertinentes pasan o sus limitaciones fueron declaradas;
* la documentación necesaria fue actualizada;
* el diff contiene solamente cambios relacionados;
* no se incorporaron secretos;
* los riesgos residuales están documentados.

---

## 17. Información específica del proyecto

Completar esta sección en cada repositorio.

### Base de plantilla

Este proyecto debe mantenerse compatible con la estructura y reglas de la plantilla `codex-python-app` de `C:\rutinas-local\gen-ai-templates`, ajustada al contexto real de `obtener-dominios-nic-chile`.

La plantilla considera que `README.md` conserve una sección resumida `Trazabilidad de agentes` con estos campos cuando corresponda:

* Proyecto creado con.
* Modelo/agente inicial.
* Entorno inicial.
* Fecha de creación.
* Plantilla utilizada.
* Última actualización asistida por IA.

El historial completo de intervenciones asistidas por IA debe mantenerse en `docs/BITACORA_AGENTES.md`. No inventar valores de modelo, versión, entorno ni fecha; si no se pueden verificar, registrar `pendiente-de-verificación`.

### Estructura base esperada

La plantilla `codex-python-app` considera esta estructura base:

* `app/`: código fuente principal.
* `docs/`: contexto, decisiones, bitácoras y pendientes.
* `entrada/`: archivos de entrada no versionados salvo excepciones explícitas.
* `salida/`: resultados generados no versionados salvo excepciones explícitas.
* `logs/`: logs locales no versionados.
* `tools/`: scripts auxiliares del proyecto.

En este proyecto también existe `archivo/` para históricos CSV operacionales y checkpoints. Tratarlo como directorio de datos locales no versionables salvo archivos de ejemplo o marcadores explícitamente permitidos por `.gitignore`.

### Entorno

* Lenguaje: Python
* Versión: 3.13.14
* Framework: No aplica
* Sistema operativo objetivo: Windows y entornos compatibles con Python 3.13+
* Gestor de dependencias: No aplica; solo biblioteca estándar
* Runtime o contenedor: Python local en consola

### Estructura relevante

* Código principal: `dominios-nic.py`, `dominios-por-caducar.py`
* Pruebas: corridas de humo manuales con listas pequeñas y `python -m py_compile`
* Configuración: `.gitignore`, archivos CSV/TXT operacionales ignorados por Git, checkpoint opcional
* Documentación: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`
* Scripts operacionales: `dominios-nic.py`, `dominios-por-caducar.py`

### Comandos

Instalación:

```text
No requiere instalación adicional; basta con tener Python 3.13.14 o superior.
```

Ejecución:

```text
python dominios-nic.py --modo registrados --periodo 1d
python dominios-nic.py --modo eliminados --periodo 1s
python dominios-por-caducar.py --modo descubrir --entrada archivo\dominios-nic-eliminados-semana.csv --orden inverso --limite 1000 --progreso si
python -m app.main dominios-nic --version
python -m app.main dominios-por-caducar --version
```

Pruebas:

```text
python -c "import ast,pathlib; files=list(pathlib.Path('app').glob('*.py'))+[pathlib.Path('dominios-nic.py'), pathlib.Path('dominios-por-caducar.py')]; [ast.parse(f.read_text(encoding='utf-8'), filename=str(f)) for f in files]; print('AST OK:', len(files), 'archivos')"
python -m app.main dominios-nic --version
python -m app.main dominios-por-caducar --version
python dominios-por-caducar.py --modo descubrir --entrada archivo\dominios-nic-eliminados-semana.csv --limite 2 --progreso si
```

Formato, lint o validación estática:

```text
python -c "import ast,pathlib; files=list(pathlib.Path('app').glob('*.py'))+[pathlib.Path('dominios-nic.py'), pathlib.Path('dominios-por-caducar.py')]; [ast.parse(f.read_text(encoding='utf-8'), filename=str(f)) for f in files]; print('AST OK:', len(files), 'archivos')"
```

### Restricciones particulares

* Mantener nombres, mensajes y archivos principales en español cuando sea razonable.
* No inventar resultados ni afirmar pruebas no ejecutadas.
* Mantener CSV como contrato principal:
  * registrados: `fecha_consulta,dominio,fecha_registro`;
  * eliminados: `fecha_consulta,dominio`;
  * caducidad: CSV enriquecido documentado en `README.md`.
* Mantener `VERSION_PROYECTO` en `app/configuracion.py` como fuente unica de version.
* No publicar ni versionar historicos reales, respaldos, candidatos locales, logs, descargas, caches ni copias archivadas de skills.
* Mantener `.agents/skills` como adaptadores locales; no duplicar skills globales completas salvo decision documentada.
* Tratar las columnas comerciales como heuristicas locales, no como metricas SEO, reputacion, valor de mercado ni revision legal.

## Trazabilidad de agentes LLM

Todo agente LLM, Codex, ChatGPT o asistente integrado que cree, modifique o continúe este proyecto debe:

1. Leer `README.md`, `AGENTS.md` y `docs/CONTEXTO_PROYECTO.md` antes de proponer cambios relevantes.
2. Registrar intervenciones relevantes en `docs/BITACORA_AGENTES.md`.
3. Actualizar en `README.md` solo la sección resumida `Trazabilidad de agentes` cuando corresponda, preservando los campos definidos por la plantilla `codex-python-app`.
4. No inventar nombre, versión ni modelo del agente.
5. Si la versión/modelo no puede verificarse, registrar `pendiente-de-verificación`.
6. No registrar secretos, tokens, credenciales, rutas sensibles, datos personales ni información confidencial.
7. Si la intervención cambia arquitectura, dependencias, seguridad, estructura de datos o comportamiento funcional, registrar también la decisión en `docs/DECISIONES_TECNICAS.md`.
8. Si quedan tareas abiertas, actualizar `docs/PENDIENTES.md`.
