# Docker en la Raspberry Pi · Fase 4

**VERIFICADO el 10 de noviembre de 2026.** Las capturas del chat «Investiga distribuciones Raspberry Pi» muestran Docker Engine ejecutando `hello-world` en ARM64 y un volumen de Compose que conserva un archivo después de eliminar y recrear el contenedor.

## Instalación y comprobaciones

El procedimiento del chat utiliza el repositorio APT oficial de Docker para Debian 13 Trixie, arquitectura `arm64`. Para reproducir la instalación, revisar los paquetes existentes, configurar la clave y la fuente APT firmada e instalar `docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-buildx-plugin` y `docker-compose-plugin`. El procedimiento indica habilitar Docker y containerd con systemd. Las capturas de estado corresponden al servicio `docker`. [Instalación oficial para Debian](https://docs.docker.com/engine/install/debian/).

| Comprobación | Resultado observado |
|---|---|
| `sudo docker run --rm hello-world` | `Hello from Docker!` con imagen `arm64v8` |
| `docker compose version` | `v5.7.0`. La versión exacta de Docker Engine no figura en las capturas. |
| `systemctl is-active docker` y `systemctl is-enabled docker` | `active` y `enabled` |
| `sudo docker info --format '{{.DockerRootDir}}'` | `/var/lib/docker` en la raíz EXT4 del SSD Kingston |
| `df -h /` | `/dev/sda2` montada en `/`, 101G disponibles y 5 % de uso |
| `sudo docker system df` | Antes de la prueba Compose se veía una imagen, cero contenedores y cero volúmenes locales |
| `vcgencmd get_throttled` | `throttled=0x0` en la lectura |

## Prueba de persistencia con Compose

En el directorio de prueba `~/pi-agents-smoke` se guardó este `compose.yaml`. El servicio `probe` solo crea `/data/marker` cuando el archivo aún no existe. En cada arranque escribe su contenido en el log. El volumen `check_data` se monta en `/data` y el servicio no publica puertos.

```yaml
services:
  probe:
    image: busybox:stable
    command: >
      sh -c 'test -f /data/marker ||
      date -u > /data/marker;
      echo "Dato persistente:";
      cat /data/marker;
      sleep 3600'
    volumes:
      - check_data:/data

volumes:
  check_data:
```

Desde el mismo directorio se realizaron dos lecturas:

```bash
cd ~/pi-agents-smoke
sudo docker compose up -d
sudo docker compose ps
sudo docker compose logs probe

sudo docker compose down
sudo docker compose up -d
sudo docker compose logs probe
```

| Momento | Resultado |
|---|---|
| Primer `up` | Compose creó `pi-agents-smoke_check_data` y arrancó `probe`. El log mostró `Tue Nov 10 01:24:11 UTC 2026`. |
| Tras `down` y el segundo `up` | Compose eliminó el contenedor y su red y volvió a crearlos. El nuevo `probe` leyó `Tue Nov 10 01:24:11 UTC 2026`. |

El marcador sobrevivió a la recreación del contenedor. La prueba se hizo con `down` sin `-v` para conservar el volumen. La limpieza posterior del proyecto de prueba se propuso en el chat y queda sin confirmar. [Referencia de Docker Compose](https://docs.docker.com/reference/cli/docker/compose/down/).

La estabilidad prolongada del SSD y la restauración de copias siguen abiertas. La fase 5 prevé comprobar `GET /health` y la persistencia de una base SQLite en el primer controlador FastAPI. [Roadmap del controlador](00-roadmap.md).
