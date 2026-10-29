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

## INC-006 — SSD USB detectado pero sin montar (diagnóstico en curso)

**Fecha:** 2026-10-29. **Síntoma inicial:** el usuario comunicó que el SSD conectado por USB «no lo reconoce». **Estado tras la captura de diagnóstico:** el sistema sí detecta el dispositivo y su partición, pero esta no está montada. No se ha determinado aún si hay un problema adicional de estabilidad.

### Diagnóstico inicial, solo lectura

Ejecutar en la Raspberry con el SSD conectado:

```bash
lsblk -o NAME,TRAN,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
lsusb
sudo journalctl -k -b --no-pager -n 100
```

Antes de compartir las salidas, ocultar números de serie, UUID y otros identificadores privados. Comparar la presencia del SSD en `lsusb`, `lsblk` y los mensajes del kernel:

### Resultados observados en la captura

- `lsblk`: `/dev/sda` es un SSD USB de 111,8 GiB (Kingston); `/dev/sda1` ocupa el disco, tiene formato NTFS y no muestra punto de montaje. La raíz `/` sigue en la microSD (`mmcblk0p2`).
- `lsusb`: aparece un puente SATA-USB JMicron JMS567.
- El registro del kernel muestra detección de `sda` y `sda1`, así como eventos de desconexión y reconexión USB y un fallo de sincronización de caché tras una desconexión. No sabemos si esas desconexiones fueron manuales; por tanto, no se atribuye aún a cable, alimentación, carcasa o SSD.

**Conclusión parcial:** «no reconocido» describía la ausencia de acceso al volumen, no la ausencia de detección del hardware. El siguiente paso es aclarar si el disco contiene datos y si las desconexiones fueron intencionadas. Antes de usarlo para datos permanentes, comprobar estabilidad y alimentación. `vcgencmd get_throttled` es una comprobación de solo lectura que puede revelar episodios de subtensión de la Raspberry; un resultado normal no descarta por sí solo problemas de cable o alimentación del USB.

La [documentación oficial de DietPi](https://dietpi.com/docs/dietpi_tools/system_configuration/) indica que `dietpi-drive_manager` permite inspeccionar y montar un disco detectado. **No montar ni formatear todavía** hasta conocer el contenido del NTFS y aclarar los eventos de desconexión.

- Si aparece en `lsblk` pero sin punto de montaje, comprobar sistema de archivos y usar `dietpi-drive_manager` para inspeccionar y, si procede, montar. En DietPi la falta de montaje no equivale a falta de detección. **Este es el caso observado.**
- Si aparece en `lsusb` pero no en `lsblk`, revisar mensajes del kernel para errores de almacenamiento USB o de la carcasa/adaptador.
- Si no aparece ni en `lsusb`, revisar cable, puerto y alimentación. Son hipótesis, no causas confirmadas. La documentación oficial de Raspberry Pi indica que los puertos USB comparten un presupuesto de corriente y sugiere un hub alimentado para descartar problemas de alimentación.

**No ejecutar** `mkfs`, `fdisk` interactivo, `wipefs`, migración de `rootfs` ni opciones **Format** de DietPi Drive Manager hasta identificar el disco, conocer si contiene datos y decidir su uso. Registrar aquí la causa y la solución solo después de una prueba verificable.

Referencias: [DietPi Drive Manager](https://dietpi.com/docs/dietpi_tools/system_configuration/), [Raspberry Pi: USB y alimentación](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html), [Raspberry Pi: `vcgencmd get_throttled`](https://www.raspberrypi.com/documentation/computers/os.html).

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
