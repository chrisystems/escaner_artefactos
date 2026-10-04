FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /trabajo

# Copia el contenido del repositorio al contenedor.
COPY . /trabajo

# Si existe un directorio src/, lo añade al PYTHONPATH para que el paquete
# pueda importarse como: python3 -m escaner_artefactos.
RUN if [ -d /trabajo/src ]; then \
      echo 'export PYTHONPATH=/trabajo/src' > /etc/profile.d/pythonpath.sh; \
    fi

ENTRYPOINT ["python3", "-m", "escaner_artefactos"]
CMD ["--help"]
