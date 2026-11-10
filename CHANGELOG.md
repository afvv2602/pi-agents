# Changelog

El formato registra eventos **comprobados** separadamente de los planes.

## [Sin publicar]

### 2026-11-10 · Controller v0.1

- Incorporados FastAPI, Dockerfile, Compose y pruebas de salud y persistencia. El traspaso confirmó la construcción ARM64, la respuesta local y por túnel SSH y la conservación de `db_initialized_at` tras recrear el contenedor. Se observó un `Connection reset by peer` transitorio en la primera consulta. [Evidencia y reproducción](docs/08-controller.md).

### 2026-11-10 · Fase 4 del controlador completada

- **VERIFICADO.** Docker ejecutó `hello-world` para ARM64. Docker Compose mostró `v5.7.0` y el servicio Docker estaba activo y habilitado. Su directorio de datos era `/var/lib/docker` en el SSD Kingston.
- El contenedor `probe` conservó `/data/marker` en un volumen con nombre tras `docker compose down` y `up -d`. Ambas lecturas mostraron `Tue Nov 10 01:24:11 UTC 2026`. [Prueba de la fase 4](docs/07-docker.md).
- La fase 3 ya había verificado `tailscaled` activo y habilitado y una sesión SSH desde Windows por la IP Tailscale de la Raspberry en la LAN. El banner de esa sesión mostró el kernel `6.18.60+rpt-rpi-v8`. Quedan pendientes el acceso desde otra red y la reconexión tras reiniciar. [Guía de Tailscale](docs/03-tailscale.md).
- **PENDIENTE.** Fase 5, primer controlador FastAPI con persistencia en SQLite. Continúan el seguimiento del SSD en USB 2.0 y el diagnóstico de USB 3.0. [Roadmap del controlador](docs/00-roadmap.md).

### 2026-11-10 · Migración a Raspberry Pi OS Lite 64-bit

- **IMPLEMENTADO y VERIFICADO.** El chat principal confirmó Raspberry Pi OS Lite sobre Debian 13 Trixie en la Raspberry Pi 4 ARM64 de 4 GB, con kernel `6.18.50+rpt-rpi-v8`. El sistema reinició tras actualizar. El SSD Kingston SV300S37A120G de unos 120 GB aloja la raíz EXT4 en `/dev/sda2` y la partición de arranque en `/dev/sda1`, montada en `/boot/firmware`.
- En el arranque observado quedaban unos 101 GB libres. NTP estaba sincronizado en `Europe/Madrid` y `vcgencmd get_throttled` devolvió `0x0`. El registro filtrado no mostró errores de E/S ni EXT4. Se comunicaron advertencias no críticas de MMC, audio, Bluetooth y Wi-Fi.
- El host `pi-agents` utiliza Wi-Fi por `wlan0` y admite acceso SSH con clave ED25519 como `afvv2602`. Windows está preparado para SSH Agent y el alias `pi-agents`.
- **EN PRUEBAS.** El SSD utiliza UAS por USB 2.0 a 480 Mb/s. Esta conexión es provisional por los errores de E/S anteriores en USB 3.0. Siguen abiertos el diagnóstico de USB 3.0 y la estabilidad prolongada del SSD. [INC-006](docs/05-resolucion-problemas.md).
- **PENDIENTE al documentar la migración.** Tailscale, Docker Engine y Compose, FastAPI, persistencia de la aplicación en SQLite, scheduler propio y registro y coordinación de nodos. [Roadmap](docs/00-roadmap.md).

### Comprobaciones históricas de DietPi

- 2026-11-09 · El usuario confirmó el arranque de DietPi desde el SSD por USB 2.0. Continúa el diagnóstico de USB 3.0 en [INC-006](docs/05-resolucion-problemas.md). Las pruebas SSH y Tailscale previas corresponden a la microSD.

- Captura aportada por el usuario antes de instalar Tailscale: sesión SSH como `piadmin`, hostname `pi-agents`, Debian 13 (Trixie) 13.7, ~55 GB libres, reloj sincronizado en `Europe/Madrid` y `sudo dpkg --audit` sin salida.
- Captura aportada tras instalar con `dietpi-software`: instalador finalizado, `tailscaled` activo y cliente Tailscale 1.104.4. En ese momento aún no se había comprobado la adhesión a la tailnet.
- Capturas posteriores: `sudo tailscale up` finalizó correctamente; `tailscale status` e `ip -4` devolvieron datos del nodo y la consola **Machines** muestra `pi-agents` conectado. IP, cuenta y URL de autenticación omitidas deliberadamente.
- Captura de PowerShell: `tailscale status` enumera el cliente Windows y `pi-agents` en la misma tailnet.
- Capturas de ambos equipos: `tailscale ping` responde en los dos sentidos mediante ruta directa por la LAN. Se omiten las direcciones concretas; en ese momento aún no se habían probado TCP/22, SSH ni acceso desde otra red.
- Captura de PowerShell: `Test-NetConnection <TAILSCALE_IP> -Port 22` devuelve `TcpTestSucceeded: True` mediante `InterfaceAlias: Tailscale`. El puerto responde en la red actual; en ese momento aún no se había probado el login SSH.
- Captura de PowerShell: login `piadmin@pi-agents` correcto por la IP Tailscale con autenticación limitada a clave pública; se solicitó la frase de paso de la clave privada local. El cliente reconoció la huella del host por una entrada previa en LAN. DietPi v10.8.2 y Raspberry Pi 4 ARM64 confirmados en el banner. La prueba sigue siendo dentro de la LAN.
- El banner advirtió temperatura de CPU de 62 °C; queda pendiente revisar tendencia y refrigeración, sin causa diagnosticada.
- Estas pruebas no confirman aún el nivel de actualizaciones APT ni el uso exclusivo de clave SSH.

### Documentación

- 2026-11-08 · Actualizada ADR-010 del [dosier maestro](docs/dosier-maestro.md) con la elección de Debian 13 sin escritorio y administración por SSH para el secundario. La instalación desde USB sigue pendiente.

- 2026-11-08 · Incorporado el [dosier maestro del homelab](docs/dosier-maestro.md), con inventario contrastado, arquitectura prevista de tres nodos y criterios de cierre del primer trabajo distribuido.

- 2026-10-30: añadido `AGENTS.md` con el alcance de mantenimiento documental, estados de evidencia, privacidad y flujo Git. Ajustado el resumen y diagrama del README para reflejar SSH por Tailscale verificado en LAN, manteniendo pendientes la prueba desde otra red y la reconexión tras reinicio.
- Revisada la guía de Tailscale con fuentes oficiales de DietPi y Tailscale: comprobaciones previas, instalación, autenticación, pruebas por capas, red externa, reinicio y recuperación.
- Convertido el roadmap en hitos con criterios de aceptación y evidencia a registrar.
- Aclarado que los hitos de infraestructura de la versión 0.1.0 proceden del registro previo; esta revisión no ha comprobado la Raspberry.
- Actualizada ADR-0002 para delimitar SSH convencional sobre Tailscale y excluir funciones innecesarias en la primera fase.

### Estado registrado en DietPi sobre microSD

- Raspberry y Windows aparecen en la tailnet; ping, TCP/22 y login SSH por clave funcionan sobre Tailscale estando en LAN. Faltan red externa, reconexión tras reinicio y endurecimiento SSH del servidor.
- El usuario comunicó que un SSD conectado por USB no se reconocía o no podía utilizarse; se abrió INC-006 con comprobaciones de solo lectura.
- Captura de diagnóstico de INC-006: el SSD USB de 111,8 GiB y su partición NTFS aparecen en `lsblk`; el puente SATA-USB aparece en `lsusb`. La partición no está montada. El kernel registra desconexión/reconexión y un fallo de sincronización de caché tras una desconexión; no se conoce si los eventos fueron manuales. No se han modificado ni formateado datos.
- Codex no ejecutó operaciones sobre la Raspberry; la instalación la realizó el usuario.

## [0.1.0] — 2026-10-29

### Confirmado

- DietPi v10.8.2 (Debian 13/Trixie ARM64) funcionando en Raspberry Pi 4 de 4 GB.
- SSH local desde Windows y hostname `pi-agents`.
- Zona horaria `Europe/Madrid` y reloj sincronizado.
- Reserva DHCP para Wi-Fi creada en el pool general de router Movistar RTF8115VW.
- Cuenta `piadmin` con privilegios `sudo` verificados.
- Alias SSH `pi-agents-local` operativo.
- Incidencias iniciales de NTP, subredes distintas y alias SSH documentadas.

### Sin confirmar todavía

- Endurecimiento de SSH basado exclusivamente en claves.
- Revisión completa del nivel de actualización de paquetes.

### Próximos hitos

- Incorporar Tailscale y probar acceso desde otra red.
- Preparar Docker Compose y servicios de orquestación.
