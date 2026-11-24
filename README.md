# Demo Linux Server Monitoring App

Local-only Flask demo that shows a read-only monitoring UI for registered Linux servers. **Metrics are simulated** (no SSH or agents).

## Scope

- Runs on the machine where you develop (Cursor / localhost)
- Binds to `127.0.0.1:5010` only
- Not for production or cloud deploy

See [docs/requirements.md](docs/requirements.md) for product scope and [docs/security.md](docs/security.md) for demo security notes.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5010

**Default login (demo only):** `admin` / `test123` (password stored hashed).

Optional env overrides: `SECRET_KEY`, `ADMIN_PASSWORD`, `ADMIN_USERNAME`, `DATABASE`.

## Using the demo

1. Sign in with the default credentials
2. Add a Linux server (name, hostname/IP, optional description)
3. Watch simulated CPU, memory, network, and listening ports refresh ~every 5s
4. Remove a server from inventory when finished (metrics remain read-only; no remote actions)

## Tests / CI

```bash
pytest -q
```

GitHub Actions runs the same `pytest` suite on push and pull requests (dummy `SECRET_KEY` / demo password env only).

## Layout

| Path | Purpose |
|------|---------|
| `app.py` | Flask entrypoint |
| `metrics.py` | Simulated metric generator |
| `templates/` | Jinja HTML |
| `static/` | CSS / JS |
| `tests/` | Unit tests |
| `docs/` | Requirements, security, TODO |
