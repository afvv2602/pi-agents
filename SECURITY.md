# Security policy / Política de seguridad

Este es un proyecto personal de infraestructura y aprendizaje. Los detalles sensibles de la instalación real **no son parte del repositorio público**.

## Información que nunca debe añadirse

- Contraseñas, frases de paso, *tokens*, claves de API o archivos `authkey` de Tailscale.
- Claves SSH privadas; ni siquiera cifradas para este repositorio.
- Archivos `.env` reales o configuraciones privadas con secretos.
- SSID, credenciales de router, MAC real, inventarios completos de dispositivos.
- Contenido privado de Obsidian o capturas sin anonimizar.

## Controles previstos

- Usuario administrador no-root y uso limitado de `sudo`.
- Claves SSH verificadas; prohibir autenticación por contraseña solo después de prueba.
- Acceso remoto mediante tailnet privada sin publicar SSH en WAN.
- Permisos de mínimo privilegio para los agentes, revisión de diffs y backups antes de escrituras al vault.
- Política de actualización y recuperación documentada.

## Divulgación

No publicar incidencias con credenciales, IP pública ni datos de cuentas. Revocar y rotar cualquier secreto expuesto accidentalmente.
