# 03 — Acceso remoto con Tailscale

**PENDIENTE en Raspberry Pi OS Lite.** Falta verificar el paquete, el servicio, la adhesión del controlador a la tailnet y el acceso desde Windows. Se mantiene como objetivo SSH convencional sobre la red privada con la cuenta `afvv2602`, sin publicar TCP/22. [Decisión de acceso remoto](adr/0002-acceso-remoto-tailscale.md).

## Evidencia histórica · DietPi en microSD

El 29 de octubre se documentaron Tailscale 1.104.4, `tailscaled` activo y ambos dispositivos en la misma tailnet. En la LAN hubo ping en ambos sentidos por ruta directa, TCP/22 accesible y login de `piadmin` con clave pública. Quedaron pendientes la prueba desde otra red y la reconexión después de un reinicio. Las capturas y su alcance se describen en el [historial de cambios](../CHANGELOG.md).

## Preparación e instalación para la fase pendiente

1. Desde la LAN, comprobar `ssh pi-agents` y conservar abierta esa sesión. En la Raspberry, revisar `cat /etc/os-release`, `dpkg --print-architecture`, `df -h /`, `timedatectl status` y `sudo dpkg --audit`.
2. Comprobar primero si existe el paquete con `dpkg-query -W tailscale` y si hay servicio con `systemctl is-active tailscaled`. Si falta el paquete, seguir los pasos de APT publicados para Debian Trixie, con su clave de firma y repositorio. Registrar la versión con `tailscale version` y comprobar el servicio. [Paquetes oficiales para Debian Trixie](https://pkgs.tailscale.com/stable/#debian-trixie).
3. Comprobar la adhesión con `tailscale status`. Si el nodo requiere autenticación, usar `sudo tailscale up` y completar el acceso a la tailnet prevista. Identificar el nodo nuevo en **Machines** y obtener su dirección con `tailscale ip -4`. Mantener la dirección, la identidad de cuenta y la URL de autenticación en privado.
4. Comprobar que el cliente de Windows está en la misma tailnet. Mantener el alias LAN `pi-agents` y definir un segundo bloque en el archivo de configuración de OpenSSH para distinguir las dos rutas. [Instalación para Windows](https://tailscale.com/docs/install/windows) · [Configuración del cliente SSH](02-red-y-ssh.md).

```sshconfig
Host pi-agents-remote
    HostName <TAILSCALE_IP>
    User afvv2602
    IdentityFile ~/.ssh/id_ed25519_pi_agents
    IdentitiesOnly yes
```

## Pruebas desde Windows

Sustituir el marcador por la dirección privada del nodo actual y utilizar esa misma dirección en `HostName`. Verificar la huella de host antes de aceptar una entrada nueva.

```powershell
$destinoPi = '<TAILSCALE_IP>'
tailscale status
tailscale ping $destinoPi
Test-NetConnection -ComputerName $destinoPi -Port 22
ssh -o PreferredAuthentications=publickey -o PasswordAuthentication=no pi-agents-remote whoami
ssh pi-agents-remote hostname
```

El ping comprueba la ruta, TCP/22 la disponibilidad del puerto y la sesión SSH la autenticación. Los resultados esperados de identidad son `afvv2602` y `pi-agents`. [SSH sobre Tailscale](https://tailscale.com/docs/reference/ssh-over-tailscale).

## Criterios de aceptación

- [ ] Registrar versión, `tailscaled` activo y los dos equipos visibles en la misma tailnet.
- [ ] En LAN, verificar ping en ambos sentidos y TCP/22 y login SSH por clave desde Windows hacia la dirección Tailscale.
- [ ] Desconectar Windows de la LAN doméstica y repetir ping, TCP/22 y SSH desde otra red.
- [ ] Tras un reinicio planificado de la Raspberry, comprobar el servicio, el acceso por la tailnet y el acceso por `ssh pi-agents` desde la LAN.
- [ ] Confirmar que no hay redirección WAN de TCP/22. Mantener el alcance acordado sin Tailscale SSH, exit node ni subnet router.
- [ ] Documentar fecha, versiones, resultados y procedimiento de revocación, omitiendo datos privados.

## Recuperación y nombres

Si falla la conexión privada, volver a la LAN con `ssh pi-agents`. Revisar `systemctl status tailscaled`, `sudo journalctl -u tailscaled --no-pager -n 50` y las políticas de la tailnet. Si se pierde un cliente, revocarlo en **Machines** y revisar su autorización SSH. Documentar la política de caducidad del nodo desatendido. [Caducidad de claves de dispositivo](https://tailscale.com/docs/features/access-control/key-expiry).

MagicDNS queda como opción posterior. Antes de cambiar el alias por IP, verificar el nombre real del dispositivo, su resolución y el login SSH. [MagicDNS](https://tailscale.com/docs/features/magicdns).
