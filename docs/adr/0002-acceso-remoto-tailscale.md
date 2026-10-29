# ADR-0002 — Acceso remoto mediante Tailscale

- Fecha: 2026-10-29
- Estado: **Propuesta; instalación pendiente**

## Contexto

Se requiere administración SSH desde redes distintas a la LAN sin exponer el puerto 22 públicamente. La red usa un router doméstico Movistar con reserva DHCP local.

## Decisión propuesta

Adoptar Tailscale como red privada entre Windows y Raspberry; mantener inicialmente el servidor OpenSSH y la autenticación por clave sobre la interfaz privada. MagicDNS es opcional y se utilizará solo tras verificar resolución. Mantener el alias SSH local durante la instalación y la prueba externa.

No activar Tailscale SSH, exit node ni subnet router en este hito: añaden capacidades que el caso de uso actual no necesita. La instalación se hará con `dietpi-software`, siguiendo el paquete optimizado de DietPi.

## Alternativas

- Abrir TCP/22 con port forwarding: desaconsejado para este caso por exposición innecesaria.
- WireGuard autogestionado: más control, pero implica configuración y operación de claves, endpoint y DNS.
- ZeroTier: otra alternativa válida de red superpuesta.

## Consecuencias previstas

Positivas: acceso entre redes, mantenimiento sencillo, no depender de IP pública doméstica.

Riesgos: dependencia de la cuenta/control plane de Tailscale; gestión de dispositivos, ACL/grants, expiración de claves y seguridad de las cuentas asociadas.

## Validación requerida

SSH desde una red distinta, sin abrir puertos, y prueba de reconexión tras reinicio, conservando SSH local. Ver [guía de Tailscale](../03-tailscale.md).
