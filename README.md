# Demo Linux Server Monitoring App

Local-only Flask demo that shows a read-only monitoring UI for registered Linux servers. **Metrics are simulated** (no SSH or agents).

## Scope

- Runs on the machine where you develop (Cursor / localhost)
- Binds to `127.0.0.1:5001` only
- Not for production or cloud deploy

See [docs/requirements.md](docs/requirements.md) for product scope.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5001

## Layout

| Path | Purpose |
|------|---------|
| `app.py` | Flask entrypoint |
| `templates/` | Jinja HTML |
| `static/` | CSS / JS |
| `docs/` | Requirements and TODO |

## Security notes (demo)

- Do not commit `.env`, secrets, or `*.db` (see `.gitignore`)
- App must stay bound to localhost for this demo
