FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Create the src directory
RUN mkdir -p /app/src

# Copy src/ if it exists, otherwise skip
COPY --chown=root:root src/ /app/src/ || true

WORKDIR /trabajo

ENTRYPOINT ["python3", "-m", "escaner_artefactos"]
CMD ["--help"]
