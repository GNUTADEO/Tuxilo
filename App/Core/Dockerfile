# =================================================
# Stage 1: Start application
# =================================================
FROM python:3.14-slim-bookworm
WORKDIR /api
RUN apt-get update && apt-get install -y \
    gcc\
    g++\
    libpq-dev\
    curl\
    jq\
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# 2. Install shared packages from local files
# -----------------------------
COPY src/packages/shared_db.zip ./shared_db.zip
COPY src/packages/models_stub.zip ./models_stub.zip

RUN pip install --no-cache-dir ./shared_db.zip \
    && pip install --no-cache-dir ./models_stub.zip \
    && rm *.zip

# -----------------------------
# 3. Config virtual environment
# -----------------------------
COPY src/pyproject.toml ./pyproject.toml
RUN pip install --no-cache-dir -e .

# -----------------------------
# 4. Copy app
# -----------------------------
COPY src/main.py ./main.py
COPY src/routers ./routers
COPY src/models ./models

# -----------------------------
# 5. setup entrypoint
# -----------------------------
COPY entrypoint_core.sh /entrypoint_core.sh
RUN chmod +x /entrypoint_core.sh
ENTRYPOINT ["/entrypoint_core.sh"]

# -----------------------------
# 6. Run uvicorn
# -----------------------------
CMD ["sh", "-c", "uvicorn main:api --host 0.0.0.0 --port 8000"]