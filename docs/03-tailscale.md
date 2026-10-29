# 03 — Acceso remoto con Tailscale

**Estado: Raspberry y Windows en la tailnet; pruebas de ruta, SSH y red externa pendientes.** Guía revisada el 2026-10-29 contra documentación oficial. El usuario ejecuta los comandos y comparte resultados; Codex documenta los resultados y prepara los siguientes pasos.

## Objetivo y decisiones

Acceder a `pi-agents` por SSH convencional desde Windows, incluso fuera de la LAN, sin redirigir TCP/22 en el router. Mantener `ssh pi-agents-local` operativo. No activar Tailscale SSH (`tailscale set --ssh`), exit node ni subnet router. Ver [ADR-0002](adr/0002-acceso-remoto-tailscale.md).

## 0. Antes de instalar (comprobado parcialmente el 2026-10-29)

Desde PowerShell, comprobar `ssh pi-agents-local` y conservar esa sesión abierta durante la instalación. En la Raspberry, revisar:

```bash
hostname
cat /etc/os-release
df -h /
timedatectl status
sudo dpkg --audit
```

Confirmar espacio libre, hora sincronizada y ausencia de paquetes a medio configurar. Si aparece un problema, resolverlo antes de seguir.

**Resultados observados en captura aportada por el usuario (2026-10-29):** sesión SSH como `piadmin` en `pi-agents`; `hostname` devuelve `pi-agents`; `/etc/os-release` indica Debian GNU/Linux 13 (Trixie), versión completa 13.7; la raíz tiene aproximadamente 55 GB libres (2 % de uso); `timedatectl status` muestra `Europe/Madrid` y `System clock synchronized: yes`; `sudo dpkg --audit` termina sin salida. `NTP service: inactive` también aparece, pero no contradice por sí solo el estado sincronizado. La captura **no** confirma la versión de DietPi, el nivel de actualizaciones APT ni que SSH use exclusivamente clave.

**Siguiente paso realizado:** el usuario instaló Tailscale mediante `sudo dietpi-software`, manteniendo disponible SSH local.

## 1. Instalar en DietPi (completado el 2026-10-29)

La [guía oficial de DietPi](https://dietpi.com/docs/software/vpn/) incluye Tailscale entre sus paquetes optimizados. Desde la sesión SSH local:

```bash
sudo dietpi-software
```

Seleccionar **Browse Software → Tailscale → Install** y confirmar el paquete elegido. Usamos la integración de DietPi en lugar del script genérico de [instalación Linux](https://tailscale.com/docs/install/linux).

```bash
systemctl is-active tailscaled
tailscale version
```

Si el servicio no está activo, revisar `sudo systemctl status tailscaled` y `sudo journalctl -u tailscaled --no-pager -n 50` antes de avanzar.

**Resultado observado en captura aportada por el usuario:** DietPi-Software indica `Install completed`; `systemctl is-active tailscaled` devuelve `active`; `tailscale version` informa 1.104.4. Esto verifica instalación y servicio activo en ese momento, pero no confirma aún que la Raspberry esté unida a la tailnet ni que el servicio sobreviva a un reinicio.

## 2. Unir la Raspberry a la tailnet (completado el 2026-10-29)

```bash
sudo tailscale up
tailscale status
tailscale ip -4
```

Abrir en el navegador la URL de autenticación que muestre `tailscale up`, usando la cuenta/tailnet prevista. Confirmar el dispositivo en **Machines** de la consola. Si se exige aprobación, completarla allí y repetir `tailscale status`. Guardar la IP Tailscale solo en configuración privada. No publicar URL de autenticación, claves ni capturas sin redactar.

**Resultado observado en capturas aportadas por el usuario:** `sudo tailscale up` devolvió `Success`; `tailscale status` enumera `pi-agents` y `tailscale ip -4` devolvió una dirección de la tailnet. La consola **Machines** muestra `pi-agents` como **Connected**, con versión 1.104.4. No se publica la dirección, identidad de cuenta ni URL de autenticación visibles en las capturas. En ese momento solo aparece un dispositivo; aún no se ha probado conexión entre equipos.

## 3. Windows y prueba de conectividad (cliente incorporado; pruebas pendientes)

Instalar el cliente según la [guía oficial para Windows](https://tailscale.com/docs/install/windows) e iniciar sesión en la misma tailnet. Comprobar ambos equipos en la aplicación y en **Machines**. Desde PowerShell:

**Resultado observado en captura aportada por el usuario (2026-10-29):** `tailscale status` ejecutado en Windows enumera el cliente Windows y `pi-agents` en la misma tailnet. La captura no prueba aún el tráfico entre ellos, la apertura de TCP/22 ni el login SSH. Se omiten IP e identidad de cuenta del repositorio.

```powershell
tailscale status
tailscale ping <TAILSCALE_IP>
Test-NetConnection <TAILSCALE_IP> -Port 22
ssh -o PreferredAuthentications=publickey -o PasswordAuthentication=no -i "$env:USERPROFILE\.ssh\id_ed25519_pi_agents" piadmin@<TAILSCALE_IP>
```

`tailscale ping` verifica la ruta privada; `Test-NetConnection` comprueba TCP/22; solo el último comando prueba el login SSH con clave. Una petición de frase de paso de la clave local es normal. Si falla SSH, revisar políticas de acceso de la tailnet, servidor, usuario y clave antes de atribuir el fallo a Tailscale.

Con SSH por IP funcionando, añadir un alias **privado** a `%USERPROFILE%\.ssh\config`:

```sshconfig
Host pi-agents-remote
    HostName <TAILSCALE_IP>
    User piadmin
    IdentityFile ~/.ssh/id_ed25519_pi_agents
    IdentitiesOnly yes
```

Probar `ssh pi-agents-remote` y verificar la clave de host SSH de la nueva dirección.

## 4. MagicDNS (opcional, pendiente)

Revisar en **DNS** de la consola si [MagicDNS](https://tailscale.com/docs/features/magicdns) está activado; en tailnets nuevas suele estarlo. Confirmar en **Machines** el nombre real del dispositivo y probar su nombre o FQDN. Mantener el alias por IP hasta validar resolución y SSH. No suponer que el hostname Linux y el nombre de tailnet coinciden.

## 5. Prueba externa y reinicio (pendientes)

1. Conectar Windows a otra red, por ejemplo un hotspot móvil, y desconectarlo de la LAN doméstica.
2. Repetir `tailscale ping <TAILSCALE_IP>`, `Test-NetConnection <TAILSCALE_IP> -Port 22` y SSH por clave. En la sesión ejecutar `hostname` y `whoami`; esperar `pi-agents` y `piadmin`. No usar la IP LAN.
3. Confirmar que el router no tiene redirección de TCP/22.
4. En una ventana autorizada, reiniciar la Raspberry. Repetir `systemctl is-active tailscaled`, `tailscale status`, SSH por Tailscale y `ssh pi-agents-local` desde LAN.
5. Registrar fecha, versiones, resultados y fallos aquí y en CHANGELOG, redactando valores privados.

## Criterios de aceptación

- [ ] `tailscaled` activo y ambos equipos visibles en la misma tailnet.
- [ ] `tailscale ping` y TCP/22 correctos desde Windows.
- [ ] SSH convencional por Tailscale con `piadmin` y clave pública, sin contraseña de cuenta.
- [ ] La conexión funciona desde una red externa.
- [ ] Tras reiniciar, Tailscale y el SSH local y remoto siguen disponibles.
- [ ] Sin port forwarding de TCP/22, exit node, subnet router ni Tailscale SSH.
- [ ] Versiones, pruebas, fallos y método de revocación documentados.

## Seguridad y recuperación

La tailnet limita conectividad según sus [políticas de acceso](https://tailscale.com/docs/reference/ssh-over-tailscale); OpenSSH sigue autenticando al usuario. Si se pierde un cliente, revocarlo desde **Machines** y revisar su clave SSH. La [caducidad de claves de dispositivo](https://tailscale.com/docs/features/access-control/key-expiry) puede interrumpir un servidor desatendido; evaluar su configuración y documentar la decisión, sin desactivarla por defecto.

Si falla el acceso remoto, volver a `ssh pi-agents-local` desde la LAN y revisar `tailscaled` y sus logs. No alterar el acceso SSH local durante este hito.

**Fuentes oficiales consultadas:** [DietPi VPN/Tailscale](https://dietpi.com/docs/software/vpn/), [DietPi Software](https://dietpi.com/docs/dietpi_tools/software_installation/), [Tailscale Linux](https://tailscale.com/docs/install/linux), [Tailscale Windows](https://tailscale.com/docs/install/windows), [SSH sobre Tailscale](https://tailscale.com/docs/reference/ssh-over-tailscale), [MagicDNS](https://tailscale.com/docs/features/magicdns), [CLI](https://tailscale.com/docs/reference/tailscale-cli).
