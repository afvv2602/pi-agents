# Roadmap y criterios de aceptación

Actualizado: 2026-10-29. **✅** confirmado por la documentación de la instalación previa; **🟡** pendiente de verificar; **⏳** no implementado. Las pruebas recientes proceden de capturas del usuario; Codex no ha ejecutado comandos en la Raspberry.

| Hito | Estado | Criterio de aceptación verificable | Evidencia a registrar |
|---|---|---|---|
| 0. DietPi y red local | ✅ | Arranque headless, SSH desde Windows, hostname y hora correctos | Comandos redactados de sistema y sesión |
| 1. Usuario y DHCP | ✅ | `piadmin` puede usar `sudo`; reserva asociada a `wlan0` | `sudo whoami`; prueba LAN tras nueva concesión |
| 2. Estado de paquetes | 🟡 | APT sin tareas interrumpidas y actualizaciones revisadas | Fecha, versiones y resultado de revisión |
| 3. SSH por clave | 🟡 | Nueva sesión con clave; contraseña de cuenta rechazada tras endurecimiento autorizado | Pruebas positivas y negativas, vía de recuperación |
| 4. Tailscale | 🟡 | SSH por IP Tailscale desde otra red; servicio recuperado tras reinicio; SSH local conservado; sin puerto WAN publicado | Instalación, adhesión y login SSH por clave sobre Tailscale en LAN comprobados. Faltan red externa, reinicio y demás pruebas de [aceptación](03-tailscale.md#criterios-de-aceptación) |
| 5. Copias y observabilidad | ⏳ | Backup fuera de microSD restaurado en prueba; espacio, logs y salud visibles | Registro de restauración y controles |
| 6. Docker Compose | ⏳ | Imagen ARM64 de prueba arranca, reinicia, registra logs y conserva datos | Archivo Compose, comandos y salida redactada |
| 7. API FastAPI | ⏳ | Healthcheck y endpoint autenticado; acceso limitado a la red autorizada | Pruebas de éxito y rechazo |
| 8. LangGraph | ⏳ | Workflow de prueba con herramientas acotadas y estado recuperable | Pruebas automatizadas y diagrama |
| 9. Obsidian | ⏳ | Lectura, dry-run, diff, aprobación y rollback sobre copia del vault | Pruebas sin datos privados |
| 10. Inferencia externa | ⏳ | Llamada a servicio remoto con timeouts y fallo controlado | Pruebas de error y coste documentado |

El 2026-10-29 se comprobaron el espacio libre, el reloj sincronizado y `sudo dpkg --audit` sin incidencias mediante captura del usuario. El hito 2 permanece 🟡 hasta revisar actualizaciones y versiones. Los hitos 2 y 3 se pueden verificar en paralelo con el hito 4, pero no se marcarán completados por el solo hecho de que Tailscale funcione. Ningún hito futuro implica despliegue automático del siguiente.

## Entregables de cada hito

Registrar objetivo, contexto, decisión y alternativas, instrucciones reproducibles, pruebas realmente ejecutadas, incidencias y soluciones, seguridad, cambios de arquitectura, entrada de CHANGELOG y siguiente paso. Sustituir en evidencias las IP, MAC, SSID, nombres de cuenta, tokens y contenido del vault.

## Próximo paso

Conectar Windows a una red distinta de la LAN y repetir `tailscale ping`, TCP/22 y SSH por clave hacia la dirección Tailscale. El usuario ejecuta los comandos y comparte resultados redactados; ver la [guía de Tailscale](03-tailscale.md).
