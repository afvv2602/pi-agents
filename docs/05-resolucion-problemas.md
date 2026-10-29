# 05 — Incidentes y resolución de problemas

Registro de incidencias observadas durante el montaje (2026-10-29). Las causas no verificadas se etiquetan como **hipótesis**.

## INC-001 — Fallo inicial de sincronización de hora

**Síntoma:** DietPi solicitaba reintentar *network time sync*, cambiar mirror NTP u omitir error.\
**Impacto:** el proceso de configuración inicial no avanzaba normalmente.\
**Observación posterior:** el sistema terminó arrancando y `timedatectl` confirmó `System clock synchronized: yes`.

**Causa raíz:** no determinada con certeza. Hipótesis: conectividad de red, DNS o alcance del servidor NTP durante el primer inicio. No afirmar que un servidor concreto fue la solución sin evidencia.

Diagnóstico:

```bash
ip route
ping -c 3 1.1.1.1
getent hosts pool.ntp.org
timedatectl status
```

## INC-002 — SSH: `Connection timed out`

**Síntoma:** Windows no alcanzaba la IP inicial de la Raspberry.\
**Diagnóstico:** los equipos estaban en distintas subredes IPv4.\
**Resolución:** conectar la Raspberry a la red doméstica utilizada por el cliente Windows y verificar una IP del mismo segmento.

```powershell
ipconfig
Test-NetConnection <IP_LOCAL> -Port 22
```

**Lección:** que el servidor arranque no implica que exista una ruta de red desde el cliente.

## INC-003 — Alias SSH no encontrado

**Síntoma:** `ssh pi-agents-local` devolvía `Could not resolve hostname`.\
**Probable causa:** el archivo `%USERPROFILE%\.ssh\config` no era reconocido, posiblemente por extensión `.txt` o contenido inválido.\
**Comprobación:** el alias se corrigió y posteriormente funcionó, pero no se confirmó cuál era el error exacto.

```powershell
Get-ChildItem "$env:USERPROFILE\.ssh" -Force
ssh -G pi-agents-local | Select-String '^hostname '
```

La ruta debe llamarse `config` sin extensión, con un bloque `Host` válido.

## INC-004 — Reserva DHCP en pool incorrecto (riesgo evitado)

**Observación:** el router dispone de varias instancias DHCP; algunas condicionadas por Vendor ID y una desactivada.\
**Acción segura:** solo crear *Static Lease* en el pool general, después de revisar rango, máscara, gateway y condiciones.

**Lección:** no pulsar `Add/Del` en la lista de servidores DHCP pensando que son reservas individuales.

## INC-005 — `NTP service: inactive` con reloj sincronizado

**Observación:** `System clock synchronized: yes` junto a `NTP service: inactive`.\
**Interpretación:** no demuestra por sí solo que la hora no se sincronice; DietPi puede utilizar mecanismos de sincronización diferentes a `systemd-timesyncd`.

## INC-006 — SSD conectado por USB no visible para el usuario (pendiente)

**Fecha:** 2026-10-29. **Estado:** comunicado por el usuario; aún no hay salida de diagnóstico ni causa confirmada. El SSD está conectado físicamente por USB a la Raspberry Pi 4, pero el usuario indica que «no lo reconoce». Todavía no sabemos si no aparece en el bus USB, si el kernel no crea un dispositivo de bloque o si únicamente falta montarlo.

### Diagnóstico inicial, solo lectura

Ejecutar en la Raspberry con el SSD conectado:

```bash
lsblk -o NAME,TRAN,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
lsusb
sudo journalctl -k -b --no-pager -n 100
```

Antes de compartir las salidas, ocultar números de serie, UUID y otros identificadores privados. Comparar la presencia del SSD en `lsusb`, `lsblk` y los mensajes del kernel:

- Si aparece en `lsblk` pero sin punto de montaje, comprobar sistema de archivos y usar `dietpi-drive_manager` para inspeccionar y, si procede, montar. En DietPi la falta de montaje no equivale a falta de detección.
- Si aparece en `lsusb` pero no en `lsblk`, revisar mensajes del kernel para errores de almacenamiento USB o de la carcasa/adaptador.
- Si no aparece ni en `lsusb`, revisar cable, puerto y alimentación. Son hipótesis, no causas confirmadas. La documentación oficial de Raspberry Pi indica que los puertos USB comparten un presupuesto de corriente y sugiere un hub alimentado para descartar problemas de alimentación.

**No ejecutar** `mkfs`, `fdisk` interactivo, `wipefs`, migración de `rootfs` ni opciones **Format** de DietPi Drive Manager hasta identificar el disco, conocer si contiene datos y decidir su uso. Registrar aquí la causa y la solución solo después de una prueba verificable.

Referencias: [DietPi Drive Manager](https://dietpi.com/docs/dietpi_tools/system_configuration/), [Raspberry Pi: USB y alimentación](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html).

## Plantilla para nuevos incidentes

```text
ID y fecha:
Síntoma:
Contexto y versión:
Comandos reproducibles:
Hipótesis:
Diagnóstico confirmado:
Cambio aplicado:
Prueba de regresión:
```
