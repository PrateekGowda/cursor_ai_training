# Security notes — local demo only

This app is a **local demo**, not production software.

## Defaults

- Binds to `127.0.0.1:5010` only (do not expose on `0.0.0.0`)
- Default user: `admin` / `test123`
- Password is stored and checked with **Werkzeug** hashing (`generate_password_hash` / `check_password_hash`)
- Override locally with env vars: `SECRET_KEY`, `ADMIN_PASSWORD` (and optional `ADMIN_USERNAME`, `DATABASE`)

## What this demo does not do

- No SSH, agents, or remote execution
- No real host credentials stored for monitoring
- No HTTPS / HA / multi-user LDAP

## Protections included

- Session cookie auth for dashboard and metrics API
- CSRF tokens on login and mutating forms (Flask-WTF)
- Flash/error messages never echo submitted passwords
- `.env`, `*.db`, and venv paths are gitignored

See also [requirements.md](requirements.md).
