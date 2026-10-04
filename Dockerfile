FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Copy src/ only if it exists, otherwise create an empty directory
COPY src/ /app/src/ 2>/dev/null || mkdir -p /app/src

WORKDIR /trabajo

ENTRYPOINT ["python3", "-m", "escaner_artefactos"]
CMD ["--help"]
