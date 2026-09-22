FROM python:3.14-slim

WORKDIR /app

# System deps needed to build/run torch and friends.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Model checkpoints downloaded by agent.preload() are cached here across restarts if mounted as a volume.
ENV HF_HOME=/app/.cache/huggingface

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--timeout", "120", "app:app"]
