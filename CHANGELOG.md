# Changelog

El formato registra eventos **comprobados** separadamente de los planes.

## [Sin publicar] — 2026-10-29

### Comprobaciones observadas

- Captura aportada por el usuario antes de instalar Tailscale: sesión SSH como `piadmin`, hostname `pi-agents`, Debian 13 (Trixie) 13.7, ~55 GB libres, reloj sincronizado en `Europe/Madrid` y `sudo dpkg --audit` sin salida.
- Captura aportada tras instalar con `dietpi-software`: instalador finalizado, `tailscaled` activo y cliente Tailscale 1.104.4. Aún no se ha comprobado la adhesión a la tailnet.
- Estas pruebas no confirman aún el nivel de actualizaciones APT, el uso exclusivo de clave SSH ni el acceso remoto por Tailscale.

### Documentación

- Revisada la guía de Tailscale con fuentes oficiales de DietPi y Tailscale: comprobaciones previas, instalación, autenticación, pruebas por capas, red externa, reinicio y recuperación.
- Convertido el roadmap en hitos con criterios de aceptación y evidencia a registrar.
- Aclarado que los hitos de infraestructura de la versión 0.1.0 proceden del registro previo; esta revisión no ha comprobado la Raspberry.
- Actualizada ADR-0002 para delimitar SSH convencional sobre Tailscale y excluir funciones innecesarias en la primera fase.

### Estado

- La adhesión de Tailscale a la tailnet, las pruebas de conectividad y el endurecimiento SSH siguen pendientes.
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
