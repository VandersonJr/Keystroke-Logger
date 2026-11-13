import os
import secrets

from flask import Flask, jsonify, render_template, request
from app.database.connection import get_connection
from app.database import models
from app.collector.event_collector import collect
from app.dashboard.routes import bp as dashboard_bp


def create_app(db_path="data/audit.db"):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["DB_PATH"] = db_path
    # Defina KEYLOGGER_SECRET_KEY em produção; sem ela, as sessões de login caem a cada reinício.
    app.config["SECRET_KEY"] = os.environ.get("KEYLOGGER_SECRET_KEY") or secrets.token_hex(32)
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")
    app.register_blueprint(dashboard_bp)

    def db():
        return get_connection(app.config["DB_PATH"])

    @app.get("/")
    def lab():
        return render_template("lab.html")

    @app.post("/api/session/start")
    def start():
        data = request.get_json(silent=True) or {}
        try:
            sid, token = models.start_session(db(), bool(data.get("consent")))
        except PermissionError as e:
            return jsonify(error=str(e)), 403
        return jsonify(session_id=sid, token=token)

    @app.post("/api/session/<int:sid>/events")
    def events(sid):
        batch = (request.get_json(silent=True) or {}).get("events", [])[:200]
        conn = db()
        saved = sum(collect(conn, sid, e) for e in batch if isinstance(e, dict))
        return jsonify(saved=saved)

    @app.post("/api/session/<int:sid>/finish")
    def finish(sid):
        models.finish_session(db(), sid)
        return jsonify(ok=True)

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
