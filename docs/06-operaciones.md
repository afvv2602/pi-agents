# 06 — Operación diaria y mantenimiento

**Estado:** guía operativa; los controles adicionales deben verificarse al desplegarse.

## Acceso local desde Windows

```powershell
ssh pi-agents-local
```

Alternativa de doble clic: [`scripts/conectar-pi-agents.bat`](../scripts/conectar-pi-agents.bat).

## Verificaciones rápidas en DietPi

```bash
hostname
uptime
free -h
df -h /
timedatectl status
ip -br addr
ip route
```

## Actualizaciones

```bash
sudo dietpi-update
sudo apt update
sudo apt upgrade
```

Antes de actualizaciones mayores: comprobar backups, espacio libre, notas de versión y mantener un método de recuperación local.

## Tailscale (tras instalarlo)

```bash
sudo systemctl status tailscaled
tailscale status
tailscale ip -4
journalctl -u tailscaled --no-pager -n 50
```

Los resultados Tailscale deben registrarse **solo después de instalar y probar** la integración.

## Seguridad

- Nunca hacer commits de `~/.ssh`, contraseñas, tokens, credenciales o archivos `.env` reales.
- `piadmin` para uso diario; `sudo` solo cuando sea necesario.
- No abrir SSH al Internet público; usar una tailnet privada.
- Comprobar autenticación por clave antes de desactivar contraseña SSH.
- Revisar periódicamente permisos de servicios, copias y caducidad de dispositivos.

## Copias de seguridad y recuperación (pendiente)

1. Definir destino de backup **fuera** de la microSD.
2. Documentar proceso de restauración y probarlo.
3. Mantener los secretos por separado y nunca guardarlos en Git.
4. Antes de conectar un vault real, probar lectura y escritura en una copia.

## Evidencias para portfolio

Al guardar capturas de terminal, ocultar la IP privada, MAC, nombres de red, URLs de autenticación, claves y cualquier metadato personal. Las capturas de paneles de router suelen revelar detalles innecesarios: preferir diagramas o valores sustituidos.
