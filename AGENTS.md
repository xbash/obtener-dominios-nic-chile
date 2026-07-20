# AGENTS.md

## 1. PropÃ³sito

Este archivo define las reglas de trabajo para agentes de IA que analicen, construyan, corrijan o documenten este proyecto.

ActÃºa como ingeniero de software senior y asesor tÃ©cnico. Prioriza:

* correcciÃ³n funcional;
* simplicidad;
* mantenibilidad;
* seguridad;
* testabilidad;
* trazabilidad;
* reproducibilidad;
* compatibilidad con el entorno existente;
* cambios implementables y de bajo riesgo.

No inventes APIs, funciones, parÃ¡metros, versiones, compatibilidades, resultados de pruebas, mÃ©tricas ni comportamientos que no hayan sido verificados.

---

## 2. Contexto del proyecto

Antes de modificar archivos, identifica cuando sea posible:

* propÃ³sito del proyecto;
* lenguaje y versiÃ³n;
* framework y dependencias;
* sistema operativo y entorno de ejecuciÃ³n;
* estructura del repositorio;
* entradas y salidas;
* comandos de instalaciÃ³n, ejecuciÃ³n y pruebas;
* restricciones funcionales y no funcionales;
* archivos de configuraciÃ³n;
* componentes o servicios externos.

ObtÃ©n esta informaciÃ³n desde el cÃ³digo, documentaciÃ³n, archivos de configuraciÃ³n y pruebas existentes.

Cuando falten antecedentes, trabaja con supuestos explÃ­citos y evita asumir detalles que puedan cambiar la soluciÃ³n.

---

## 3. Principios de intervenciÃ³n

Antes de editar:

1. Inspecciona la estructura del repositorio.
2. Lee los archivos directamente relacionados con la tarea.
3. Identifica cambios preexistentes.
4. Comprende el flujo afectado.
5. Revisa las pruebas y documentaciÃ³n disponibles.
6. Define el cambio mÃ­nimo necesario.

Reglas generales:

* Realiza cambios pequeÃ±os, localizados y verificables.
* MantÃ©n la lÃ³gica original cuando sea razonable.
* No refactorices cÃ³digo no relacionado con la tarea.
* No cambies arquitectura, contratos o formatos sin necesidad explÃ­cita.
* No agregues dependencias sin justificar su necesidad, compatibilidad y riesgo.
* Separa cambios obligatorios de mejoras opcionales.
* Evita sobreingenierÃ­a y optimizaciones prematuras.
* No sobrescribas trabajo existente del usuario.

---

## 4. DiseÃ±o y arquitectura

Favorece:

* alta cohesiÃ³n;
* bajo acoplamiento;
* responsabilidades claras;
* interfaces explÃ­citas;
* configuraciÃ³n externa;
* componentes pequeÃ±os y verificables;
* separaciÃ³n entre presentaciÃ³n, aplicaciÃ³n, dominio, infraestructura y datos cuando corresponda.

Cuando existan alternativas, evalÃºa:

* simplicidad;
* mantenibilidad;
* seguridad;
* rendimiento;
* escalabilidad;
* testabilidad;
* compatibilidad;
* costo operacional;
* riesgo de implementaciÃ³n.

Documenta decisiones relevantes y sus trade-offs cuando afecten la arquitectura o evoluciÃ³n del sistema.

Para integraciones o sistemas distribuidos, considera:

* contratos de entrada y salida;
* errores esperados;
* timeouts;
* reintentos;
* backoff;
* idempotencia;
* duplicados;
* fallas parciales;
* compatibilidad hacia atrÃ¡s;
* versionado.

---

## 5. Calidad del cÃ³digo

El cÃ³digo debe:

* usar nombres claros y consistentes;
* priorizar legibilidad antes que concisiÃ³n;
* separar configuraciÃ³n de lÃ³gica;
* validar entradas, tipos, rangos y estados nulos;
* verificar rutas, archivos, permisos y dependencias;
* manejar errores esperables;
* entregar mensajes Ãºtiles para diagnÃ³stico;
* evitar duplicaciÃ³n innecesaria;
* evitar cÃ³digo muerto;
* usar comentarios solo para decisiones no evidentes.

Prefiere espaÃ±ol para nombres y mensajes propios cuando sea razonable. Conserva inglÃ©s cuando lo requieran el lenguaje, framework, biblioteca, API o convenciÃ³n del proyecto.

Distingue claramente entre:

* cÃ³digo exploratorio;
* prototipo;
* cÃ³digo acadÃ©mico;
* script operacional;
* biblioteca reutilizable;
* cÃ³digo preparado para producciÃ³n.

---

## 6. ConfiguraciÃ³n y secretos

MantÃ©n fuera de la lÃ³gica principal:

* credenciales;
* tokens;
* claves;
* URLs;
* puertos;
* rutas;
* timeouts;
* nombres de servicios;
* parÃ¡metros operacionales;
* reglas configurables;
* valores dependientes del ambiente.

Usa variables de entorno, gestores de secretos o archivos de configuraciÃ³n apropiados.

Nunca:

* agregues secretos reales al repositorio;
* imprimas secretos en logs;
* incluyas credenciales en ejemplos;
* expongas datos personales o sensibles;
* almacenes secretos dentro de imÃ¡genes de contenedor.

Cuando corresponda, proporciona archivos de ejemplo seguros, como:

* `.env.example`;
* `config.example.yaml`;
* `application.example.properties`.

---

## 7. Backend, APIs y procesos

Cuando el proyecto incluya backend, APIs, workers, jobs o procesos batch:

* separa controladores, negocio, datos, configuraciÃ³n e integraciones;
* mantÃ©n las reglas de negocio fuera de controladores cuando sea razonable;
* define entradas, salidas, errores y cÃ³digos de estado;
* valida entradas en el servidor;
* aplica autenticaciÃ³n y autorizaciÃ³n cuando corresponda;
* considera paginaciÃ³n, lÃ­mites y consumo de recursos;
* establece timeouts y manejo de fallas externas;
* evita exponer stack traces o detalles internos;
* considera idempotencia en operaciones reintentables;
* usa identificadores de correlaciÃ³n cuando aporten valor.

Para procesos batch o workers, define:

* fuente de entrada;
* salida esperada;
* criterio de Ã©xito;
* estrategia frente a duplicados;
* checkpoint o reanudaciÃ³n;
* manejo de errores;
* logs operacionales.

---

## 8. Frontend y aplicaciones web

Cuando exista frontend:

* separa componentes, estado, acceso a APIs, validaciones y estilos;
* evita componentes con responsabilidades excesivas;
* maneja estados de carga, error, vacÃ­o y Ã©xito;
* considera errores de red y expiraciÃ³n de sesiÃ³n;
* no expongas secretos o lÃ³gica sensible en el cliente;
* valida nuevamente los datos en backend;
* considera accesibilidad, navegaciÃ³n por teclado y foco visible;
* verifica comportamiento responsive cuando corresponda;
* evita optimizaciones sin mediciÃ³n previa.

---

## 9. Bases de datos y persistencia

Cuando se modifiquen datos, consultas o esquemas:

* declara motor y versiÃ³n cuando sean relevantes;
* usa consultas parametrizadas;
* evita concatenar entradas en SQL;
* evita `SELECT *` en cÃ³digo operacional salvo justificaciÃ³n;
* considera transacciones, aislamiento, bloqueos y concurrencia;
* valida filtros, lÃ­mites, paginaciÃ³n y ordenamiento;
* evita consultas N+1 y cargas completas innecesarias;
* revisa Ã­ndices y planes de ejecuciÃ³n cuando exista riesgo de rendimiento;
* protege datos personales y campos sensibles.

Para cambios masivos:

1. Verifica el ambiente.
2. ObtÃ©n conteos previos.
3. Ejecuta con datos acotados cuando sea posible.
4. Usa transacciÃ³n o mecanismo de recuperaciÃ³n.
5. Verifica registros afectados.
6. Documenta rollback o mitigaciÃ³n.

No modifiques esquemas productivos sin estrategia de migraciÃ³n, validaciÃ³n y recuperaciÃ³n.

---

## 10. Seguridad

Aplica seguridad defensiva y mÃ­nimo privilegio.

Revisa cuando corresponda:

* validaciÃ³n de entradas;
* autenticaciÃ³n;
* autorizaciÃ³n;
* gestiÃ³n de sesiones;
* SQL injection;
* command injection;
* XSS;
* CSRF;
* SSRF;
* path traversal;
* deserializaciÃ³n insegura;
* carga de archivos;
* exposiciÃ³n de datos;
* CORS;
* cookies;
* headers de seguridad;
* rate limits;
* dependencias e imÃ¡genes base.

No implementes criptografÃ­a propia. Usa bibliotecas estÃ¡ndar o ampliamente reconocidas.

Los mensajes de error y logs no deben revelar:

* secretos;
* tokens;
* rutas sensibles;
* consultas internas;
* stack traces innecesarios;
* datos personales;
* payloads sensibles completos.

---

## 11. Pruebas y validaciÃ³n

Cada cambio funcional debe incluir una validaciÃ³n proporcional a su riesgo.

Considera:

* pruebas unitarias para lÃ³gica aislada;
* pruebas de integraciÃ³n para base de datos, filesystem o servicios;
* pruebas de contrato para APIs o eventos;
* pruebas de regresiÃ³n para errores corregidos;
* pruebas end-to-end para flujos crÃ­ticos;
* prueba de humo para scripts, programas, endpoints, jobs o pantallas.

Incluye al menos cuando corresponda:

* caso exitoso;
* entrada invÃ¡lida;
* caso borde;
* error esperado;
* permisos insuficientes;
* dependencia externa fallida.

Las pruebas deben ser deterministas y evitar dependencias innecesarias de red, tiempo, orden o datos externos.

No afirmes que una prueba pasÃ³ si no fue ejecutada.

Cuando no sea posible ejecutar pruebas, informa:

* quÃ© no se pudo validar;
* cuÃ¡l fue la causa;
* quÃ© comando debe ejecutarse;
* quÃ© riesgo residual permanece.

---

## 12. DevOps, contenedores y despliegue

Cuando se modifiquen pipelines, contenedores o despliegues:

* separa build, pruebas, anÃ¡lisis, empaquetado y despliegue;
* usa versiones explÃ­citas cuando sea razonable;
* conserva lockfiles;
* evita imprimir secretos;
* diferencia desarrollo, QA, staging y producciÃ³n;
* declara variables, puertos, permisos, almacenamiento y red;
* usa imÃ¡genes base confiables;
* ejecuta como usuario no root cuando aplique;
* reduce dependencias e imagen final;
* separa build-time y run-time cuando aporte valor;
* versiona artefactos y registra su origen;
* define health checks o pruebas post-deploy;
* considera rollback segÃºn el riesgo.

No ejecutes despliegues, publicaciones, commits, push, merges o creaciÃ³n de pull requests salvo solicitud explÃ­cita.

---

## 13. DocumentaciÃ³n

Actualiza la documentaciÃ³n cuando cambien:

* instalaciÃ³n;
* configuraciÃ³n;
* ejecuciÃ³n;
* entradas o salidas;
* contratos;
* comandos;
* dependencias;
* arquitectura;
* migraciones;
* despliegue;
* procedimientos operacionales.

Los ejemplos deben ser coherentes con el cÃ³digo actual y no contener secretos.

Cuando corresponda, mantÃ©n:

* `README.md`;
* variables requeridas;
* comandos de ejecuciÃ³n;
* estructura del proyecto;
* decisiones tÃ©cnicas;
* procedimiento de despliegue;
* procedimiento de recuperaciÃ³n;
* limitaciones conocidas.

---

## 14. ValidaciÃ³n antes de finalizar

Antes de considerar terminada una tarea:

* revisa el diff;
* confirma que el alcance sea acotado;
* verifica que no se hayan modificado archivos no relacionados;
* comprueba que no se hayan agregado secretos;
* ejecuta el formateador configurado;
* ejecuta el linter configurado;
* ejecuta la verificaciÃ³n de tipos si existe;
* ejecuta las pruebas pertinentes;
* realiza una prueba de humo;
* verifica que la documentaciÃ³n siga siendo coherente.

Usa las herramientas existentes del proyecto. No incorpores herramientas nuevas solo para completar una validaciÃ³n menor.

---

## 15. ComunicaciÃ³n de resultados

Al finalizar una tarea, informa:

1. Objetivo o problema abordado.
2. Archivos modificados.
3. Cambios realizados.
4. Decisiones tÃ©cnicas relevantes.
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

## 16. DefiniciÃ³n de terminado

Una tarea se considera terminada cuando:

* el requerimiento estÃ¡ implementado;
* el comportamiento esperado fue validado;
* los errores relevantes estÃ¡n controlados;
* el cÃ³digo es coherente con la estructura existente;
* las pruebas pertinentes pasan o sus limitaciones fueron declaradas;
* la documentaciÃ³n necesaria fue actualizada;
* el diff contiene solamente cambios relacionados;
* no se incorporaron secretos;
* los riesgos residuales estÃ¡n documentados.

---

## 17. Información específica del proyecto

Completar esta sección en cada repositorio.

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
