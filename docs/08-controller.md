# Controller v0.1 · FastAPI y SQLite

**MVP verificado el 10 de noviembre de 2026** en Raspberry Pi OS Lite ARM64. El despliegue comunicado se construyó en `~/pi-agents-controller/`. FastAPI expone `GET /health` y guarda la fecha de inicialización en la tabla `metadata` de `/data/controller.sqlite3`.

## Reproducir desde GitHub

En un equipo con Git, Docker Engine y el complemento Compose, desde una carpeta de trabajo:

```bash
git clone --branch docs/fase-4-docker https://github.com/afvv2602/pi-agents.git
cd pi-agents
docker compose -f infra/compose.yaml config
docker compose -f infra/compose.yaml up -d --build
docker compose -f infra/compose.yaml ps
docker compose -f infra/compose.yaml logs --tail=50 controller
curl -fsS http://127.0.0.1:8000/health
```

Usar `sudo docker` si la cuenta lo requiere. Esperar a que `ps` indique `healthy` antes de consultar la API. Para inspeccionar las últimas comprobaciones de salud desde Bash:

```bash
docker inspect --format '{{json .State.Health}}' "$(docker compose -f infra/compose.yaml ps -q controller)"
```

## Recreación y parada

Guardar el valor de `db_initialized_at`. Desde la raíz del repositorio, recrear el servicio conservando su volumen y comparar la nueva respuesta una vez que el servicio esté listo.

```bash
docker compose -f infra/compose.yaml down
docker compose -f infra/compose.yaml up -d
docker compose -f infra/compose.yaml ps
curl -fsS http://127.0.0.1:8000/health
```

Para detener la aplicación basta `docker compose -f infra/compose.yaml stop`. El volumen con nombre `controller_data` se conserva con `down`. Añadir `-v` lo eliminaría.

## Evidencia de la Raspberry

Se construyó la imagen `pi-agents-controller:0.1.0` y se crearon red, volumen y contenedor. Antes y después de la recreación, `GET /health` devolvió los mismos valores:

```json
{
  "status": "ok",
  "service": "pi-agents-controller",
  "version": "0.1.0",
  "db_initialized_at": "2026-11-10T01:31:36.328678+00:00"
}
```

La primera petición inmediatamente posterior al arranque devolvió `Connection reset by peer`. La siguiente respondió correctamente. La causa y la frecuencia siguen sin determinar. Un volumen que sobrevive a la recreación sigue necesitando una copia externa y una prueba de restauración.

## Acceso desde Windows

Con ambos equipos en la red doméstica se abrió este túnel en PowerShell:

```powershell
ssh -N -L 18000:127.0.0.1:8000 pi-agents-remote
```

Desde otra terminal, `Invoke-RestMethod http://127.0.0.1:18000/health` devolvió la misma fecha de SQLite. El puerto 8000 del host solo escucha en loopback. El acceso remoto usa la clave SSH sobre Tailscale. `/health` carece de autenticación de aplicación. Siguen pendientes la red externa y la reconexión tras reiniciar la Raspberry. [Guía de Tailscale](03-tailscale.md).

## Diferencias del repositorio y pruebas locales

El código Python conserva el contrato desplegado. El [Dockerfile](../services/gateway-api/Dockerfile) usa Python 3.13 slim y el [Compose](../infra/compose.yaml) construye desde `../services/gateway-api`. El nombre de proyecto explícito `pi-agents-controller` conserva el nombre de volumen por defecto del despliegue original al mover Compose a `infra/`. Si el despliegue se inició con otro nombre de proyecto, se debe identificar ese nombre antes de reutilizar su volumen.

En la Raspberry se instalaron `fastapi>=0.115,<1` y `uvicorn>=0.30,<1`. El traspaso no incluye las versiones exactas resueltas allí. Para esta reproducción se fijan FastAPI 0.162.2, Uvicorn 0.54.0 y sus dependencias en [requirements.txt](../services/gateway-api/requirements.txt). Esta selección y la nueva disposición de archivos quedan pendientes de validación con Docker en ARM64. La imagen se ejecuta como `10001:10001` con raíz de solo lectura, `/tmp` temporal, `no-new-privileges`, healthcheck y política `unless-stopped`.

En un entorno virtual de Python, ejecutar desde la raíz del repositorio:

```bash
cd services/gateway-api
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v
```

Las pruebas ejercitan `GET /health` mediante ASGI y comprueban que dos arranques de la aplicación conservan el mismo registro en una base SQLite temporal. En la copia del repositorio se cierran explícitamente las conexiones SQLite después de cada uso. La prueba local en Windows detectó que aplazar el cierre podía mantener abierto el archivo después de la petición. Se conserva la transacción de inicialización y la respuesta HTTP de la implementación desplegada.
