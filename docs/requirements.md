# Requirements — Demo Linux Server Monitoring App

## Problem
Internal L1/L2/L3 and application teams currently log into Linux servers to check real-time memory, CPU, network usage, and port details. This demo provides a local, read-only monitoring UI so teams can view that information without SSH-ing into each host.

## Users
Internal infrastructure and application development teams (L1, L2, L3).

## Scope
Local demo only. Metrics are **simulated** (no SSH/agent collection). Deploy where Cursor is running.

## Features

### 1. Read-only monitoring UI
- User-friendly dashboard showing registered Linux servers
- Display simulated CPU %, memory used/total, network in/out, and listening ports
- Metrics auto-refresh approximately every 5 seconds
- Monitoring views are read-only (no remote actions)

### 2. Sign-in
- Session-based login
- Default username: `admin`
- Password: `test123` (stored hashed with Werkzeug)
- Unauthenticated users are redirected to login

### 3. Server inventory
- Add a Linux server (name, hostname/IP, optional description)
- List servers on the dashboard
- Remove a server from inventory (maintenance only; metrics remain read-only)

## Tech stack
- Python, Flask, Jinja templates
- SQLite for server inventory
- Vanilla CSS/JS for UI and refresh

## Non-goals
- Real SSH or agent-based metric collection
- Multi-user roles / LDAP
- Production hardening (HTTPS, HA)
