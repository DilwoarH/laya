# laya

Flask API that wraps the `laya` `Router` agent for typed-decision predictions.

## Running with Docker

Build and start the server:

```bash
docker compose up --build
```

The API will be available at `http://127.0.0.1:8001`.

- `GET /health` — health check
- `POST /predict` — body: `{"state": "...", "questions": {...}}`

The `typed-decisions` model checkpoint is downloaded from Hugging Face Hub on
first startup and cached in the `hf-cache` Docker volume, so subsequent
restarts don't re-download it.

Stop the server:

```bash
docker compose down
```

## Testing the API

With the server running, use the sample client from the host:

```bash
pip install requests
python client.py
```

## Running locally without Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
