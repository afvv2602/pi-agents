# Roadmap y criterios de aceptación

Las fases numeradas aquí siguen la secuencia del chat «Investiga distribuciones Raspberry Pi». El [dosier maestro](dosier-maestro.md) mantiene por separado las fases del homelab de tres nodos.

| Fase del controlador | Estado | Evidencia y criterio de cierre |
|---|---|---|
| 1. Instalación de Raspberry Pi OS Lite | VERIFICADO | Raspberry Pi OS Lite 64-bit arranca desde el SSD Kingston con la raíz EXT4 en `/dev/sda2`. |
| 2. Diagnóstico y actualización inicial | VERIFICADO | Reinicio tras actualizar, montajes, sincronización NTP y acceso SSH con ED25519 comprobados. La observación prolongada del SSD continúa. |
| 3. Tailscale y acceso privado | VERIFICADO en LAN | `tailscaled` activo y habilitado. Windows abrió SSH por clave hacia la dirección Tailscale de la Raspberry. Pruebas desde otra red y tras reiniciar pendientes. [Evidencia y controles](03-tailscale.md). |
| 4. Docker Engine y Docker Compose | VERIFICADO | `hello-world` ejecutado en ARM64, Compose `v5.7.0` y servicio Docker activo y habilitado. El volumen conservó el marcador al recrear el contenedor. [Prueba y resultados](07-docker.md). |
| 5. FastAPI y persistencia en SQLite | PENDIENTE | Obtener `GET /health` y verificar que el valor inicial guardado en SQLite sobrevive a la recreación del controlador. Validar acceso privado y rechazo de peticiones no autorizadas según el diseño. |
| 6. Registro de nodos y orquestación | PENDIENTE | Registrar un worker y sus capacidades, observar su heartbeat y comprobar que el scheduler propio conserva un trabajo con el nodo ausente. Al volver el nodo, ejecutar el trabajo y registrar resultado y estado en la Raspberry. |

**Estabilidad del SSD en USB 2.0 · EN PRUEBAS.** Falta fijar la duración y la carga del periodo de observación. Registrar montajes, desconexiones USB, errores de E/S o EXT4 y `vcgencmd get_throttled` durante uso habitual y tras varios arranques. La causa de los fallos históricos en USB 3.0 sigue abierta. [Operación y seguimiento](06-operaciones.md).

## Controles y fases posteriores

- **Administración.** Revalidar la reserva DHCP y el estado de paquetes. La autenticación con ED25519 está confirmada. El rechazo de contraseñas por el servidor requiere una prueba independiente.
- **Copias y observabilidad.** Restaurar en prueba una copia externa al SSD del controlador y registrar espacio, logs y salud.
- **Obsidian.** Probar lectura, simulación, diff, aprobación y recuperación sobre una copia del vault.
- **Inferencia en el PC principal.** Documentar rendimiento, tiempos de espera y comportamiento cuando el nodo GPU esté apagado.

Registrar fecha, procedimiento, resultado y alcance de cada prueba. Compartir únicamente evidencias sin direcciones reales, MAC, SSID, claves, tokens ni contenido privado. Las pruebas de Tailscale en DietPi se conservan en el [historial](../CHANGELOG.md).
