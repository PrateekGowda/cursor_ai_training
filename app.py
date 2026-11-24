"""
Demo Linux Server Monitoring App — local-only Flask demo.
Metrics are simulated; bind is localhost only.
"""

from __future__ import annotations

import os
import sqlite3
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_wtf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash

from metrics import simulate_metrics

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB = BASE_DIR / "monitor.db"

csrf = CSRFProtect()


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        DATABASE=str(os.environ.get("DATABASE", DEFAULT_DB)),
        ADMIN_USERNAME=os.environ.get("ADMIN_USERNAME", "admin"),
        ADMIN_PASSWORD=os.environ.get("ADMIN_PASSWORD", "test123"),
        WTF_CSRF_ENABLED=True,
        WTF_CSRF_CHECK_DEFAULT=True,
    )
    if test_config:
        app.config.update(test_config)

    # Hash once at startup; plaintext password is never stored on disk.
    app.config["ADMIN_PASSWORD_HASH"] = generate_password_hash(
        app.config["ADMIN_PASSWORD"]
    )

    csrf.init_app(app)

    @app.before_request
    def _open_db() -> None:
        g.db = get_db(app)

    @app.teardown_appcontext
    def _close_db(_exc: BaseException | None) -> None:
        db = g.pop("db", None)
        if db is not None:
            db.close()

    with app.app_context():
        init_db(app)

    register_routes(app)
    return app


def get_db(app: Flask) -> sqlite3.Connection:
    db = getattr(g, "db", None)
    if db is not None:
        return db
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(app: Flask) -> None:
    db_path = Path(app.config["DATABASE"])
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                host TEXT NOT NULL,
                description TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def register_routes(app: Flask) -> None:
    @app.route("/")
    def index():
        if session.get("user"):
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if session.get("user"):
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            # Never log passwords; never echo them in flash messages.
            ok = (
                username == app.config["ADMIN_USERNAME"]
                and check_password_hash(app.config["ADMIN_PASSWORD_HASH"], password)
            )
            if ok:
                session.clear()
                session["user"] = username
                return redirect(url_for("dashboard"))
            flash("Invalid username or password.", "error")

        return render_template("login.html")

    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()
        flash("Signed out.", "success")
        return redirect(url_for("login"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        servers = (
            g.db.execute(
                "SELECT id, name, host, description FROM servers ORDER BY id"
            ).fetchall()
        )
        return render_template("dashboard.html", servers=servers)

    @app.route("/servers", methods=["POST"])
    @login_required
    def add_server():
        name = (request.form.get("name") or "").strip()
        host = (request.form.get("host") or "").strip()
        description = (request.form.get("description") or "").strip() or None

        if not name or not host:
            flash("Name and hostname/IP are required.", "error")
            return redirect(url_for("dashboard"))

        g.db.execute(
            "INSERT INTO servers (name, host, description) VALUES (?, ?, ?)",
            (name, host, description),
        )
        g.db.commit()
        flash("Server added.", "success")
        return redirect(url_for("dashboard"))

    @app.route("/servers/<int:server_id>/delete", methods=["POST"])
    @login_required
    def delete_server(server_id: int):
        cur = g.db.execute("DELETE FROM servers WHERE id = ?", (server_id,))
        g.db.commit()
        if cur.rowcount:
            flash("Server removed.", "success")
        else:
            flash("Server not found.", "error")
        return redirect(url_for("dashboard"))

    @app.route("/api/servers/<int:server_id>/metrics")
    @login_required
    def server_metrics(server_id: int):
        row = g.db.execute(
            "SELECT id FROM servers WHERE id = ?", (server_id,)
        ).fetchone()
        if row is None:
            return jsonify({"error": "not found"}), 404
        return jsonify(simulate_metrics(server_id))


app = create_app()


if __name__ == "__main__":
    # Local demo only — never bind 0.0.0.0 for this app.
    # Port 5010: 5000/5001 are often taken by other local demos on shared hosts.
    app.run(host="127.0.0.1", port=5010, debug=True)
