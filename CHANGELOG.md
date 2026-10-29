# Changelog

El formato registra eventos **comprobados** separadamente de los planes.

## [Sin publicar] — 2026-10-29

### Documentación

- Revisada la guía de Tailscale con fuentes oficiales de DietPi y Tailscale: comprobaciones previas, instalación, autenticación, pruebas por capas, red externa, reinicio y recuperación.
- Convertido el roadmap en hitos con criterios de aceptación y evidencia a registrar.
- Aclarado que los hitos de infraestructura de la versión 0.1.0 proceden del registro previo; esta revisión no ha comprobado la Raspberry.
- Actualizada ADR-0002 para delimitar SSH convencional sobre Tailscale y excluir funciones innecesarias en la primera fase.

### Estado

- Tailscale, las pruebas externas y el endurecimiento SSH siguen pendientes.
- No se ejecutaron operaciones sobre la Raspberry.

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
