# ADR-0001 — Elegir DietPi como sistema base

- Fecha: 2026-10-29
- Estado: **Sustituida el 2026-11-10 por [ADR-0003](0003-raspberry-pi-os-lite.md)**. Se conserva la decisión aplicada en la instalación anterior.

## Contexto

Se necesita un servidor Linux ARM64, sin escritorio, de bajo consumo, manejable desde Windows y apto para alojar procesos Python y servicios en contenedores sobre Raspberry Pi 4 de 4 GB.

## Decisión

Utilizar **DietPi** (basado en Debian) y mantener la operación *headless* por SSH.

## Alternativas

- Raspberry Pi OS Lite: mayor familiaridad y soporte directo del fabricante.
- Ubuntu Server: amplio ecosistema cloud, pero potencialmente más pesado.
- Alpine: mínimo consumo, a costa de ajustes adicionales en dependencias.

## Consecuencias

Positivas: configuración sencilla, footprint reducido, herramientas `dietpi-config`, `dietpi-software`, mantenimiento por APT.

Riesgos: posibles particularidades de DietPi al seguir tutoriales Debian genéricos. Mitigación: documentar pasos concretos y usar guías oficiales de DietPi.
