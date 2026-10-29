# 01 — Instalación base de DietPi

**Estado:** completada la instalación inicial. Algunas verificaciones de actualización están pendientes.

## Hardware observado

- Raspberry Pi 4 Model B, 4 GB; arquitectura ARM64/aarch64.
- microSD con capacidad reconocida por el sistema de ~58 GiB.
- Administración remota desde Windows, sin necesidad de pantalla o teclado para operación normal.

## Sistema operativo

- DietPi v10.8.2 (observado en el banner).
- Debian GNU/Linux 13 `trixie` (observado en `/etc/os-release`).
- Hostname configurado: `pi-agents`.
- Zona horaria: `Europe/Madrid`.
- Hora del sistema sincronizada tras resolver un incidente de arranque.

## Instalación reproducible

1. Descargar la imagen DietPi ARM64 específica de Raspberry Pi desde https://dietpi.com/.
2. Flashear la microSD con una herramienta de imágenes compatible.
3. Conectar a red y alimentar la Raspberry.
4. Completar el primer inicio, cambio de contraseñas y ajustes iniciales.
5. Entrar por SSH y verificar hardware, sistema, red y hora.
6. Desde `dietpi-config` ajustar hostname y zona horaria.

> No guardar contraseñas iniciales ni credenciales definitivas en este repositorio.

## Comprobaciones

```bash
hostname
hostname -I
cat /etc/os-release
free -h
df -h /
timedatectl status
ip -br -4 addr
ip route
```

### Resultados confirmados (2026-10-29)

- `hostname` → `pi-agents`.
- `timedatectl status` → `Europe/Madrid`, `System clock synchronized: yes`.
- Conexión SSH comprobada desde Windows.
- Usuario `piadmin` con `sudo` confirmado.

`NTP service: inactive` fue observado con `System clock synchronized: yes`: no concluir que el reloj está mal por ese campo aislado. El arranque inicial sí encontró un error NTP; ver incidencias.

## Actualizaciones (verificación pendiente)

```bash
sudo dietpi-update
sudo apt update
sudo apt upgrade
```

No marcar como finalizadas hasta haber revisado la ejecución y los posibles reinicios. Para registrar las versiones reales:

```bash
cat /etc/os-release
uname -a
```

Referencias: https://dietpi.com/docs/install/ y https://dietpi.com/docs/getting_started/.
