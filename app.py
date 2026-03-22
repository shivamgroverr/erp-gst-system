# app.py — Main Flask Application
from flask import Flask, redirect, url_for, session
from flask_login import current_user
from extensions import db, login_manager, migrate
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"]          = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # ── Register all blueprints ──────────────────────────────
    from modules.auth       import auth_bp
    from modules.gst_module import gst_bp
    from modules.reports    import reports_bp
    from modules.journal    import journal_bp
    from modules.alerts     import alerts_bp
    from modules.tds_module import tds_bp
    from modules.smf_calculator import smf_bp
    from modules.year_closing   import year_bp
    from modules.validators     import validator_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(gst_bp,       url_prefix="/gst")
    app.register_blueprint(reports_bp,   url_prefix="/")
    app.register_blueprint(journal_bp,   url_prefix="/journal")
    app.register_blueprint(alerts_bp,    url_prefix="/alerts")
    app.register_blueprint(tds_bp,       url_prefix="/tds")
    app.register_blueprint(smf_bp,       url_prefix="/smf")
    app.register_blueprint(year_bp,      url_prefix="/year")
    app.register_blueprint(validator_bp, url_prefix="/validate")

    # ── Context processor (company, year, alert count) ──────
    @app.context_processor
    def inject_globals():
        from models import ComplianceAlert
        alert_count = 0
        if current_user.is_authenticated:
            cid = session.get("company_id")
            if cid:
                alert_count = ComplianceAlert.query.filter_by(
                    company_id=cid, status="pending").count()
        return dict(
            company_name=session.get("company_name",""),
            fin_year=session.get("fin_year",""),
            alert_count=alert_count,
        )

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("reports.hub"))
        return redirect(url_for("auth.login"))

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
