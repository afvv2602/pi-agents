# ADR-0003 — Raspberry Pi OS Lite 64-bit como sistema base

- Fecha: 2026-11-10
- Estado: **Aplicada y verificada** en el controlador.
- Sustituye a [ADR-0001, elección de DietPi](0001-elegir-dietpi.md).

## Decisión y alcance

El chat principal confirmó la migración de la Raspberry Pi 4 a Raspberry Pi OS Lite 64-bit sobre Debian 13 Trixie. La Raspberry conserva su función de controlador disponible 24/7. El PC secundario sigue previsto para servicios y trabajos de CPU, y el principal para inferencia bajo demanda.

## Consecuencias

Las guías de instalación y mantenimiento pasan a utilizar Raspberry Pi Imager y APT. El arranque y la raíz EXT4 están verificados en el SSD por USB 2.0. Este enlace es provisional mientras se investiga el historial de errores en USB 3.0 y se observa la estabilidad prolongada.

Las pruebas de Tailscale realizadas con DietPi conservan valor histórico. La instalación y las pruebas de los servicios sobre la nueva base requieren evidencia propia. [Inventario y diagnósticos](../dosier-maestro.md).
