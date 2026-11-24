"""
Demo Linux Server Monitoring App — local-only Flask skeleton.
Metrics are simulated; bind is localhost only.
"""

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-only-change-me"


@app.route("/")
def index():
    """Landing: send visitors to the login shell for now."""
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login / landing shell (session auth wired in the next phase)."""
    # POST is accepted so the form shell works; credentials are ignored for now.
    if request.method == "POST":
        flash("Sign-in lands in the next phase — skeleton only for now.", "error")
    return render_template("login.html")


if __name__ == "__main__":
    # Local demo only — never bind 0.0.0.0 for this app.
    app.run(host="127.0.0.1", port=5001, debug=True)
