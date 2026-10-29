# 02 — Red, DHCP y administración SSH

**Estado:** LAN/SSH funcionales; reserva DHCP registrada. Autenticación exclusivamente por clave pendiente de comprobar y reforzar.

## Contexto

- Cliente: Windows con OpenSSH desde PowerShell.
- Servidor: DietPi en Raspberry Pi 4, interfaz principal Wi-Fi `wlan0`.
- Router: Movistar RTF8115VW.
- Hostname: `pi-agents`.
- La IP local real, MAC y SSID se excluyen del repositorio público.

## Incidente de subredes durante el arranque

Inicialmente Windows y Raspberry estaban en **subredes distintas** (`192.168.1.0/24` vs. `192.168.68.0/24`). Intentar SSH a la Raspberry produjo `Connection timed out`. Tras conectar DietPi a la red doméstica correcta, se pudo acceder localmente.

Para diagnosticar:

```powershell
ipconfig
Test-NetConnection <IP_LOCAL> -Port 22
tracert -d <IP_LOCAL>
```

```bash
ip -br -4 addr
ip route
```

## Reserva DHCP en router Movistar

Se verificaron varias instancias DHCP en `Configuration > LAN Setting > LAN DHCP`:

- Índice 0: rango condicionado para `IAL` (no apto para cliente general).
- Índice 1: rango condicionado `TEF_IOT` (no apto para cliente general).
- Índice 2: deshabilitado.
- **Índice 3:** pool doméstico `192.168.1.33–192.168.1.199`, sin condición de Vendor ID.

Se añadió una entrada **habilitada** en `índice 3 > Static Lease` asociando la MAC de `wlan0` a la IP local asignada. Se observó posteriormente conectividad de la Raspberry en la IP reservada.

**Importante:** registrar una reserva no garantiza al 100 % su permanencia tras todos los reinicios o cambios de firmware. Revalidar después de actualizar el router y al cambiar interfaz de red.

## Administración sin root directo

Se creó el usuario `piadmin` y se comprobó:

```bash
sudo whoami
# root
```

El shell de `piadmin` es el recomendado para administración habitual; `sudo` para cambios privilegiados. El acceso directo de root deberá restringirse tras verificar acceso alternativo.

## SSH desde Windows

Se configuró y verificó el alias `pi-agents-local` del cliente OpenSSH. Ejemplo publicable de `%USERPROFILE%\.ssh\config`:

```sshconfig
Host pi-agents-local
    HostName <IP_LOCAL>
    User piadmin
    IdentityFile ~/.ssh/id_ed25519_pi_agents
    IdentitiesOnly yes
```

En el equipo real se reemplaza `<IP_LOCAL>` por la dirección asignada; **no publicar la configuración real**.

Comprobación del alias desde PowerShell:

```powershell
ssh -G pi-agents-local | Select-String '^hostname '
ssh pi-agents-local
```

### Reproducir la configuración de clave SSH en Windows

En PowerShell **local de Windows** (no dentro del shell Linux):

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.ssh"
ssh-keygen -t ed25519 -a 64 -f "$env:USERPROFILE\.ssh\id_ed25519_pi_agents" -C "windows-pi-agents"
```

Proteger la clave privada con una frase de paso. La clave pública termina en `.pub`; **nunca copiar la privada al servidor**.

Con una sesión SSH por contraseña todavía disponible, autorizar la clave pública:

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519_pi_agents.pub" | ssh piadmin@<IP_LOCAL> "umask 077; mkdir -p ~/.ssh; cat >> ~/.ssh/authorized_keys; chmod 700 ~/.ssh; chmod 600 ~/.ssh/authorized_keys"
```

Antes de endurecer el servidor, probar la clave explícitamente sin recurrir a la contraseña de usuario. Una frase de paso de la **clave privada local** puede seguir siendo solicitada:

```powershell
ssh -o PreferredAuthentications=publickey -o PasswordAuthentication=no -i "$env:USERPROFILE\.ssh\id_ed25519_pi_agents" piadmin@<IP_LOCAL>
```

> El comando de autorización agrega la clave a `authorized_keys` y, si se ejecuta repetidamente, puede añadir duplicados. Inspeccionar el archivo antes de repetirlo.

Para obligar a usar clave pública en una prueba (todavía pendiente de confirmación documentada):

```powershell
ssh -o PreferredAuthentications=publickey -o PasswordAuthentication=no pi-agents-local
```

Solo tras comprobar con **una segunda sesión independiente** que la autenticación por clave funciona, se puede desactivar login SSH por contraseña en DietPi, por ejemplo:

```bash
sudo /boot/dietpi/func/dietpi-set_software disable_ssh_password_logins 1
```

Mantener abierta una sesión funcional durante el cambio, probar desde otra nueva y verificar la ruta de recuperación antes de cerrar la anterior. El comando procede de https://dietpi.com/docs/software/ssh/.

## Script opcional de doble clic

Ver [`scripts/conectar-pi-agents.bat`](../scripts/conectar-pi-agents.bat) para abrir SSH desde Windows con `ssh pi-agents-local`.

## No confundir

- La reserva DHCP ofrece estabilidad **solo en LAN**.
- Tailscale aportará conectividad segura entre redes y una IP/nombre de tailnet.
- No es necesario publicar TCP/22 en Internet.
