# Changelog

El formato registra eventos **comprobados** separadamente de los planes.

## [Sin publicar] — 2026-10-29

### Comprobaciones observadas

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

- Revisada la guía de Tailscale con fuentes oficiales de DietPi y Tailscale: comprobaciones previas, instalación, autenticación, pruebas por capas, red externa, reinicio y recuperación.
- Convertido el roadmap en hitos con criterios de aceptación y evidencia a registrar.
- Aclarado que los hitos de infraestructura de la versión 0.1.0 proceden del registro previo; esta revisión no ha comprobado la Raspberry.
- Actualizada ADR-0002 para delimitar SSH convencional sobre Tailscale y excluir funciones innecesarias en la primera fase.

### Estado

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
