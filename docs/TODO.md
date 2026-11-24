# TODO — Demo Linux Server Monitoring App

Small, AI-friendly increments for a **local-only** Flask demo. Metrics are simulated (no SSH).

Default login (once auth lands): `admin` / `test123` (hashed). App port: **5010** (avoid clash with other local demos on 5000/5001).

---

## 1. Project initialization and basic UI (skeleton / phase 0)

- [x] Create project layout (`app.py`, `templates/`, `static/`, `docs/`, `requirements.txt`)
- [x] Add `.gitignore` (venv, `__pycache__`, `*.db`, `.env`)
- [x] Add minimal `README.md` (venv → install → run → open URL)
- [x] Scaffold Flask app bound to `127.0.0.1` only
- [x] Add base layout + simple attractive login/landing shell (CSS)
- [x] **Security:** Bind localhost only; do not commit secrets; gitignore `.env` / DB
- [x] **Docs:** Note local-demo scope and run steps in `README.md`; keep `docs/requirements.md` short

---

## 2. Sign-in and unit tests

- [x] Add session-based login route (`GET`/`POST /login`) and logout
- [x] Seed default user `admin` with **Werkzeug-hashed** password (`test123`)
- [x] Protect dashboard and APIs: redirect unauthenticated users to login
- [x] Generic error message on failed login (do not reveal which field failed)
- [x] Add `pytest` + Flask test client fixtures (`tests/conftest.py`)
- [x] Unit tests: successful login, failed login, logout clears session, protected route redirects
- [x] Unit test: password stored/checked as hash (plaintext never in responses)
- [x] **Security:** Use `SECRET_KEY` for sessions; `check_password_hash` only; never log passwords
- [x] **Docs:** Document default creds and “demo only” warning in `README.md` / `docs/security.md`

---

## 3. Server inventory (add Linux hosts)

- [x] SQLite table for servers (name, hostname/IP, optional description)
- [x] Add-server form (auth required)
- [x] List servers on dashboard
- [x] Remove server from inventory (POST; confirm in UI)
- [x] Unit tests: add server requires login; list/delete behavior; no secrets in HTML
- [x] **Security:** Only authenticated users can mutate inventory; validate required fields; no remote exec
- [x] **Docs:** Document add-server fields and that metrics are simulated

---

## 4. Read-only monitoring UI (simulated metrics)

- [x] Simulator for CPU, memory, network in/out, listening ports (seeded by server id)
- [x] Dashboard cards showing metrics (read-only)
- [x] Auto-refresh via JSON API (~5s) with session auth
- [x] Unit tests: metrics shape/keys; API requires login; 404 for unknown server
- [x] **Security:** Metrics endpoints require session; responses contain no credentials
- [x] **Docs:** State clearly that values are simulated (not live SSH)

---

## 5. Hardening polish (demo-appropriate)

- [x] Load `SECRET_KEY` / admin seed password from env (safe local defaults in code)
- [x] Add CSRF protection on login and mutating forms (e.g. Flask-WTF)
- [x] Ensure flash/error messages never echo passwords
- [x] **Security:** Short `docs/security.md` (hashed password, localhost bind, no SSH secrets)
- [x] **Docs:** Point README to `docs/security.md` and `docs/requirements.md`

---

## 6. CI/CD — GitHub Actions

- [x] Add `.github/workflows/ci.yml`
- [x] On push/PR: checkout → set up Python → install deps → run `pytest`
- [x] Fail CI if unit tests fail
- [x] **Security:** No real secrets in workflow; use dummy `SECRET_KEY` / test password env vars only
- [x] **Docs:** One-line note in README that CI runs tests on GitHub Actions

---

## 7. Final local demo checklist

- [x] Fresh clone path: `python3 -m venv .venv` → `pip install -r requirements.txt` → `python app.py`
- [x] Confirm login `admin` / `test123` on http://127.0.0.1:5010
- [x] Confirm add server → metrics cards refresh
- [x] Confirm unauthenticated access redirects to login
- [x] **Docs:** README stays minimal (local deploy only; no cloud steps)
