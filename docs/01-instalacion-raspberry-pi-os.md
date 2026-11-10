# 01 — Instalación de Raspberry Pi OS Lite en SSD

**IMPLEMENTADO.** La Raspberry Pi 4 de 4 GB utiliza Raspberry Pi OS Lite 64-bit, basado en Debian 13 Trixie. El usuario confirmó el reinicio tras la actualización. El dosier recoge la observación del sistema instalado. [Inventario de NODO-01](dosier-maestro.md).

## Preparación de una instalación equivalente

Estos pasos sirven para preparar otro medio o reconstruir el controlador cuando corresponda.

1. Identificar el disco de destino por modelo y capacidad. Grabar la imagen sustituye su contenido. Conservar una copia de los datos que deban recuperarse.
2. En Raspberry Pi Imager, seleccionar Raspberry Pi 4 y la edición **Raspberry Pi OS Lite (64-bit)** basada en Trixie. Seleccionar el SSD de destino.
3. Personalizar hostname `pi-agents`, usuario `afvv2602`, zona horaria `Europe/Madrid` y Wi-Fi. Habilitar SSH con la clave **pública** ED25519 del administrador. Introducir los datos de red solo en el equipo local.
4. Grabar y verificar la imagen. Con la Raspberry apagada, conectar el SSD por USB 2.0 y arrancar desde él. Esta es la conexión provisional del proyecto.
5. Comprobar el acceso local y los montajes. Antes de dar por válido el arranque desde SSD, identificar qué dispositivo respalda `/`. [SSH desde Windows](02-red-y-ssh.md).

Referencia del fabricante para la selección de imagen y la personalización del primer arranque. [Raspberry Pi Imager](https://www.raspberrypi.com/documentation/computers/getting-started.html).

## Comprobación del sistema instalado

```bash
cat /etc/os-release
dpkg --print-architecture
uname -r
hostname
whoami
ip -br link show wlan0
lsblk -o NAME,MODEL,SIZE,FSTYPE,MOUNTPOINTS
findmnt -no SOURCE,FSTYPE,TARGET --mountpoint /
findmnt -no SOURCE,FSTYPE,TARGET --mountpoint /boot/firmware
lsusb -t
df -h /
timedatectl status
vcgencmd get_throttled
```

En el sistema observado, el kernel era `6.18.50+rpt-rpi-v8` y el Kingston SV300S37A120G de unos 120 GB alojaba `/` en `/dev/sda2` (EXT4) y `/boot/firmware` en `/dev/sda1`. Quedaban unos 101 GB libres en la raíz. El adaptador utilizaba UAS a 480 Mb/s. NTP estaba sincronizado en `Europe/Madrid` y `vcgencmd get_throttled` devolvió `0x0`.

Los diagnósticos de arranque y el seguimiento de los errores previos en USB 3.0 se registran en [INC-006](05-resolucion-problemas.md). Para actualizar el sistema y repetir las observaciones durante uso normal, consultar la [guía de operaciones](06-operaciones.md).
