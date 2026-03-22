from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import JournalHeader, JournalLine, Account, AuditTrail
from datetime import date, datetime

journal_bp = Blueprint("journal", __name__)

@journal_bp.route("/journal")
@login_required
def index():
    cid  = session.get("company_id")
    fy   = session.get("fin_year")
    page = request.args.get("page", 1, type=int)
    q    = request.args.get("q","")
    query = JournalHeader.query.filter_by(company_id=cid, fin_year=fy,
                                           is_cancelled=False)
    if q:
        query = query.filter(JournalHeader.voucher_no.ilike(f"%{q}%"))
    pagination = query.order_by(JournalHeader.voucher_date.desc()
                 ).paginate(page=page, per_page=50)
    return render_template("journal/index.html", pagination=pagination, q=q)

@journal_bp.route("/journal/create", methods=["GET","POST"])
@login_required
def create():
    cid = session.get("company_id")
    fy  = session.get("fin_year")
    accounts = Account.query.filter_by(company_id=cid, is_active=True
               ).order_by(Account.name).all()
    if request.method == "POST":
        jh = JournalHeader(
            company_id   = cid,
            fin_year     = fy,
            voucher_no   = request.form.get("voucher_no"),
            voucher_type = request.form.get("voucher_type","Journal"),
            voucher_date = datetime.strptime(request.form.get("voucher_date"), "%Y-%m-%d").date(),
            narration    = request.form.get("narration",""),
            created_by   = current_user.id,
        )
        db.session.add(jh); db.session.flush()
        acc_ids = request.form.getlist("account_id[]")
        debits  = request.form.getlist("debit[]")
        credits = request.form.getlist("credit[]")
        for i, acc_id in enumerate(acc_ids):
            if not acc_id: continue
            jl = JournalLine(
                journal_header_id = jh.id,
                account_id = int(acc_id),
                debit  = float(debits[i]  or 0),
                credit = float(credits[i] or 0),
            )
            db.session.add(jl)
        db.session.commit()
        flash("Journal entry saved.", "success")
        return redirect(url_for("journal.index"))
    return render_template("journal/create.html", accounts=accounts)

@journal_bp.route("/journal/<int:jh_id>")
@login_required
def view(jh_id):
    jh = JournalHeader.query.get_or_404(jh_id)
    return render_template("journal/view.html", jh=jh)

@journal_bp.route("/journal/<int:jh_id>/cancel")
@login_required
def cancel(jh_id):
    jh = JournalHeader.query.get_or_404(jh_id)
    jh.is_cancelled = True
    db.session.commit()
    flash("Entry cancelled.", "warning")
    return redirect(url_for("journal.index"))
