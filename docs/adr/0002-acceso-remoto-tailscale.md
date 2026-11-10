# ADR-0002 — Acceso remoto mediante Tailscale

- Fecha: 2026-10-29
- Estado: **Elección de red privada vigente. Verificación pendiente en Raspberry Pi OS Lite**

## Contexto

Se requiere administración SSH desde redes distintas a la LAN sin exponer el puerto 22 públicamente. La reserva DHCP del router doméstico se documentó durante la etapa DietPi.

## Decisión

Adoptar Tailscale como red privada entre Windows y Raspberry y mantener inicialmente el servidor OpenSSH y la autenticación por clave sobre la interfaz privada. MagicDNS es opcional y se utilizará solo tras verificar resolución. Mantener el alias SSH local durante la instalación y la prueba externa.

El alcance se limita a OpenSSH convencional sobre la red privada, sin Tailscale SSH, exit node ni subnet router. El paquete para Debian 13 Trixie es la referencia para Raspberry Pi OS Lite. En DietPi se verificó SSH sobre Tailscale desde la LAN. En el nuevo sistema siguen pendientes instalación, adhesión y pruebas de acceso.

## Alternativas

- Abrir TCP/22 con port forwarding: desaconsejado para este caso por exposición innecesaria.
- WireGuard autogestionado: más control, pero implica configuración y operación de claves, endpoint y DNS.
- ZeroTier: otra alternativa válida de red superpuesta.

## Consecuencias previstas

Positivas: acceso entre redes, mantenimiento sencillo, no depender de IP pública doméstica.

Riesgos: dependencia de la cuenta/control plane de Tailscale; gestión de dispositivos, ACL/grants, expiración de claves y seguridad de las cuentas asociadas.

## Validación requerida

SSH desde una red distinta, sin abrir puertos, y prueba de reconexión tras reinicio, conservando SSH local. Ver [guía de Tailscale](../03-tailscale.md).
