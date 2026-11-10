# Roadmap y criterios de aceptación

Estado comunicado el 10 de noviembre de 2026 para el controlador `pi-agents`. La migración está **IMPLEMENTADA**. El reinicio tras actualizar, el arranque desde el SSD, la hora sincronizada y el acceso SSH con clave ED25519 están **VERIFICADOS**. El [dosier maestro](dosier-maestro.md) recoge las fases del homelab completo.

| Fase del controlador | Estado | Evidencia necesaria para cerrarla |
|---|---|---|
| 1. Estabilidad del SSD en USB 2.0 | EN PRUEBAS | Registrar el periodo observado y la carga habitual. Tras varios arranques, verificar ambos montajes, revisar si hay desconexiones USB, reinicios del enlace o errores de E/S y EXT4, y anotar el resultado de `vcgencmd get_throttled`. Mantener separado el diagnóstico de USB 3.0. |
| 2. Tailscale sobre Raspberry Pi OS Lite | PENDIENTE | Comprobar paquete, servicio y adhesión a la tailnet. Validar ping, TCP/22 y SSH por clave en LAN y desde otra red. Repetir tras reiniciar y conservar SSH local sin publicar puertos. [Guía de pruebas](03-tailscale.md). |
| 3. Docker Engine y Docker Compose | PENDIENTE | Registrar versiones de Engine y del complemento Compose. Ejecutar un servicio ARM64 de prueba, revisar sus logs y comprobar que recupera sus datos tras recrear el contenedor. |
| 4. API y persistencia | PENDIENTE | Probar salud y autenticación de FastAPI en la red autorizada, incluido el rechazo de una petición sin autorización. Crear un registro de prueba en SQLite y recuperarlo tras reiniciar la aplicación. |
| 5. Registro de nodos y orquestación | PENDIENTE | Registrar un worker y sus capacidades, observar su heartbeat y comprobar que el scheduler propio conserva un trabajo con el nodo ausente. Al volver el nodo, ejecutar el trabajo y registrar resultado y estado en la Raspberry. |

En el último arranque, los registros filtrados estaban libres de errores de E/S y EXT4. Falta acordar y documentar el periodo de observación representativo para la fase 1. [Operación y seguimiento](06-operaciones.md).

## Controles y fases posteriores

- **Administración.** Revalidar la reserva DHCP y el estado de paquetes. La autenticación con ED25519 está confirmada. El rechazo de contraseñas por el servidor requiere una prueba independiente.
- **Copias y observabilidad.** Restaurar en prueba una copia externa al SSD del controlador y registrar espacio, logs y salud.
- **Obsidian.** Probar lectura, simulación, diff, aprobación y recuperación sobre una copia del vault.
- **Inferencia en el PC principal.** Documentar rendimiento, tiempos de espera y comportamiento cuando el nodo GPU esté apagado.

Registrar fecha, procedimiento, resultado y alcance de cada prueba. Compartir únicamente evidencias sin direcciones reales, MAC, SSID, claves, tokens ni contenido privado. Las pruebas de Tailscale en DietPi se conservan en el [historial](../CHANGELOG.md).
