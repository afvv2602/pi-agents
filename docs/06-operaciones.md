# 06 — Operación diaria y mantenimiento

**Estado:** guía operativa; los controles adicionales deben verificarse al desplegarse.

## Acceso local desde Windows

```powershell
ssh pi-agents
```

Alternativa de doble clic: [`scripts/conectar-pi-agents.bat`](../scripts/conectar-pi-agents.bat).

La conexión usa OpenSSH con el usuario `afvv2602` y la identidad ED25519 preparada en Windows. [Configuración del alias y del agente](02-red-y-ssh.md).

## Verificaciones rápidas en Raspberry Pi OS Lite

```bash
hostname
uptime
free -h
df -h /
timedatectl status
ip -br addr
ip route
```

### Seguimiento del SSD

Para cada periodo de observación, anotar fecha, tiempo de actividad, carga habitual y si hubo reinicio. Comprobar dónde están montados la raíz y el arranque, la velocidad y el controlador USB, y revisar los mensajes del kernel del arranque en curso.

```bash
findmnt -no SOURCE,FSTYPE,TARGET --mountpoint /
findmnt -no SOURCE,FSTYPE,TARGET --mountpoint /boot/firmware
lsusb -t
vcgencmd get_throttled
sudo journalctl -k -b --no-pager | grep -Ei 'I/O error|Buffer I/O|EXT4-fs.*(error|warning)|USB disconnect|reset .*USB device|uas.*(abort|reset)'
```

Registrar los errores con su contexto o indicar que el filtro no encontró coincidencias. Repetir durante el uso habitual y después de otros arranques. En la observación inicial, `/dev/sda2` alojaba la raíz EXT4 y `/dev/sda1` estaba montada en `/boot/firmware`. El adaptador usaba UAS por USB 2.0 a 480 Mb/s. La duración y carga representativas para validar la estabilidad siguen por acordar. [Incidencia del SSD](05-resolucion-problemas.md).

**Antecedente térmico (2026-10-29).** El banner de DietPi mostró una advertencia de temperatura de CPU a 62 °C durante una sesión SSH. Para valorar su relevancia en la nueva instalación, queda por medir la temperatura en reposo y bajo carga.

## Actualizaciones

```bash
sudo apt update
apt list --upgradable
sudo apt full-upgrade
```

Revisar los cambios que propone APT antes de confirmarlos. Antes de actualizaciones mayores, comprobar copias, espacio libre y vía de recuperación local. Tras un reinicio, verificar los montajes, SSH y el registro del arranque. [Mantenimiento de Raspberry Pi OS](https://www.raspberrypi.com/documentation/computers/os.html).

## Tailscale en Raspberry Pi OS Lite

```bash
sudo systemctl status tailscaled
tailscale status
tailscale ip -4
journalctl -u tailscaled --no-pager -n 50
```

El servicio estaba activo y habilitado en la prueba de SSH desde Windows en la LAN. Para contrastar la recuperación tras reiniciar o el acceso desde otra red, seguir la [guía de Tailscale](03-tailscale.md).

## Docker en el SSD

La fase 4 verificó la ejecución ARM64 y la persistencia de un volumen al recrear el contenedor. Para repetir las lecturas de servicio, ocupación y logs, consultar la [prueba de Docker y Compose](07-docker.md).

## Seguridad

- Nunca hacer commits de `~/.ssh`, contraseñas, tokens, credenciales o archivos `.env` reales.
- Utilizar la cuenta administradora `afvv2602`. Reservar `sudo` para operaciones que requieran privilegios.
- No abrir SSH al Internet público; usar una tailnet privada.
- Comprobar autenticación por clave antes de desactivar contraseña SSH.
- Revisar periódicamente permisos de servicios, copias y caducidad de dispositivos.

## Copias de seguridad y recuperación (pendiente)

El SSD es el disco del sistema. La copia histórica de la microSD y su comprobación de integridad están documentadas en el [dosier](dosier-maestro.md). La restauración del controlador actual sigue pendiente.

1. Definir destino de backup independiente del SSD del sistema.
2. Documentar proceso de restauración y probarlo.
3. Mantener los secretos por separado y nunca guardarlos en Git.
4. Antes de conectar un vault real, probar lectura y escritura en una copia.

## Evidencias para portfolio

Al guardar capturas de terminal, ocultar la IP privada, MAC, nombres de red, URLs de autenticación, claves y cualquier metadato personal. Las capturas de paneles de router suelen revelar detalles innecesarios: preferir diagramas o valores sustituidos.
