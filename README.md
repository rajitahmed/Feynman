# Feynman

Voice-first Feynman-method practice tool. See `docs/SPEC.md`.

## Run it

Server (needs [uv](https://docs.astral.sh/uv/)). Copy `server/.env.example` to `server/.env` and fill in the keys first.

```
cd server
uv sync
uv run fastapi dev main.py      # http://localhost:8000/health
```

Client (needs Node):

```
cd client
npm install
npm run dev                     # http://localhost:5173
```

## Checks

```
cd server && uv run ruff format --check . && uv run ruff check . && uv run pytest
cd client && npm run format:check && npm run lint && npm run build
```
