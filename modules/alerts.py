from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required
from extensions import db
from models import ComplianceAlert
from datetime import date

alerts_bp = Blueprint("alerts", __name__)

@alerts_bp.route("/alerts")
@login_required
def index():
    cid    = session.get("company_id")
    alerts = ComplianceAlert.query.filter_by(company_id=cid
             ).order_by(ComplianceAlert.due_date).all()
    overdue  = [a for a in alerts if a.status=="pending" and a.due_date < date.today()]
    upcoming = [a for a in alerts if a.status=="pending" and a.due_date >= date.today()]
    return render_template("alerts/index.html",
        overdue=overdue, upcoming=upcoming, today=date.today())

@alerts_bp.route("/alerts/dismiss/<int:alert_id>")
@login_required
def dismiss(alert_id):
    a = ComplianceAlert.query.get_or_404(alert_id)
    a.status = "dismissed"
    db.session.commit()
    return redirect(url_for("alerts.index"))

@alerts_bp.route("/alerts/complete/<int:alert_id>")
@login_required
def complete(alert_id):
    a = ComplianceAlert.query.get_or_404(alert_id)
    a.status = "completed"
    db.session.commit()
    return redirect(url_for("alerts.index"))
