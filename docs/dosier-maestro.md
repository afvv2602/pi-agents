# HOMELAB AI · DOSIER MAESTRO DEL PROYECTO

**Versión:** 0.3 — Sistema operativo del servidor secundario elegido
**Fecha:** 8 de noviembre de 2026
**Estado:** Raspberry operativa en LAN · sistema distribuido en diseño
**Proyecto existente:** `pi-agents`
**Repositorio:** https://github.com/afvv2602/pi-agents

---

# 1. Resumen ejecutivo

## 1.1. Visión del proyecto

Construir una **infraestructura doméstica distribuida, autogestionada y orientada a inteligencia artificial**, aprovechando tres dispositivos existentes:

1. Raspberry Pi 4 de 4 GB como controlador principal, disponible permanentemente.
2. Ordenador secundario con Linux como servidor de servicios, almacenamiento y procesamiento general.
3. Ordenador principal con Windows/Linux y GPU NVIDIA como nodo de computación de alto rendimiento.

El objetivo es crear un ecosistema capaz de ejecutar agentes de inteligencia artificial, automatizar tareas, compartir recursos, almacenar información y ofrecer servicios privados accesibles desde cualquier dispositivo autorizado.

El sistema tendrá un **orquestador propio desarrollado principalmente en Python**, encargado de decidir dónde, cuándo y cómo ejecutar los trabajos.

La infraestructura deberá seguir funcionando parcialmente aunque uno o varios nodos de cómputo estén apagados.

## 1.2. Filosofía de diseño

**Principio fundamental: la Raspberry coordina, el servidor secundario proporciona servicios y el ordenador principal aporta potencia de cálculo.**

Principios:

- **Local-first:** priorizar ejecución y almacenamiento locales.
- **Self-hosted:** mantener el control sobre infraestructura y datos.
- **Modular:** añadir o reemplazar componentes sin reconstruir todo.
- **Resiliente:** tolerar desconexiones y recuperar trabajos pendientes.
- **Hardware-aware:** adaptar las tareas a los recursos disponibles.
- **Cost-conscious:** minimizar llamadas a APIs comerciales.
- **Security by design:** aislar componentes y gestionar permisos.
- **Observable:** poder conocer el estado y las decisiones del sistema.
- **Incremental:** implementar por fases verificables.

No se pretende construir una infraestructura sobredimensionada desde el principio, sino una plataforma extensible.

---

# 2. Objetivos

## 2.1. Objetivos principales

### OBJ-01 · Orquestador distribuido propio

Desarrollar una plataforma central capaz de:

- Registrar los distintos nodos.
- Detectar su disponibilidad.
- Monitorizar recursos.
- Recibir y almacenar trabajos.
- Seleccionar el nodo de ejecución.
- Gestionar prioridades y dependencias.
- Reintentar trabajos fallidos.
- Almacenar resultados y errores.
- Coordinar agentes y herramientas.

### OBJ-02 · Inteligencia artificial local

Disponer de modelos de lenguaje ejecutados localmente, particularmente en la GPU NVIDIA.

Se busca ejecutar tareas de:

- Programación y revisión de código.
- Análisis de documentos.
- Generación de contenido estructurado.
- Consultas sobre conocimiento personal.
- Procesamiento de textos.
- Automatización asistida por IA.
- Coordinación de agentes especializados.

Los modelos deberán poder sustituirse sin modificar la arquitectura general.

### OBJ-03 · Infraestructura doméstica

Desplegar servicios propios, progresivamente:

- Servidor Linux permanente.
- NAS y almacenamiento compartido.
- VPN privada.
- Sistema de copias de seguridad.
- Contenedores Docker.
- Panel de administración.
- Monitorización y alertas.
- Servicios web internos.
- Automatizaciones programadas.

### OBJ-04 · Acceso multidispositivo

Permitir utilizar el sistema desde:

- Ordenador principal.
- Ordenador secundario.
- Mac.
- iPhone.
- iPad.
- Otros dispositivos autorizados.

Los usuarios deberán acceder mediante interfaces web, APIs o clientes específicos utilizando la red privada.

### OBJ-05 · Plataforma personal de agentes

Integrar progresivamente agentes para:

- Obsidian y gestión del conocimiento.
- Estudio de chino HSK1.
- Estudio AWS.
- Desarrollo de software.
- Administración del homelab.
- Gestión documental.
- Procesamiento y clasificación de información.

---

# 3. Inventario del hardware

## NODO-01 · Raspberry Pi

**Hostname verificado:** `pi-agents`. El nombre `pi-control` designa el rol propuesto.

| Componente | Especificación |
|---|---|
| Equipo | Raspberry Pi 4 Model B |
| Memoria | 4 GB RAM |
| Arquitectura | ARM64 |
| Sistema operativo | DietPi v10.8.2, Debian 13 (Trixie), ARM64 |
| Disponibilidad objetivo | 24/7 |
| Conectividad | Wi-Fi con reserva DHCP. SSH por Tailscale probado desde Windows en LAN |
| Almacenamiento | microSD de unos 64 GB. SSD USB de 111,8 GiB detectado, con partición NTFS sin montar. Desconexiones pendientes de diagnóstico ([INC-006](05-resolucion-problemas.md)) |
| Función | Controlador principal |

### Responsabilidades

- API de entrada.
- Orquestador central.
- Scheduler de tareas.
- Registro de nodos.
- Heartbeats y comprobaciones de salud.
- Cola persistente.
- Base de datos operativa.
- Automatizaciones ligeras.
- Supervisión del sistema.
- Control remoto de nodos.
- Wake-on-LAN cuando sea compatible.

### Restricciones

No cargar este nodo con inferencia pesada, bases de datos voluminosas ni servicios que comprometan la disponibilidad del coordinador.

**Decisión:** conservar la Raspberry como núcleo permanente del proyecto.

---

## NODO-02 · Ordenador secundario

**Identificador propuesto:** `home-server`

| Componente | Especificación |
|---|---|
| CPU | Intel Core i5, generación 8.ª/9.ª por confirmar |
| RAM | 8 GB |
| GPU | AMD Radeon RX 590 |
| Sistema operativo previsto | Debian 13 estable (amd64), sin escritorio. Instalación desde USB y acceso SSH pendientes de verificar |
| Almacenamiento | Pendiente de inventariar |
| Disponibilidad objetivo | 24/7, pendiente de confirmar |
| Función | Servidor general y worker |

### Responsabilidades

- Servicios Docker.
- Almacenamiento compartido.
- Futuro NAS.
- Servicios de archivos.
- Indexación documental.
- Procesamiento CPU.
- Bases de datos o servicios auxiliares.
- Workers de tareas Python.
- Automatizaciones generales.
- Monitorización y herramientas internas.
- Posible sistema de copias de seguridad.

### Limitaciones

Los 8 GB de RAM aconsejan empezar con un conjunto pequeño de servicios.

La Radeon RX 590 no debe considerarse una GPU de inferencia fiable hasta verificar experimentalmente su compatibilidad y rendimiento. No dispone del soporte ROCm habitual de las GPU AMD modernas.

Se estudiará Vulkan con llama.cpp, pero no condicionará la arquitectura inicial.

### Posibles ampliaciones

- Aumentar RAM a 16 GB si resulta necesario.
- Incorporar discos dedicados.
- Medir consumo en reposo.
- Evaluar si conviene conservar la RX 590.
- Añadir un SAI/UPS.

**Decisión propuesta:** convertir este equipo en el servidor doméstico principal de servicios y almacenamiento.

---

## NODO-03 · Ordenador principal

**Identificador propuesto:** `ai-worker`

| Componente | Especificación |
|---|---|
| CPU | AMD Ryzen 7 5800X |
| RAM | 32 GB |
| GPU | NVIDIA RTX 4060 Ti |
| VRAM | Pendiente de confirmar: 8 o 16 GB |
| Almacenamiento SSD | 1 TB M.2 |
| Almacenamiento HDD | 2 TB |
| Sistema operativo previsto | Dual boot Windows/Linux, instalación Linux pendiente de acreditar |
| Disponibilidad | Variable |
| Función | Computación e inferencia IA |

### Responsabilidades

- Ejecución de modelos LLM.
- Inferencia acelerada mediante CUDA.
- Agentes de programación.
- Análisis intensivo.
- Generación de contenido con modelos grandes.
- Procesamiento de documentos extensos.
- Ejecución de tareas de desarrollo y tests exigentes.
- Pruebas y experimentación con modelos.

### Comportamiento previsto

Cuando Linux esté activo, el nodo ofrecerá servicios y workers Linux.

Cuando Windows esté activo, se podrá instalar un servicio independiente de inferencia o worker compatible, siempre que no perjudique el uso personal del PC.

Cuando el equipo esté apagado, el controlador mantendrá pendientes los trabajos que requieran sus recursos.

### Posible Wake-on-LAN

Se estudiará encender el equipo desde la Raspberry para ejecutar trabajos de manera automática.

El arranque remoto deberá respetar la configuración dual boot y no cambiar de sistema operativo de forma inesperada.

**Decisión:** utilizarlo como principal nodo de IA, sin convertirlo en una dependencia permanente de la plataforma.

---

# 4. Arquitectura del sistema

## 4.1. Distribución lógica

### Capa 1 · Acceso y red

Elementos:

- Tailscale.
- Red local Ethernet.
- DNS interno.
- Clientes autorizados.
- API de entrada.
- Futuro panel de control.

Tailscale será la solución inicial de acceso privado remoto, sin exponer servicios innecesarios a Internet.

Se priorizará conexión Ethernet entre los nodos.

### Capa 2 · Plano de control

**Ubicación:** Raspberry Pi.

Componentes:

- API Gateway interno.
- Node Registry.
- Task Scheduler.
- Job Manager.
- Model Router.
- Agent Orchestrator.
- Estado persistente.
- Sistema de eventos.
- Monitorización básica.

Esta capa mantiene el inventario de recursos y decide cómo tratar las peticiones.

### Capa 3 · Plano de ejecución

**Ubicación:** ordenador secundario y ordenador principal; la Raspberry también podrá ejecutar trabajos ligeros.

Cada nodo ejecutará un worker que se registre ante el controlador.

Los workers podrán ofrecer capacidades diferenciadas:

- Python.
- Ejecución de herramientas.
- CPU.
- Inferencia LLM.
- Indexación.
- Procesamiento documental.
- Gestión de archivos.
- Tareas programadas.

### Capa 4 · Persistencia y almacenamiento

Distribución propuesta:

- Raspberry: estado y trabajos pendientes.
- Secundario: almacenamiento compartido y servicios de datos.
- Principal: modelos locales y datos temporales de inferencia.

La indisponibilidad del NAS no debe impedir que la Raspberry registre y conserve trabajos.

### Capa 5 · Aplicaciones y agentes

Esta capa contendrá agentes personales y aplicaciones que utilizarán el orquestador.

Se separará la lógica del agente de la infraestructura que ejecuta el modelo.

---

# 5. Arquitectura funcional del orquestador

## 5.1. Componentes principales

| Componente | Responsabilidad |
|---|---|
| API Server | Recibir solicitudes autenticadas |
| Node Registry | Registrar nodos y capacidades |
| Health Monitor | Comprobar disponibilidad |
| Task Scheduler | Seleccionar dónde ejecutar |
| Job Manager | Controlar estados y reintentos |
| Queue Manager | Conservar trabajos pendientes |
| Model Router | Seleccionar modelos y endpoints |
| Agent Runtime | Ejecutar agentes y herramientas |
| Worker Service | Ejecutar tareas en cada nodo |
| Event Log | Registrar decisiones y resultados |

## 5.2. Ciclo de un trabajo

1. Un cliente envía una solicitud.
2. La API autentica y valida la petición.
3. Se crea un identificador único de trabajo.
4. La tarea queda registrada de forma persistente.
5. El scheduler comprueba sus requisitos.
6. Se identifican los nodos disponibles.
7. Se reserva capacidad en el nodo seleccionado.
8. El worker recibe y ejecuta el trabajo.
9. Se registran progreso, resultados y errores.
10. El trabajo finaliza o se reprograma.

### Estados iniciales

- `pending`
- `queued`
- `assigned`
- `running`
- `succeeded`
- `failed`
- `retrying`
- `cancelled`

Los estados y sus transiciones se documentarán como contrato técnico antes de implementar los workers.

## 5.3. Política de asignación

La primera versión utilizará un scheduler determinista en Python.

Factores de decisión:

- Disponibilidad del nodo.
- Capacidad CPU.
- RAM disponible.
- VRAM disponible.
- Modelo requerido.
- Carga actual.
- Prioridad.
- Coste energético estimado.
- Localidad de los datos.
- Restricciones de permisos.
- Tiempo máximo admitido.

Se descartarán los nodos que no puedan satisfacer los requisitos mínimos.

La selección entre los candidatos restantes utilizará una puntuación configurable.

No se utilizará un LLM para tomar las decisiones básicas de infraestructura.

## 5.4. Modos operativos

### Modo normal

Raspberry, servidor secundario y PC principal disponibles.

La plataforma distribuye las tareas entre todos ellos.

### Modo reducido

PC principal apagado.

El sistema sigue funcionando con Raspberry y servidor secundario.

Las tareas que requieran GPU NVIDIA permanecen pendientes o utilizan una alternativa válida.

### Modo mínimo

Solo Raspberry disponible.

La plataforma mantiene:

- API básica.
- Registro de trabajos.
- Cola.
- Estado del sistema.
- Automatizaciones ligeras.
- Tareas que no dependan de los otros nodos.

### Recuperación

Cuando un nodo reaparece:

1. Se identifica.
2. Publica capacidades.
3. Se comprueba su estado.
4. Se habilita para nuevas tareas.
5. Se reevalúan los trabajos pendientes.

Los trabajos interrumpidos solo se reintentarán cuando su política lo permita. Las operaciones con efectos externos deberán disponer de protección contra duplicados.

---

# 6. Stack tecnológico

## 6.1. Tecnologías iniciales propuestas

| Categoría | Tecnología |
|---|---|
| Lenguaje principal | Python |
| API | FastAPI |
| Validación | Pydantic |
| Contenedores | Docker Compose |
| Base de datos inicial | SQLite |
| Coordinación | Scheduler Python propio |
| Workers | Servicios Python propios |
| Comunicación inicial | HTTP privado |
| Inferencia | Ollama |
| Inferencia avanzada | llama.cpp |
| VPN | Tailscale |
| Control de versiones | Git y GitHub |
| Sistema Raspberry | Linux 64-bit existente |
| Sistema secundario | Debian 13 estable sin escritorio, administrado por SSH |
| Sistema principal Linux | Ubuntu Desktop |
| Monitorización inicial | Logs estructurados y health checks |

SQLite es apropiado para la primera versión con un único controlador y almacenamiento local fiable.

No se utilizará SQLite como base de datos compartida simultáneamente a través de una carpeta de red.

## 6.2. Tecnologías previstas para evolución

| Tecnología | Uso futuro |
|---|---|
| NATS JetStream | Mensajería y trabajos persistentes |
| PostgreSQL | Persistencia más compleja |
| LiteLLM | Enrutamiento avanzado entre proveedores |
| LangGraph | Flujos de agentes con estado |
| OpenAI Agents SDK | Herramientas y coordinación de agentes Python |
| Open WebUI | Interfaz conversacional |
| OpenMediaVault | Administración del NAS |
| Uptime Kuma | Supervisión de disponibilidad |
| Prometheus + Grafana | Métricas y observabilidad |
| K3s | Orquestación de contenedores, si se justifica |
| WireGuard / Headscale | Alternativa futura de VPN |

Estas herramientas no están aprobadas para instalación inmediata. Su incorporación dependerá de necesidades concretas.

---

# 7. Estrategia de inteligencia artificial local

## 7.1. Objetivo

Reducir la dependencia económica de las APIs comerciales mediante modelos locales.

La arquitectura deberá permitir cambiar el modelo o el proveedor sin reescribir los agentes.

## 7.2. Reparto de inferencia

**Raspberry**

No será el nodo principal de inferencia. Se podrán evaluar modelos extremadamente ligeros, pero nunca a costa del servicio de control.

**PC secundario**

Se evaluarán modelos pequeños con CPU y, experimentalmente, aceleración Vulkan mediante RX 590.

Prioridad baja frente a sus funciones de servidor.

**PC principal**

Nodo preferido para inferencia LLM.

Modelos iniciales candidatos:

- Qwen3 4B.
- Qwen3 8B.
- Qwen2.5-Coder 7B.
- Qwen3 14B, condicionado a VRAM y memoria efectiva.

Los modelos definitivos se seleccionarán con pruebas de rendimiento y calidad.

## 7.3. Restricciones

No asumir que:

- Varios nodos pueden sumar su VRAM automáticamente.
- La ejecución de múltiples agentes es siempre más eficiente.
- Un modelo local pequeño reemplaza a los mejores modelos comerciales.
- El tamaño del archivo descargado equivale a la RAM o VRAM total consumida.

Será obligatorio medir contexto, memoria, latencia, generación de tokens y tasa de éxito.

## 7.4. Política económica

Primera etapa: **inferencia local como opción predeterminada**.

Las API comerciales quedan fuera del flujo normal inicial y podrán incorporarse posteriormente como fallback opcional, explícitamente autorizado y con límites de gasto.

---

# 8. Agentes y casos de uso previstos

## AGENT-01 · Obsidian

Funciones previstas:

- Buscar notas.
- Consultar información personal.
- Interpretar plantillas.
- Crear borradores estructurados.
- Revisar frontmatter.
- Generar enlaces entre notas.
- Detectar duplicados.
- Crear entradas a partir de audio o chat.

**Restricción:** la sincronización actual del vault mediante iCloud exige un mecanismo de escritura seguro. Se debe evitar que Linux modifique una copia no sincronizada del vault.

## AGENT-02 · Chino HSK1

Funciones:

- Crear lecciones.
- Generar vocabulario.
- Descomponer hanzi.
- Crear plantillas.
- Relacionar palabras, caracteres, sesiones y lecciones.
- Revisar progresos.
- Preparar ejercicios.

Deberá reutilizar el sistema de plantillas de Obsidian.

## AGENT-03 · AWS

Funciones:

- Consultar apuntes.
- Preparar sesiones de estudio.
- Generar preguntas de repaso.
- Revisar respuestas.
- Proponer laboratorios.
- Consultar progreso de certificación.

## AGENT-04 · Desarrollo

Funciones:

- Analizar repositorios.
- Generar código.
- Ejecutar tests.
- Detectar errores.
- Elaborar propuestas de cambios.
- Preparar documentación.
- Revisar diferencias Git.

Los cambios importantes deberán pasar por pruebas y aprobación antes de fusionarse o desplegarse.

## AGENT-05 · Infraestructura

Funciones:

- Consultar estado de servidores.
- Detectar servicios caídos.
- Examinar logs.
- Proponer acciones correctivas.
- Gestionar backups.
- Reiniciar servicios autorizados.
- Solicitar encendido remoto de nodos.

Las operaciones destructivas o críticas requerirán autorización.

## AGENT-06 · Gestión documental

Funciones futuras:

- Clasificar documentos.
- Extraer información.
- Indexar contenidos.
- Realizar búsquedas semánticas.
- Preparar resúmenes.
- Organizar información del NAS.

---

# 9. Servicios de homelab

## SERV-01 · VPN privada

**Solución inicial:** Tailscale.

Objetivo: comunicación privada entre servidores y dispositivos personales.

La Raspberry ya dispone de una instalación funcional.

Pendiente:

- Incorporar el secundario y verificar el cliente del principal bajo Linux. Windows ya accede a la Raspberry por Tailscale desde la LAN. Quedan pendientes la prueba desde otra red y la reconexión tras reinicio.
- Configurar nombres internos.
- Revisar políticas de acceso.
- Definir qué aplicaciones estarán disponibles remotamente.

## SERV-02 · NAS

**Ubicación propuesta:** PC secundario.

Funciones:

- Almacenamiento compartido.
- Datos de aplicaciones.
- Documentos.
- Repositorios y archivos.
- Backups de la Raspberry.
- Copias de datos del equipo principal.

Se evaluará OpenMediaVault cuando tengamos inventario completo de discos.

El NAS no sustituye a las copias de seguridad independientes.

## SERV-03 · Monitorización

Primera etapa:

- Estado de nodos.
- Servicios activos.
- Carga CPU.
- RAM disponible.
- GPU y VRAM cuando proceda.
- Almacenamiento.
- Trabajos en curso.
- Errores y alertas.

Posteriormente:

- Métricas históricas.
- Consumo energético.
- Rendimiento de modelos.
- Disponibilidad de servicios.
- Panel de observabilidad.

## SERV-04 · Panel de administración

Interfaz web privada que permitirá:

- Ver los tres nodos.
- Consultar su disponibilidad.
- Consultar modelos disponibles.
- Enviar trabajos.
- Examinar la cola.
- Supervisar agentes.
- Consultar resultados.
- Autorizar acciones.
- Revisar incidencias.
- Solicitar encendido de nodos compatibles.

## SERV-05 · Copias de seguridad

Se diseñarán copias de:

- Estado del controlador.
- Configuración.
- Base de datos.
- Contenedores y volúmenes relevantes.
- Archivos del NAS.
- Información personal.

Los backups deberán incluir restauraciones de prueba.

---

# 10. Decisiones estratégicas y tácticas

Los identificadores de la tabla pertenecen al briefing. Los [ADR técnicos del repositorio](adr/) mantienen su numeración propia. Se distingue entre decisiones establecidas, propuestas iniciales y cuestiones pendientes.

| ID | Decisión | Estado |
|---|---|---|
| ADR-001 | Mantener Raspberry como controlador 24/7 | Establecida |
| ADR-002 | Utilizar los tres equipos existentes | Establecida |
| ADR-003 | Desarrollar orquestador propio Python | Establecida |
| ADR-004 | Priorizar modelos locales | Establecida |
| ADR-005 | Utilizar Tailscale inicialmente | Establecida |
| ADR-006 | PC principal con dual boot | Establecida |
| ADR-007 | PC secundario con Linux completo | Establecida |
| ADR-008 | Principal como nodo GPU bajo demanda | Establecida |
| ADR-009 | Secundario como servidor/NAS | Propuesta |
| ADR-010 | Debian 13 estable sin escritorio para el secundario, administrado por SSH | Establecida |
| ADR-011 | Ubuntu Desktop para principal | Propuesta |
| ADR-012 | FastAPI + SQLite para V1 | Propuesta |
| ADR-013 | Docker Compose antes de K3s | Propuesta |
| ADR-014 | Ollama como motor de inferencia inicial | Propuesta |
| ADR-015 | Integrar NATS cuando sea necesario | Diferida |
| ADR-016 | Automatizar encendido mediante Wake-on-LAN | Pendiente de validar |
| ADR-017 | Elegir solución segura para escritura Obsidian | Pendiente |
| ADR-018 | Ampliar RAM y discos del secundario | Pendiente de mediciones |

### Decisiones sobre Orca

Se ha evaluado Orca como herramienta de coordinación de agentes de programación, pero no se ha seleccionado como runtime principal del homelab.

Podría utilizarse como herramienta auxiliar de desarrollo.

La coordinación central del proyecto se implementará mediante componentes propios y, cuando resulte útil, frameworks como LangGraph o Agents SDK.

### Decisiones sobre infraestructura

No introducir inicialmente:

- Kubernetes/K3s.
- Proxmox.
- Alta disponibilidad compleja.
- Clústeres distribuidos de inferencia de un mismo modelo.
- Servicios de almacenamiento sobredimensionados.
- Dependencia obligatoria de APIs comerciales.

El proyecto debe justificar cada incorporación mediante necesidad y resultados medibles.

---

# 11. Hoja de ruta

## FASE 0 · Inventario y diseño

**Objetivo:** documentar infraestructura y decisiones.

Trabajos:

- Confirmar VRAM de la 4060 Ti.
- Identificar modelo exacto del i5.
- Inventariar discos del secundario.
- Aclarar las desconexiones del SSD USB de la Raspberry. El SO y la microSD ya están identificados.
- Comprobar conexiones Ethernet.
- Evaluar consumo energético.
- Referencia del estado actual de la Raspberry: [roadmap operativo](00-roadmap.md).

**Entregable:** inventario técnico completo y arquitectura V1 aprobada.

## FASE 1 · Preparación de infraestructura

**Objetivo:** conectar los tres nodos.

Trabajos:

- Identificar el disco de destino por modelo y capacidad. Preparar el USB con Debian 13 netinst amd64, instalar y verificar el primer arranque y una sesión SSH desde el principal.
- Preparar dual boot del principal.
- Configurar Linux, SSH y drivers.
- Instalar Tailscale.
- Configurar Docker.
- Asignar nombres internos.
- Verificar comunicación.
- Evaluar Wake-on-LAN.

**Criterio de aceptación:** comunicación privada entre nodos y acceso desde dispositivos autorizados.

## FASE 2 · Orquestador V1

**Objetivo:** disponer de una plataforma mínima funcional.

Trabajos:

- FastAPI en Raspberry.
- Registro de nodos.
- Heartbeats.
- Persistencia de tareas.
- Scheduler.
- Worker Python.
- Gestión de errores.
- Reintentos.
- Logs.
- Pruebas de desconexión.

**Criterio de aceptación:** enviar un trabajo desde un cliente, almacenarlo en la Raspberry y ejecutarlo en el secundario o principal cuando estén disponibles, sin perderlo ante desconexiones controladas.

## FASE 3 · Inferencia local

**Objetivo:** ejecutar IA mediante el sistema distribuido.

Trabajos:

- Instalar Ollama en PC principal.
- Configurar aceleración NVIDIA.
- Probar modelos.
- Medir memoria y rendimiento.
- Integrar Model Router.
- Exponer inferencia mediante API privada.
- Preparar fallback para tareas no ejecutables.

**Criterio de aceptación:** solicitar una inferencia desde otro dispositivo y recibir el resultado a través del controlador, sin acceder directamente a la API del modelo.

## FASE 4 · Primeros agentes útiles

**Objetivo:** crear valor personal sobre la infraestructura.

Prioridad sugerida:

1. Agente de estado del sistema.
2. Agente Obsidian de consulta.
3. Agente HSK1 de generación estructurada.
4. Agente de programación.
5. Agente de documentos.

**Criterio de aceptación:** al menos un agente funcional, con herramientas autorizadas, logs y pruebas de calidad.

## FASE 5 · NAS y servicios

**Objetivo:** consolidar el servidor secundario.

Trabajos:

- Configurar almacenamiento.
- Elegir solución NAS.
- Compartir archivos.
- Configurar backups.
- Desplegar servicios auxiliares.
- Monitorizar discos y capacidad.

**Criterio de aceptación:** acceso remoto privado a archivos y restauración verificada de una copia de seguridad.

## FASE 6 · Automatización avanzada

**Objetivo:** reducir operaciones manuales.

Trabajos:

- Wake-on-LAN.
- Apagado inteligente.
- Política de ahorro energético.
- Planificación basada en recursos.
- Dependencias entre tareas.
- Control de concurrencia.
- Alertas.
- Recuperación automatizada segura.

**Criterio de aceptación:** recuperar un worker desconectado, asignarle trabajos y gestionar errores de forma predecible.

## FASE 7 · Escalabilidad

**Objetivo:** preparar ampliaciones futuras.

Posibles líneas:

- Nuevos nodos.
- Más almacenamiento.
- Colas distribuidas.
- Contenedores orquestados.
- Bases de datos más avanzadas.
- Mayor observabilidad.
- Agentes especializados adicionales.
- Arquitecturas híbridas con cloud.

Esta fase no implica instalar todas esas tecnologías, sino mantener una arquitectura que permita incorporarlas.

---

# 12. Riesgos y mitigaciones

| Riesgo | Mitigación prevista |
|---|---|
| Raspberry sobrecargada | Mantener únicamente servicios ligeros de control |
| Pérdida de microSD | SSD y backups |
| PC principal apagado | Cola persistente y ejecución diferida |
| Windows activo | Worker opcional y modo ocupado |
| RX 590 poco útil en inferencia | Priorizar CPU, NAS y servicios |
| Memoria insuficiente en secundario | Limitar servicios; ampliar solo tras medir |
| Pérdida de trabajos | Persistencia, confirmaciones y reintentos |
| Trabajos duplicados | Idempotencia y estado persistente |
| Corrupción del vault | Integración segura y backups |
| Agentes con permisos excesivos | Principio de mínimo privilegio y aprobaciones |
| Exposición de servicios | Red privada y autenticación |
| Consumo eléctrico elevado | Monitorización y encendido bajo demanda |
| Fallo de la Raspberry | Copias del estado y procedimiento de recuperación |
| Complejidad excesiva | Desarrollo incremental y decisiones documentadas |

---

# 13. Indicadores de éxito

Para evaluar el proyecto se seguirán indicadores objetivos:

### Infraestructura

- Disponibilidad del controlador.
- Tiempo de recuperación tras reinicio.
- Porcentaje de heartbeats recibidos.
- Consumo de RAM/CPU.
- Consumo eléctrico.

### Orquestación

- Trabajos completados.
- Trabajos fallidos.
- Trabajos pendientes.
- Reintentos.
- Tiempo hasta asignación.
- Tiempo hasta finalización.
- Ejecuciones duplicadas con efectos externos.

### Inteligencia artificial

- Latencia de inferencia.
- Tokens por segundo.
- Uso de VRAM.
- Calidad de respuestas.
- Éxito en tareas con herramientas.
- Coste de ejecución local.
- Necesidad de fallback.

### Operación

- Recuperaciones exitosas.
- Restauraciones verificadas.
- Intervenciones manuales.
- Incidencias de seguridad.
- Ahorro frente a llamadas API equivalentes, cuando exista una comparación válida.

Los objetivos numéricos se fijarán después de medir la primera versión.

---

# 14. Organización del proyecto y del dosier

El proyecto seguirá utilizando `pi-agents` como base, ampliando su alcance funcional.

Se propone conservar dentro del repositorio una carpeta de documentación estructurada.

## Estructura documental sugerida

**00 — Visión y planificación**

- Briefing maestro.
- Alcance.
- Objetivos.
- Roadmap.
- Backlog general.

**01 — Infraestructura**

- Inventario de hardware.
- Raspberry Pi.
- Servidor secundario.
- PC principal.
- Diagramas de red.
- VPN.
- Almacenamiento.

**02 — Arquitectura**

- Arquitectura general.
- Plano de control.
- Plano de ejecución.
- Scheduler.
- Workers.
- Persistencia.
- Contratos API.

**03 — Inteligencia artificial**

- Inventario de modelos.
- Benchmarks.
- Model Router.
- Herramientas.
- Agentes.
- Evaluaciones.

**04 — Servicios**

- NAS.
- Backups.
- Monitorización.
- Automatizaciones.
- Panel de control.

**05 — Operaciones**

- Instalación.
- Despliegues.
- Mantenimiento.
- Seguridad.
- Recuperación ante fallos.
- Runbooks.

**06 — Gestión**

- ADR (Architecture Decision Records).
- Riesgos.
- Incidencias.
- Hitos.
- Changelog.
- Resultados de pruebas.

Cada cambio relevante de arquitectura deberá dejar constancia de su motivo, alternativas consideradas y consecuencias.

---

# 15. Modelo de trabajo y mantenimiento

Se mantendrá la separación entre **diseño arquitectónico, implementación y validación**.

### Diseño

Definir decisiones técnicas, requisitos, restricciones y próximos hitos antes de desarrollar.

### Implementación

Utilizar Codex y agentes de desarrollo para modificar el repositorio, crear componentes, tests y documentación según especificaciones técnicas aprobadas.

### Validación

Comprobar que los cambios funcionan antes de considerarlos cerrados.

Cada hito deberá producir:

- Cambios identificables.
- Documentación actualizada.
- Tests pertinentes.
- Resultado de validación.
- Instrucciones de despliegue.
- Commit o conjunto de commits trazables.

No se considerará completado un hito únicamente porque el código haya sido generado.

---

# 16. Cuestiones abiertas

Antes de comenzar las instalaciones, hay que resolver:

1. ¿La RTX 4060 Ti tiene 8 o 16 GB de VRAM?
2. ¿Cuál es el modelo exacto del Intel i5?
3. ¿Qué discos tiene el PC secundario?
4. ¿El PC secundario permanecerá encendido 24/7?
5. ¿Es estable el SSD USB para el uso previsto? El sistema actual arranca desde microSD.
6. ¿Los tres dispositivos tienen acceso a Ethernet?
7. ¿Cuánto consume en reposo el PC secundario?
8. ¿Qué espacio se reservará para Linux en el equipo principal?
9. ¿Cuál será la estrategia definitiva de sincronización Obsidian?
10. ¿Qué presupuesto existe para discos, RAM, SSD o SAI?
11. ¿Qué servicios necesitan disponibilidad permanente?
12. ¿Qué tipo de solicitudes tendrán prioridad sobre otras?

Estas cuestiones se resolverán cuando afecten a la siguiente decisión técnica. No deben bloquear trabajos independientes.

---

# 17. Primer hito oficial

## HITO-001 · Infraestructura base operativa

**Objetivo:** conseguir que la Raspberry Pi y el PC secundario funcionen como los dos primeros nodos de un sistema distribuido.

### Alcance

- Inventario de ambos equipos.
- Instalación y configuración del secundario.
- Acceso SSH.
- Tailscale.
- Docker.
- Identificación y conectividad.
- Primer worker remoto.
- Primera ejecución enviada desde Raspberry.

### Fuera de alcance

- NAS definitivo.
- Modelos grandes.
- Multiagente avanzado.
- Kubernetes.
- Panel completo.
- Automatización de encendido.
- Alta disponibilidad.

### Resultado esperado

Desde la Raspberry se podrá solicitar al secundario que ejecute una tarea Python, recibir su resultado y registrar si finalizó correctamente.

Este será el punto de partida para el scheduler distribuido.

---

# 18. Visión final

La plataforma deberá permitir una interacción como la siguiente:

**Solicitud:** «Revisa mis apuntes de AWS, identifica qué debo repasar y prepara los ejercicios de mañana».

El sistema:

1. Recibe la solicitud desde cualquier dispositivo autorizado.
2. Identifica los agentes y herramientas necesarios.
3. Consulta los datos disponibles mediante la integración autorizada.
4. Selecciona los modelos de IA y los nodos adecuados.
5. Ejecuta las tareas.
6. Valida los resultados.
7. Guarda los cambios autorizados.
8. Devuelve la respuesta.
9. Conserva el registro de la ejecución.

Todo ello sin exigir que el usuario conozca qué servidor ha ejecutado cada operación.

**Meta final:** construir una plataforma personal distribuida, privada, modular y extensible donde los ordenadores domésticos se comporten como recursos de un mismo sistema, coordinados por un orquestador propio y capaces de ejecutar agentes de inteligencia artificial y servicios autogestionados.

## Registro de actualización · 8 de noviembre de 2026

| Estado | Resultado y procedencia |
|---|---|
| VERIFICADO | El chat «Preparar backup e instalar Linux ligero» registró la copia íntegra de la tarjeta anterior y la comprobación de su integridad. La restauración del controlador actual sigue pendiente. |
| VERIFICADO | Los chats «Análisis Sistemas Linux Raspberry Pi» y «Continuar proyecto Pi Agents» documentan DietPi y acceso SSH por clave mediante Tailscale desde la LAN. Véanse las [pruebas de conectividad](03-tailscale.md) y el [registro de cambios](../CHANGELOG.md). |
| EN PRUEBAS | La prueba desde otra red, la reconexión tras reinicio y el diagnóstico del SSD siguen abiertos. |
| PENDIENTE | «Instalar Linux Dual Boot» recoge el requisito de conservar Windows. La elección de distribución y el arranque de Linux en el principal quedan por verificar. |
| PENDIENTE | «Comparar Orca y alternativas» aporta el diseño de tres nodos. HITO-001 se cerrará cuando la Raspberry envíe una tarea al secundario y quede registrado su resultado. |
| PENDIENTE de instalación | En «Explorar sistema operativo del PC secundario» se eligió Debian con administración por SSH y se acordó instalarlo desde USB tras una prueba incompleta de SteamOS. La configuración elegida reserva la RAM para servicios y workers. Se valoraron Ubuntu Server LTS y OpenMediaVault. Quedan por confirmar el disco de destino, el arranque y el primer acceso por SSH. |
