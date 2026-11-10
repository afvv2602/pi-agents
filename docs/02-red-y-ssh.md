# 02 — Red local y SSH desde Windows

La Raspberry utiliza `wlan0` y responde al acceso SSH por clave ED25519 con el usuario administrador `afvv2602`. Su hostname es `pi-agents`. Windows está preparado para usar SSH Agent y el alias local `pi-agents`. En la LAN también se verificó el acceso por clave a la dirección Tailscale de la Raspberry. [Prueba desde Windows y validaciones pendientes](03-tailscale.md).

## Configurar el alias local

En Windows, editar `%USERPROFILE%\.ssh\config` (sin extensión). Sustituir `<IP_LOCAL>` por la dirección LAN comprobada y ajustar `IdentityFile` al nombre de la clave ED25519 que ya tiene autorizada la Raspberry. El nombre de archivo de este ejemplo es orientativo.

```sshconfig
Host pi-agents
    HostName <IP_LOCAL>
    User afvv2602
    IdentityFile ~/.ssh/id_ed25519_pi_agents
    IdentitiesOnly yes
```

Desde PowerShell se puede revisar la configuración efectiva sin abrir una conexión. Deben aparecer el destino LAN elegido, `user afvv2602` y la ruta de la identidad prevista.

```powershell
ssh -G pi-agents | Select-String '^(hostname|user|identityfile) '
```

## Cargar la clave en SSH Agent

Si hay que habilitar el agente de OpenSSH en Windows, ejecutar estos comandos una vez en PowerShell **como administrador**.

```powershell
Set-Service -Name ssh-agent -StartupType Automatic
Start-Service ssh-agent
Get-Service ssh-agent
```

Después, en PowerShell **con la cuenta habitual de Windows**, cargar la clave existente y comprobar que aparece una identidad ED25519. Usar la misma ruta que en `IdentityFile`. La frase de paso desbloquea la clave en el cliente. [Gestión de claves en OpenSSH para Windows](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement).

```powershell
ssh-add "$env:USERPROFILE\.ssh\id_ed25519_pi_agents"
ssh-add -l
```

Para una instalación nueva que necesite un par de claves, elegir un nombre de archivo libre, ejecutar `ssh-keygen -t ed25519` y proteger la privada con una frase de paso. Autorizar en la Raspberry el archivo público `.pub` durante la [preparación del sistema](01-instalacion-raspberry-pi-os.md). La clave privada permanece en Windows.

## Verificar el equipo y la sesión

Una reinstalación puede cambiar la clave de host. Si OpenSSH avisa de un cambio, contrastar la huella mostrada con la obtenida por una vía fiable, por ejemplo en la consola física con `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` si se negocia ED25519. Tras confirmar la identidad del equipo, actualizar únicamente la entrada antigua del destino en `known_hosts`.

```powershell
ssh pi-agents
```

Desde una segunda conexión de Windows se puede comprobar la autenticación por clave y la identidad del equipo.

```powershell
ssh -o PreferredAuthentications=publickey -o PasswordAuthentication=no pi-agents whoami
ssh pi-agents hostname
```

Las respuestas esperadas son `afvv2602` y `pi-agents`. La prueba acredita el método usado en esa conexión. El rechazo de contraseñas por el servidor sigue pendiente de verificación. Para un futuro endurecimiento, conservar una sesión funcional y comprobar el acceso desde una segunda sesión antes de cerrar la primera.

El [lanzador de doble clic](../scripts/conectar-pi-agents.bat) utiliza el mismo alias. Mantener la configuración real, las direcciones y las claves fuera del repositorio.

## Diagnóstico de red y antecedente DHCP

Si hay un timeout, consultar en privado la IP actual de `wlan0` y la ruta con `ip -br -4 addr` e `ip route`. Desde Windows, comparar con `ipconfig` y probar el puerto del destino, por ejemplo con `Test-NetConnection`. Para un alias que no se reconoce, revisar el nombre del archivo `config` y la salida de `ssh -G pi-agents`.

En la etapa DietPi se documentó una reserva habilitada para `wlan0` en el pool doméstico general del router Movistar (índice 3 de *LAN DHCP*, opción *Static Lease*). Los índices 0 y 1 tenían condiciones de fabricante y el 2 estaba deshabilitado. Falta revalidar la reserva en la nueva instalación. El usuario `piadmin` y el alias `pi-agents-local` identifican las pruebas históricas. [Incidencias anteriores](05-resolucion-problemas.md).
