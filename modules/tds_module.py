from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models import TdsEntry, Party
from sqlalchemy import func
from datetime import date

tds_bp = Blueprint("tds", __name__)

TDS_SECTIONS = {
    "194C": {"name":"Contractor","rate":1.0,"threshold":30000},
    "194J": {"name":"Professional","rate":10.0,"threshold":30000},
    "194I": {"name":"Rent","rate":10.0,"threshold":240000},
    "194H": {"name":"Commission","rate":5.0,"threshold":15000},
    "194A": {"name":"Interest","rate":10.0,"threshold":40000},
    "192":  {"name":"Salary","rate":0.0,"threshold":0},
}

@tds_bp.route("/tds")
@login_required
def index():
    cid = session.get("company_id")
    fy  = session.get("fin_year")
    entries = TdsEntry.query.filter_by(company_id=cid, fin_year=fy
              ).order_by(TdsEntry.txn_date.desc()).all()
    total_tds     = sum(float(e.tds_amount) for e in entries)
    pending_tds   = sum(float(e.tds_amount) for e in entries if not e.is_paid)
    return render_template("tds/index.html",
        entries=entries, total_tds=total_tds,
        pending_tds=pending_tds, sections=TDS_SECTIONS, fy=fy)

@tds_bp.route("/tds/create", methods=["GET","POST"])
@login_required
def create():
    cid   = session.get("company_id")
    fy    = session.get("fin_year")
    parties = Party.query.filter_by(company_id=cid, is_active=True).all()
    if request.method == "POST":
        section    = request.form.get("section")
        tds_rate   = float(TDS_SECTIONS.get(section,{}).get("rate",0))
        amount     = float(request.form.get("amount",0))
        tds_amount = round(amount * tds_rate / 100, 2)
        entry = TdsEntry(
            company_id = cid, fin_year = fy,
            party_id   = int(request.form.get("party_id")),
            section    = section,
            txn_date   = date.fromisoformat(request.form.get("txn_date")),
            amount     = amount, tds_rate = tds_rate, tds_amount = tds_amount,
        )
        db.session.add(entry); db.session.commit()
        flash("TDS entry saved.", "success")
        return redirect(url_for("tds.index"))
    return render_template("tds/create.html", parties=parties, sections=TDS_SECTIONS)
