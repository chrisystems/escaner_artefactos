FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

COPY src/ /app/src/

WORKDIR /trabajo

ENTRYPOINT ["python3", "-m", "escaner_artefactos"]
CMD ["--help"]