FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Create the src directory and copy if it exists
RUN mkdir -p /app/src
COPY src/ /app/src/ 2>/dev/null || true

WORKDIR /trabajo

ENTRYPOINT ["python3", "-m", "escaner_artefactos"]
CMD ["--help"]
